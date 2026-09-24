---
name: dialog-map
description: Trigger is exact "dialog-map" phrase.
---

# Overview
Creates and edits dialog maps (IBIS-style question/answer/pro/con trees).

Dialog maps are visible trees (Directed Graphs) of decisions and rationale. They are composed of questions, answers, pros, and cons. Indentation-based nesting provides context for sub-nodes, enabling fast context and rationale lookups.

<!-- note: They're also great for keeping meetings on track and productive. I've used this structure for facilitating in-person meetings of up to 30 people. It prevents repeating topics, ensures all perspectives are heard, and clarifies when statements actually answer the questions at hand. -->

## Instructions
Use this skill to:
1. **Create** a dialog map from free-form text (meeting notes, a problem
   description, a transcript, an email thread, dialog with the user, etc).
2. **Modify** an existing dialog map when the user asks to add, remove,
   reorganize, or resolve nodes — in the same conversation or a pasted map.

## Format

Indentation-based outline using these node types:

| Symbol | Node     | Allowed Children |
|--------|----------|--------------------|
| `?`    | Question | `?/./*` |
| `.`    | Answer   | `?/+/-` |
| `*`    | Answer (chosen as decision) | `?/+/-` |
| `+`    | Pro      | `?` |
| `-`    | Con      | `?` |

### Example
```
What should we eat?
  . salad
    - insufficient protein
  . pizza
    + cheese has protein
    - too salty
  * sushi
    + yummy
    + good protein
    Where should we get it from?
      . restaurant
        - expensive
      * grocery store
```

## Node Rules
- `?`: Questions must conform to `## Question Taxonomy`.
- `?`: Any node may have questions
- `*`: When a question has >= 2 decision answers (`*`), those answers and their pros/cons must be logically compatible. If they are not, notify the user.

## Question Taxonomy
Use this taxonomy to sanity-check that each `?` node is really a question (not a statement) and to help phrase new questions when the user asks you to add one.

| Type | Asks about | Example |
| ------ | ----------- | --------- |
| Deontic | The ultimate goal | "What should we do about x?" |
| Instrumental | The method/means to a goal | "How should we do x?" |
| Issue | The problem to be addressed | "What is the problem with x?" |
| Criteria | Standards for a good answer | "What are the criteria for a good answer to question x?" |
| Meaning | Shared understanding of a term | "What does x mean mean?" |
| Factual | Objective facts | "What are team metric values?" |
| Context | History/background | "What led us to this point?" |
| Stakeholder | People/groups involved or affected | "Who are the project's stakeholders?" |



## Converting free-form text to a dialog map

1. Read through the source text and identify the central question(s) being
   discussed — these become the top-level `?` nodes.
2. For each question, pull out the distinct options/positions people raised
   as `.` answers.
3. Under each answer, extract the reasons given for or against it as `+`/`-`
   children. Don't invent pros/cons that aren't implied by the source text.
4. If the source text shows a decision was actually made, mark that answer
   `*` instead of `.`.
5. If resolving one answer raises a new question (e.g. "sushi — but from
   where?"), nest a `?` under that node and repeat.
6. When the source text is ambiguous or missing reasoning for a claim, leave
   it out rather than fabricating a pro/con — a thin map is better than an
   invented one.




## Modifying an existing map

When the user asks to change a map (theirs or one you generated earlier):
- Preserve existing structure and wording except for what they asked to
  change — don't silently reorganize or reword untouched nodes.
- Adding a node: place it at the correct nesting level per the containment
  rules above (e.g. a new pro/con goes under an answer, not a question).
- Marking a decision: change that answer's symbol from `.` to `*`.
- Removing a node: remove its entire subtree with it.
- When asked to output the map, always output the full, latest, updated tree.

## Output

Return the dialog map as a plain-text code block in the format above. Don't
add commentary before or after unless the user asked a question that needs
one, or you made a judgment call worth flagging (e.g. you omitted an
unsupported pro/con, or left an ambiguous decision unmarked).
