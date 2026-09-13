# AI Receipt & Expense Tracker

> ⚠️ **THIS IS ONLY A MOCKUP** — This README is a draft/placeholder to align the team before development starts. Details (repo structure, exact commands, file names) will change as we build. Do not treat this as final documentation.

---

## 1. What This Project Is About

This is our **INF1009 Team Project**: a terminal-based, AI-powered receipt and expense tracker.

**The problem:** Manually logging expenses is tedious, so people skip it. This app removes that friction — snap a photo of a receipt, and the AI reads it for you.

**How it works:**
1. User provides a receipt image (via terminal).
2. The AI reads the image and extracts structured data — merchant, date, category, total.
3. The app applies budget/spending rules to the extracted data (e.g. flag overspending in a category).
4. Results are saved to a flat file (CSV/JSON) so expense history persists across runs.
5. User can view summaries and filter past expenses by category.

**Why AI is core, not decoration:** There's no reliable rule-based way to parse an arbitrary photo of a receipt (different formats, fonts, layouts). The AI is doing the actual extraction work — remove it, and the app has no way to turn a photo into usable data. This satisfies the module's "AI is the core engine" requirement.

**Architecture — 4 layers, all procedural (functions only, no classes):**

```
User / receipt image
      ↓
  io_manager        → terminal input/output, validation, formatting
      ↓
  ai_manager         → sends image to AI, validates structured JSON response
      ↓
  logic_manager      → business rules (budget flags, category rules)
      ↓
  data_manager       → save/load CSV or JSON, filter/query past records
```

**Hard constraints we must follow:**
- 100% procedural — no `class` definitions anywhere in the codebase
- AI must be load-bearing (every record passes through the AI API)
- AI responses must be structured JSON, validated before use
- All persistence via flat files (CSV/JSON) — no database
- Must run in Docker on any machine
- Git history must show granular, meaningful commits — no single dump commit

---

## 2. Team Roles & Responsibilities

*(Assign actual names once the team confirms — placeholders below)*

| Role | Owns | Responsibilities |
|---|---|---|
| **io_manager owner** | `io_manager.py` | All terminal input/output. Prompt for receipt file path, validate input (reject bad file paths, re-prompt), format and print all output (summaries, tables, results). **No other file should contain a `print()` call.** |
| **ai_manager owner** | `ai_manager.py` | Build the prompt sent to the AI, call the AI API with the receipt image, parse and validate the JSON response against our expected schema, retry or log gracefully on failure. **No business/domain logic here** — pure API interaction only. |
| **logic_manager owner** | `logic_manager.py` | Apply our budget/spending rules to AI-extracted data. Decide outcomes (flag, accept, alert). Must include at least one multi-condition rule (e.g. category = Groceries AND total > threshold → flag). This is where our actual product idea lives. |
| **data_manager owner** | `data_manager.py` | Save processed records to CSV/JSON, load all records on startup, implement at least one filter/query function (e.g. filter by category or date range), handle missing/corrupt files without crashing. |
| **DevOps / Git owner** | `Dockerfile`, repo hygiene | Set up and maintain the Dockerfile, verify `docker run` produces working output on every team member's machine, enforce branching policy (feature branches, PRs, no direct pushes to main), keep commit history clean and granular. |

**Shared responsibilities (everyone):**
- Write your own unit/test cases for your manager's functions
- Keep your manager's functions decoupled — talk to other managers only through function calls/return values, not shared global state
- Commit early, commit often, on your own feature branch
- Review at least one teammate's PR before it merges

---

## 3. Status

🚧 Planning stage. Architecture and roles above are proposed and subject to team discussion.

---

*This README is a working mockup for internal team alignment — not a finished project document.*
