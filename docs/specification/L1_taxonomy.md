# Grammar Taxonomy

## Source Data

The implemented taxonomy is stored in `data/grammar_patterns/grammar_taxonomy.yaml` under the `grammar_taxonomy` root key (`data/grammar_patterns/grammar_taxonomy.yaml:1`).

## Categories

The current taxonomy contains 18 top-level categories:

- `verb` (`data/grammar_patterns/grammar_taxonomy.yaml:2-40`)
- `tense` (`data/grammar_patterns/grammar_taxonomy.yaml:42-70`)
- `modal` (`data/grammar_patterns/grammar_taxonomy.yaml:72-92`)
- `voice` (`data/grammar_patterns/grammar_taxonomy.yaml:94-110`)
- `mood` (`data/grammar_patterns/grammar_taxonomy.yaml:112-137`)
- `non_finite` (`data/grammar_patterns/grammar_taxonomy.yaml:139-171`)
- `relative` (`data/grammar_patterns/grammar_taxonomy.yaml:173-197`)
- `clause` (`data/grammar_patterns/grammar_taxonomy.yaml:199-223`)
- `syntax` (`data/grammar_patterns/grammar_taxonomy.yaml:225-261`)
- `article` (`data/grammar_patterns/grammar_taxonomy.yaml:263-283`)
- `noun` (`data/grammar_patterns/grammar_taxonomy.yaml:285-301`)
- `pronoun` (`data/grammar_patterns/grammar_taxonomy.yaml:303-326`)
- `adjective` (`data/grammar_patterns/grammar_taxonomy.yaml:328-346`)
- `adverb` (`data/grammar_patterns/grammar_taxonomy.yaml:348-364`)
- `comparison` (`data/grammar_patterns/grammar_taxonomy.yaml:366-392`)
- `preposition` (`data/grammar_patterns/grammar_taxonomy.yaml:394-432`)
- `collocation` (`data/grammar_patterns/grammar_taxonomy.yaml:434-466`)
- `special_construction` (`data/grammar_patterns/grammar_taxonomy.yaml:468-495`)

## Structure

Each top-level category contains pattern groups, and each pattern group contains machine-readable subpattern IDs. For example, `verb.subject_verb_agreement` contains agreement errors such as `third_person_s_missing`, `have_has_confusion`, and `relative_clause_antecedent_agreement` (`data/grammar_patterns/grammar_taxonomy.yaml:2-10`).

## Current Coverage

The taxonomy now covers 378 subpatterns across university entrance exam grammar and error-correction areas. This includes verb forms, tense/aspect, modals, voice, mood and conditionals, non-finite forms, relatives, clauses and conjunctions, syntax, articles, nouns, pronouns, adjectives, adverbs, comparison, prepositions, collocations, and special constructions (`data/grammar_patterns/grammar_taxonomy.yaml:2-495`).
