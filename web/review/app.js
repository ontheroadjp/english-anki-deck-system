const state = {
  words: [],
  query: "",
  status: "",
  view: "cards",
};

const TABLE_COLUMNS = [
  "Headword",
  "Pronunciation",
  "Part of speech",
  "Exam level",
  "Meanings",
  "Example sentence",
  "Example translation",
  "Source",
  "Status",
  "Wordbook",
  "Word audio",
  "Example audio",
];

const summary = document.querySelector("#summary");
const list = document.querySelector("#word-list");
const table = document.querySelector("#word-table");
const search = document.querySelector("#search");
const status = document.querySelector("#status");
const tabCards = document.querySelector("#tab-cards");
const tabTable = document.querySelector("#tab-table");

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
    const message = '<p class="empty">Run export-json before opening this page.</p>';
    list.innerHTML = message;
    table.innerHTML = message;
  });

search.addEventListener("input", (event) => {
  state.query = event.target.value.trim().toLowerCase();
  render();
});

status.addEventListener("change", (event) => {
  state.status = event.target.value;
  render();
});

tabCards.addEventListener("click", () => setView("cards"));
tabTable.addEventListener("click", () => setView("table"));

function setView(view) {
  if (state.view === view) return;
  state.view = view;
  const cardsActive = view === "cards";
  tabCards.setAttribute("aria-selected", String(cardsActive));
  tabTable.setAttribute("aria-selected", String(!cardsActive));
  list.hidden = !cardsActive;
  table.hidden = cardsActive;
  render();
}

function render() {
  const words = state.words.filter(matchesFilters);
  if (state.view === "cards") {
    renderCards(words);
  } else {
    renderTable(words);
  }
}

function renderCards(words) {
  if (words.length === 0) {
    list.innerHTML = '<p class="empty">No words match the current filters.</p>';
    return;
  }
  list.replaceChildren(...words.map(renderWord));
}

function renderTable(words) {
  const rows = words.flatMap((word) =>
    (word.examples || [])
      .filter((example) => !state.status || example.review_status === state.status)
      .map((example) => renderTableRow(word, example)),
  );

  if (rows.length === 0) {
    table.innerHTML = '<p class="empty">No examples match the current filters.</p>';
    return;
  }

  const tableEl = document.createElement("table");
  tableEl.className = "word-table";
  tableEl.innerHTML = `
    <thead>
      <tr>${TABLE_COLUMNS.map((column) => `<th>${escapeHtml(column)}</th>`).join("")}</tr>
    </thead>
    <tbody>${rows.join("")}</tbody>
  `;
  table.replaceChildren(tableEl);
}

function renderTableRow(word, example) {
  const meanings = (word.meanings || []).map((meaning) => meaning.ja).filter(Boolean).join("; ");
  const wordAudio = (word.audio?.word || []).map((audio) => audio.ref || audio.url).filter(Boolean).join(", ");
  const exampleAudio = (word.audio?.examples || [])
    .filter((audio) => audio.example_id === example.id)
    .map((audio) => audio.ref || audio.url)
    .filter(Boolean)
    .join(", ");
  return `
    <tr>
      <td>${escapeHtml(word.headword)}</td>
      <td>${escapeHtml(word.pronunciation || "")}</td>
      <td>${escapeHtml(word.part_of_speech || "")}</td>
      <td>${escapeHtml(word.exam_level || "")}</td>
      <td class="cell-meanings">${escapeHtml(meanings)}</td>
      <td class="cell-wrap">${escapeHtml(example.sentence || "")}</td>
      <td class="cell-wrap">${escapeHtml(example.ja_translation || "")}</td>
      <td>${sourceBadge(example.source)}</td>
      <td>${statusBadge(example.review_status)}</td>
      <td class="cell-wordbook">${escapeHtml(wordbookLabel(word))}</td>
      <td>${escapeHtml(wordAudio || "")}</td>
      <td>${escapeHtml(exampleAudio || "")}</td>
    </tr>
  `;
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
