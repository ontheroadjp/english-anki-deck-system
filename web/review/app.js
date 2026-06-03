const state = {
  words: [],
  query: "",
  status: "",
};

const summary = document.querySelector("#summary");
const list = document.querySelector("#word-list");
const search = document.querySelector("#search");
const status = document.querySelector("#status");

fetch("vocabulary.json")
  .then((response) => {
    if (!response.ok) {
      throw new Error(`Failed to load vocabulary.json: ${response.status}`);
    }
    return response.json();
  })
  .then((data) => {
    state.words = data.words || [];
    summary.textContent = `${data.metadata?.word_count ?? state.words.length} words loaded`;
    render();
  })
  .catch((error) => {
    summary.textContent = error.message;
    list.innerHTML = '<p class="empty">Run export-json before opening this page.</p>';
  });

search.addEventListener("input", (event) => {
  state.query = event.target.value.trim().toLowerCase();
  render();
});

status.addEventListener("change", (event) => {
  state.status = event.target.value;
  render();
});

function render() {
  const words = state.words.filter(matchesFilters);
  if (words.length === 0) {
    list.innerHTML = '<p class="empty">No words match the current filters.</p>';
    return;
  }
  list.replaceChildren(...words.map(renderWord));
}

function matchesFilters(word) {
  const haystack = [
    word.headword,
    word.pronunciation,
    word.part_of_speech,
    word.exam_level,
    ...(word.meanings || []).map((meaning) => meaning.ja),
    ...(word.examples || []).flatMap((example) => [
      example.sentence,
      example.ja_translation,
      example.source,
      example.review_status,
    ]),
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();

  const statusMatch =
    !state.status || (word.examples || []).some((example) => example.review_status === state.status);
  const queryMatch = !state.query || haystack.includes(state.query);
  return statusMatch && queryMatch;
}

function renderWord(word) {
  const article = document.createElement("article");
  article.className = "word-card";

  const statuses = [...new Set((word.examples || []).map((example) => example.review_status))];
  const wordAudio = (word.audio?.word || []).map((audio) => audio.ref || audio.url).filter(Boolean);

  article.innerHTML = `
    <div class="word-header">
      <div>
        <h2>${escapeHtml(word.headword)}</h2>
        <p class="meta">${escapeHtml(compact([word.part_of_speech, word.pronunciation, levelLabel(word)]).join(" / "))}</p>
      </div>
      <div class="badges">${statuses.map(statusBadge).join("")}</div>
    </div>
    <div class="section">
      <h3>Meanings</h3>
      <ol>${(word.meanings || []).map((meaning) => `<li>${escapeHtml(meaning.ja)}</li>`).join("")}</ol>
    </div>
    <div class="section">
      <h3>Examples</h3>
      ${(word.examples || []).map(renderExample).join("")}
    </div>
    <div class="section details">
      <span>Wordbooks: ${escapeHtml(wordbookLabel(word))}</span>
      <span>Word audio: ${escapeHtml(wordAudio.join(", ") || "missing")}</span>
    </div>
  `;
  return article;
}

function renderExample(example) {
  const sourceLabel = example.source === "ai_generated" ? "AI generated" : "Imported";
  return `
    <div class="example">
      <div class="example-top">
        ${sourceBadge(example.source)}
        ${statusBadge(example.review_status)}
        <span>${escapeHtml(sourceLabel)}</span>
      </div>
      <p class="sentence">${escapeHtml(example.sentence)}</p>
      <p class="translation">${escapeHtml(example.ja_translation || "No Japanese translation")}</p>
    </div>
  `;
}

function sourceBadge(value) {
  const sourceValue = value === "ai_generated" ? "ai" : "imported";
  return `<span class="badge source ${escapeHtml(sourceValue)}">${escapeHtml(sourceValue)}</span>`;
}

function statusBadge(value) {
  const statusValue = value || "draft";
  return `<span class="badge ${escapeHtml(statusValue)}">${escapeHtml(statusValue)}</span>`;
}

function wordbookLabel(word) {
  return (word.wordbooks || [])
    .map((entry) => compact([entry.wordbook_name, entry.edition && `${entry.edition}th`, entry.target_number]).join(" "))
    .join(", ") || "none";
}

function levelLabel(word) {
  return compact([word.eiken && `EIKEN ${word.eiken}`, word.exam_level && `Level ${word.exam_level}`]).join(" / ");
}

function compact(values) {
  return values.filter((value) => value !== null && value !== undefined && value !== "");
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
