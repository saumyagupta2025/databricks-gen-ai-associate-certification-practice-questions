# Databricks GenAI Associate — Quiz Trainer

An offline, single-page quiz app that loads your MCQ + open questions from JSON and
lets you take interactive, self-scoring practice quizzes. Built for exam prep — no
server, no build step, no data leaves your browser.

Currently loaded: **600 questions** across four sets — Set 1 Core, Set 2 Applied,
Set 3 Advanced, and **Module Drills (50 per module = 300)**. To drill one module at a
time, select the "Module Drills" set and pick a single section.

## How to run

Just open **`index.html`** in any modern browser (double-click it, or drag it into a
browser tab). That's it — everything is self-contained.

> The app reads questions from `questions.js` (which assigns `window.QUIZ_DATA`).
> `questions.json` is the human-readable source of truth; `questions.js` is the same
> data wrapped so the page works directly from `file://` with no web server.

If your browser ever blocks the local script, run a tiny static server instead:

```bash
cd quiz-app
python3 -m http.server 8000
# then open http://localhost:8000
```

## Publish it on GitHub Pages

This repo is already set up to deploy as a live website — `index.html` is at the root
and a GitHub Actions workflow (`.github/workflows/deploy.yml`) publishes it to Pages on
every push to `main`. No build step.

**One-time setup:**

1. Create an empty repo on GitHub (e.g. `databricks-genai-quiz`). Don't add a README
   from the GitHub UI, so the first push is clean.
2. Push this folder (run these from inside the project folder):

   ```bash
   git init
   git add .
   git commit -m "Quiz trainer: 600-question bank"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git push -u origin main
   ```

   > If `git init` and the first commit were already made for you, skip those two lines
   > and start at `git remote add origin …`.

3. On GitHub: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
4. The "Deploy to GitHub Pages" workflow runs automatically. When it finishes, your app
   is live at `https://<your-username>.github.io/<your-repo>/`.

After that, every `git push` to `main` redeploys. To update questions, edit
`questions.json`, run `python3 build_questions.py`, then commit and push.

> **Privacy note:** GitHub Pages is public — anyone with the URL can see the app and
> its questions. For a private study tool, keep the repo private and just run it
> locally (open `index.html`), or use a host with access control.

## What it does

- **Build a quiz:** pick any combination of question sets, filter by section and by
  type (MCQ / open / all), choose how many questions, toggle shuffle and instant
  feedback.
- **MCQ questions:** pick an option; with instant feedback on, the correct answer and
  a "Why" rationale appear immediately. With it off, you only see results at the end.
- **Open questions:** think through your answer, hit **Reveal model answer**, then mark
  yourself **Got it / Missed** (self-graded).
- **Results:** an overall score ring with a pass-footing verdict (~80%+), plus a
  per-section breakdown so you can see exactly which domains are weak.
- **Review answers:** the full list with the correct key, what you chose, and the
  rationale for every question.
- **Redo missed:** instantly re-quiz only the questions you got wrong.

## Files

| File | Purpose |
|------|---------|
| `index.html` | The entire app (HTML + CSS + JS). Open this. |
| `questions.json` | Source of truth for all questions (human-editable). |
| `questions.js` | Generated wrapper the app loads (`window.QUIZ_DATA = …`). |
| `build_questions.py` | Validates `questions.json` and regenerates `questions.js`. |

## Editing or adding questions

1. Open `questions.json`.
2. Add or edit a question object inside the relevant set's `questions` array:

```json
{
  "id": "set1-q301",
  "set": "set1",
  "section_num": 3,
  "section": "Application Development",
  "weight": 30,
  "type": "mcq",
  "question": "Your question stem here?",
  "options": [
    {"letter": "A", "text": "Option A"},
    {"letter": "B", "text": "Option B"},
    {"letter": "C", "text": "Option C"},
    {"letter": "D", "text": "Option D"}
  ],
  "answer": "B",
  "explanation": "Why B is right and why the others are wrong."
}
```

For an **open** question, set `"type": "open"`, `"options": null`, `"answer": null`,
and put the model answer in `"explanation"`.

3. Run the rebuild (this also validates that every MCQ `answer` matches an option and
   that there are no duplicate IDs):

```bash
python3 build_questions.py
```

4. Reload `index.html`.

## Adding a whole new set

Append a new object to `"sets"` in `questions.json`:

```json
{ "id": "set4", "title": "Set 4 — Mock Exam", "description": "...", "questions": [ ... ] }
```

Then run `python3 build_questions.py`. The new set appears automatically on the setup
screen — no code changes needed.
