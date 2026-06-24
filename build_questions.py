#!/usr/bin/env python3
"""
Regenerate questions.json and questions.js for the quiz app.

USAGE
-----
1) Edit questions in JSON directly (questions.json), OR
2) Run this script to (re)build from a questions.json you maintain.

If you only edit questions.json, just run:  python build_questions.py
It will rewrite questions.js (the file the app actually loads) from questions.json.

JSON SCHEMA (questions.json)
----------------------------
{
  "meta": { "exam": str, "format": str, "blueprint": [ {"num":int,"title":str,"weight":int}, ... ] },
  "sets": [
    {
      "id": "set1", "title": "Set 1 — Core", "description": str,
      "questions": [
        {
          "id": "set1-q1",
          "set": "set1",
          "section_num": 1,            # 1..6
          "section": "Design Applications",
          "weight": 14,
          "type": "mcq",               # "mcq" | "open"
          "question": "stem text",
          "options": [ {"letter":"A","text":"..."}, ... ],  # null for open
          "answer": "B",                # correct letter; null for open
          "explanation": "why / model answer"
        }
      ]
    }
  ]
}

To ADD a question: append an object to the relevant set's "questions" array
following the schema above, then run this script.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
JSON = os.path.join(HERE, "questions.json")
JS   = os.path.join(HERE, "questions.js")

def main():
    if not os.path.exists(JSON):
        sys.exit("questions.json not found.")
    with open(JSON, encoding="utf-8") as f:
        data = json.load(f)

    # light validation
    problems = []
    seen = set()
    for s in data.get("sets", []):
        for q in s.get("questions", []):
            qid = q.get("id")
            if qid in seen: problems.append(f"duplicate id: {qid}")
            seen.add(qid)
            if q.get("type") == "mcq":
                if not q.get("options"): problems.append(f"{qid}: mcq missing options")
                letters = {o["letter"] for o in q.get("options", [])}
                if q.get("answer") not in letters:
                    problems.append(f"{qid}: answer '{q.get('answer')}' not among options {sorted(letters)}")
            elif q.get("type") != "open":
                problems.append(f"{qid}: type must be 'mcq' or 'open'")
    if problems:
        print("VALIDATION ISSUES:")
        for p in problems: print("  -", p)
        print("(fix these in questions.json; aborting)"); sys.exit(1)

    with open(JS, "w", encoding="utf-8") as f:
        f.write("window.QUIZ_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n")

    total = sum(len(s["questions"]) for s in data["sets"])
    mcq = sum(1 for s in data["sets"] for q in s["questions"] if q["type"]=="mcq")
    print(f"OK — wrote questions.js  ({len(data['sets'])} sets, {total} questions: {mcq} MCQ / {total-mcq} open)")

if __name__ == "__main__":
    main()
