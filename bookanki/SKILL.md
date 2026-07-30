---
name: bookanki
description: Generate Anki flashcards from a subchapter of the book repo and sync to AnkiWeb so Anki Android can pull them. Invoke as `/bookanki <book> <N.M>` — e.g. `/bookanki dsa 7.2`. Reads the subchapter prose from this repo, creates a nested deck (Book::Chapter N::Subchapter N.M), generates 8–15 Basic + Cloze cards via AnkiConnect at http://localhost:8765, then triggers sync.
---

# bookanki

Turn a single subchapter of the book repo into Anki flashcards and push them to AnkiWeb. The user reviews on Anki Android after pulling.

## Arguments

Two positional arguments, space-separated after the command:

1. `book` — maps to the top-level repo directory and a display name used in deck titles.
2. `subchapter` — dotted number like `7.2`, `10.4`, `16.1`.

If either is missing or malformed, stop and ask the user. Do not guess.

## Workflow

Follow these steps in order. Each step has an explicit stop condition — respect it.

### 1. Locate and slice the subchapter

Given `book` and subchapter `N.M`:

1. Primary source: `{book}/chapter{N}.md`. If missing, fall back to `{book}/chapter{N}_subchapter_outline.md`. If neither exists, stop and report.
2. Find the heading line matching `## **{N}.{M} ` (note the trailing space — this prevents `7.1` from matching `7.10`). Read from that heading up to, but not including, the `## **{N}.{M+1} ` heading or end of file. That slice is the subchapter body.
3. If the slice is empty or under ~20 lines, stop and tell the user the content looks too thin to card.

Use `Grep -n` to locate both boundary headings, then `Read` with `offset` and `limit` to extract only those lines — avoids pulling the whole chapter file into context when chapters are long.

### 2. Resolve deck name and tags

- Full deck name: `{deck prefix}::Chapter {N}::Subchapter {N}.{M}`. AnkiConnect's `createDeck` creates the full hierarchy when given a `::`-joined name.
- Per-note tags: `["bookanki", "{book}", "ch{N}", "subch{N}.{M}"]`. These tags are the source of truth for the duplicate check in step 4 — decks can be renamed by the user, tags cannot be accidentally lost.

### 3. Check AnkiConnect reachability (and auto-start Anki if needed)

Ping AnkiConnect:
```bash
curl -s --max-time 2 http://localhost:8765 -H 'Content-Type: application/json' \
  -d '{"action":"version","version":6}'
```

Expect `{"result":6,"error":null}` (or a higher integer). If you get that, proceed.

If the request fails (connection refused, timeout, empty body), try to launch Anki desktop in the background and poll until it's ready:

```bash
# launch detached so the skill isn't tied to the GUI process
nohup anki >/dev/null 2>&1 &
disown
```

If `anki` isn't on PATH, also try `flatpak run net.ankiweb.Anki` as a fallback. Then poll the `version` endpoint up to **30 seconds** (sleep 1s between attempts) until it returns a result. Anki's GUI takes a few seconds to boot and AnkiConnect only starts listening once the main window is up.

If after 30s the endpoint is still unreachable, stop and tell the user — likely Anki isn't installed, AnkiConnect add-on isn't installed, or the launcher command differs on their host. Do not proceed to modify any state.

### 4. Skip-if-already-populated check

Call `findNotes` scoped by tag:

```json
{"action":"findNotes","version":6,"params":{"query":"tag:subch{N}.{M} tag:bookanki"}}
```

If the returned `result` array is non-empty, report how many cards already exist and stop. **Do not** regenerate, update, or add duplicates. The user can manually delete the cards or notes in Anki and re-run if they want to redo a subchapter.

### 5. Create the deck if needed

```json
{"action":"createDeck","version":6,"params":{"deck":"{full deck name}"}}
```

Idempotent — safe to call even if the deck already exists.

### 6. Generate cards

Produce **8–15** flashcards covering the essentials of the subchapter. Use a mix:

- **Basic** for definitions, direct Q/A on core concepts, "what problem does X solve", "when would you use X vs Y".
- **Cloze** for terminology, complexity bounds (e.g. `Binary search runs in {{c1::O(log n)}} time`), invariants, tradeoff pairs, and mechanical fill-in-the-blank recall.

Guidelines:
- **One fact per card.** If a card's back has an "and" joining two distinct facts, split it into two cards.
- Prefer **understanding over trivia** — "Why does a BST require balancing?" beats "In what year was the AVL tree invented?".
- Cover any **Common Pitfall / Confusion Point** boxes in the subchapter — those are high-value cards.
- **Code-recall cards** are fine; keep snippets to a handful of lines and wrap them in `<pre>…</pre>` so Anki preserves whitespace.
- **Skip narrative fluff**: "Pause and reflect", "Opening hook", "Bridge to next section", chapter-summary filler, and anecdotes without factual payload.
- Cloze sentences should use `{{c1::…}}`, `{{c2::…}}` — one cloze card can have multiple deletions if they belong to the same conceptual unit.

### 7. Build the `addNotes` payload

Because card content can contain quotes, backticks, and code, **write the payload to a temp file and pass it with `curl --data @`** rather than inlining JSON in a shell argument. This avoids quoting bugs.

Basic note shape:
```json
{
  "deckName": "{full deck}",
  "modelName": "Basic",
  "fields": {"Front": "...", "Back": "..."},
  "tags": ["bookanki","{book}","ch{N}","subch{N}.{M}"],
  "options": {"allowDuplicate": false}
}
```

Cloze note shape:
```json
{
  "deckName": "{full deck}",
  "modelName": "Cloze",
  "fields": {"Text": "... {{c1::answer}} ...", "Back Extra": ""},
  "tags": ["bookanki","{book}","ch{N}","subch{N}.{M}"],
  "options": {"allowDuplicate": false}
}
```

Wrap the list in the `addNotes` envelope:
```json
{"action":"addNotes","version":6,"params":{"notes":[ ... ]}}
```

POST it:
```bash
curl -s http://localhost:8765 -H 'Content-Type: application/json' \
  --data @/tmp/bookanki_payload.json
```

`addNotes` returns `{"result":[<id>, <id>, null, ...], "error":null}`. A `null` entry means that specific note was rejected (usually an empty field or a cloze note with no `{{cN::…}}`). If any nulls appear, report the indices that failed but continue.

### 8. Sync to AnkiWeb

```json
{"action":"sync","version":6}
```

This tells desktop Anki to push to AnkiWeb. The user pulls on Anki Android — either manually or via its auto-sync on app open.

### 9. Report

One concise summary to the user:
- Full deck name (so they can navigate to it on their phone).
- Count of Basic vs Cloze cards added.
- Any failed notes from step 7 with a one-line reason.
- Confirmation that sync was triggered.

## AnkiConnect quick reference

All requests: `POST http://localhost:8765`, header `Content-Type: application/json`, body:
```json
{"action":"<name>","version":6,"params":{...}}
```

Actions used by this skill:
- `version` — connectivity check, no params.
- `createDeck` — `{"deck":"A::B::C"}`.
- `findNotes` — `{"query":"tag:subchN.M tag:bookanki"}`.
- `addNotes` — `{"notes":[…]}`.
- `sync` — no params.

Full action list: https://git.sr.ht/~foosoft/anki-connect

## Stop conditions (summary)

Stop and report without touching Anki if:
- Arguments missing or malformed.
- Neither `chapter{N}.md` nor `chapter{N}_subchapter_outline.md` exists.
- The subchapter slice is empty or trivially short.
- AnkiConnect is unreachable.
- `findNotes` reports existing cards for this subchapter.
