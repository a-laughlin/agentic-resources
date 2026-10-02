# Luce

**Elucidate your Intent** _through incremental interrogation._

_Inspired by Matt Pocock's [grill-me skill](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md)._

## 💡 Why This Exists
When using grill-me, I noticed extraneous (counterproductive) cognitive load along with some other [challenges](#challenges). I built this skill to reduce those effects and gain a few extra [benefits](#benefits). Key results are 2-4x faster decision tree exploration, pausing mid-session, and a shareable tree format for decision records and specs.

For example, from `/luce dinner` to the decision tree below took 3 minutes and 17 keystrokes (excluding enter).

Notation: `?` question, `.` answer, `+` pro, `-` con, `*` decision.

```txt
What should I do about dinner?
    * cook at home
        + no travel with kids
        - cleanup
        Assumptions?
            . you have ingredients for a meal on hand
            . you would cook
            . control over ingredients won't change decision
            . leftovers for later meals won't change decision
            . prep time won't change decision
    . eat out
        + no cleanup
        - travel with kids
        Assumptions?
            . you have a kid-friendly restaurant in mind
            . no prep won't change decision
    Who are you eating with?
        . family with kids
            How many people are eating?
                . 4
            Assumptions?
                . kids are old enough to sit through a restaurant meal
                . family has no dietary restrictions
                . kids will eat ordinary family meals
    Assumptions?
        . time allows cooking at home or eating out
        . eating out costs more than cooking at home
```
_Similar trees produced with Claude Sonnet 5.5 and Opus 5.5 in similar times. The full Sonnet 5.5 session log is available under [Usage Example](#usage-example)._

Over time, the [differences from grill-me](#️-differences-from-grill-me) became significant enough to merit a new name, hence Luce.


## Installation
npx skills: `npx skills add https://www.a-laughlin.com/agentic-resources --skill luce -a claude-code -g`\
pnpm: `pnpm dlx skills add https://www.a-laughlin.com/agentic-resources --skill luce -a claude-code -g`\
Claude plugin: `claude plugin marketplace add a-laughlin/agentic-resources && claude plugin install luce@agentic-resources`\
gh: `gh skill install a-laughlin/agentic-resources luce`\
curl: `curl -fsSL --create-dirs https://www.a-laughlin.com/agentic-resources/agent-skills/luce/SKILL.md -o ~/.claude/skills/luce/SKILL.md`\
--\
Swap `-a claude-code | ~/.claude/skills` for your agent (e.g.`cursor`, `~/.cursor/skills`, `~/.agents/skills`, …).


## Usage

In your favorite AI chat, `/luce <problems, solutions, questions, ideas, anything...>`

## Usage Example

Notation: `?` question, `.` answer, `+` pro, `-` con, `*` decision.

Here's one grilling session with Opus 5.5. Completed in 3 minutes, 17 characters, and without leaving the number pad.
This example required 3 minutes and 17 characters typed, without ever leaving the number pad.

```txt
❯ /grill-me about dinner

⏺ Skill(grill-me)
Successfully loaded skill

What should I do about dinner?
  1 . cook at home
  2 . order delivery
  3 . eat out
  4 . eat leftovers
  5 . get takeout
  6 . skip dinner
  7 ? How much time do you have before dinner?
  8 ? How does cost differ across cooking, delivery, eating out, takeout?
  9 ? Who are you eating with?

---

Type ".": keep all, "123 11": keep "1,2,3,11"pecific, "++|m": more, "defer", "tree", or____.

✻ Cogitated for 6s · done 10:08 PM

❯ 139

What should I do about dinner?
  . cook at home
  . eat out
  Assumptions?
    1 . time allows cooking at home or eating out
    2 . eating out costs more than cooking at

---

You skipped two questions, so I turned them into assumptions.

Type ".": keep all, "123 11": keep "1,2,3,11"pecific, "++|m": more, "defer", "tree", or____.

✻ Crunched for 4s · done 10:08 PM

❯ .

What should I do about dinner?
  . cook at home
  . eat out
  Who are you eating with?
    1 . alone
    2 . partner
    3 . family with kids
    4 . friends
    5 . guests you're hosting
  assumed: time allows cooking at home or eat
  assumed: eating out costs more than cooking at home

---

Type ".": keep all, "123 11": keep "1,2,3,11", "-|g": general, "+|s": specific, "++|m": more, "defer", "tree", or
____.

✻ Brewed for 3s · done 10:08 PM

❯ 3

What should I do about dinner?
  . cook at home
  . eat out
  Who are you eating with?
    . family with kids
      1 ? How old are the kids?
      2 ? How many people are eating?
      3 ? What dietary restrictions does the family have?
      4 ? What foods will the kids eat?
  assumed: time allows cooking at home or eating out
  assumed: eating out costs more than cooking

---

Type ".": keep all, "0":keep none, "123 11": neral, "+|s": specific, "++|m": more, "defer", "tree", or ____.

✻ Cooked for 4s · done 10:09 PM

❯ 2

What should I do about dinner?
  . cook at home
  . eat out
  Who are you eating with?
    . family with kids
      How many people are eating?
      Assumptions?
        1 . kids are old enough to sit throug
        2 . family has no dietary restrictions
        3 . kids will eat ordinary family mea
  assumed: time allows cooking at home or eating out
  assumed: eating out costs more than cooking

---

You skipped three questions, so I turned them into assumptions.

Type ".": keep all, "0":keep none, "123 11": neral, "+|s": specific, "++|m": more, "defer", "tree", or ____.

✻ Baked for 3s · done 10:09 PM

❯ .

What should I do about dinner?
  . cook at home
  . eat out
  Who are you eating with?
    . family with kids
      How many people are eating?
        1 . 3
        2 . 4
        3 . 5
        4 . 6 or more
      assumed: kids are old enough to sit through a restaurant meal
      assumed: family has no dietary restrict
      assumed: kids will eat ordinary family meals
  assumed: time allows cooking at home or eat
  assumed: eating out costs more than cooking at home

---

Type ".": keep all, "123 11": keep "1,2,3,11", "-|g": general, "+|s": specific, "++|m": more, "defer", "tree", or
____.

✻ Cooked for 3s · done 10:09 PM

❯ 2

What should I do about dinner?
  . cook at home
    1 + control over ingredients
    2 + leftovers for later meals
    3 + no travel with kids
    4 - prep time
    5 - cleanup
    6 ? What ingredients do you have on hand?
    7 ? Who would cook?
  . eat out
  Who are you eating with?
    . family with kids
      How many people are eating?
        . 4
  assumed: time allows cooking at home or eat
  assumed: eating out costs more than cooking at home

---

Type ".": keep all, "0":keep none, "123 11": keep "1,2,3,11", "-|g": general, "+|s": specific, "++|m": more, "defer",
"tree", or ____.

✻ Brewed for 6s · done 10:09 PM

❯ 345

What should I do about dinner?
  . cook at home
    + no travel with kids
    - cleanup
    Assumptions?
      1 . you have ingredients for a meal on hand
      2 . you would cook
      3 . control over ingredients won't change decision
      4 . leftovers for later meals won't change decision
      5 . prep time won't change decision
  . eat out
  assumed: time allows cooking at home or eating out
  assumed: eating out costs more than cooking

---

You skipped two questions, two pros, and one con, so I turned them into assumptions.

Type ".": keep all, "0":keep none, "123 11": neral, "+|s": specific, "++|m": more, "defer", "tree", or ____.

✻ Sautéed for 3s · done 10:10 PM

❯ .

What should I do about dinner?
  . cook at home
    + no travel with kids
    - cleanup
  . eat out
    1 + no prep
    2 + no cleanup
    3 + a treat for the kids
    4 - travel with kids
    5 - wait for a table
    6 - less control over ingredients
    7 ? Which restaurant?
  assumed: time allows cooking at home or eating out
  assumed: eating out costs more than cooking

---

Type ".": keep all, "0":keep none, "123 11": neral, "+|s": specific, "++|m": more, "defer", "tree", or ____.

✻ Churned for 5s · done 10:10 PM

❯ 24

What should I do about dinner?
  . cook at home
    + no travel with kids
    - cleanup
  . eat out
    + no cleanup
    - travel with kids
    Assumptions?
      1 . you have a kid-friendly restaurant in mind
      2 . no prep won't change decision
      3 . a treat for the kids won't change decision
      4 . wait for a table won't change decision
      5 . less control over ingredients won't change decision
  assumed: time allows cooking at home or eat
  assumed: eating out costs more than cooking at home

---

You skipped one question, two pros, and two cons, so I turned them into assumptions.

Type ".": keep all, "0":keep none, "123 11": keep "1,2,3,11", "-|g": general, "+|s": specific, "++|m": more, "defer",
"tree", or ____.

✻ Cogitated for 3s · done 10:10 PM

❯ 12

Decide: What should I do about dinner?
  1 . cook at home
    + no travel with kids
    - cleanup
    assumed: you have ingredients for a meal
    assumed: you would cook
  2 . eat out
    + no cleanup
    - travel with kids
    assumed: you have a kid-friendly restaurant in mind
    assumed: no prep won't change decision
  assumed: eating out costs more than cooking at home
  assumed: time allows cooking at home or eat

---

Type "123 11": decide "1,2,3,11", "defer", "t

✻ Sautéed for 3s · done 10:11 PM

❯ 1

What should I do about dinner?
  * cook at home
    + no travel with kids
    - cleanup
    Assumptions?
      . you have ingredients for a meal on hand
      . you would cook
      . control over ingredients won't change decision
      . leftovers for later meals won't chang
      . prep time won't change decision
  . eat out
    + no cleanup
    - travel with kids
    Assumptions?
      . you have a kid-friendly restaurant in
      . no prep won't change decision
  Who are you eating with?
    . family with kids
      How many people are eating?
        . 4
      Assumptions?
        . kids are old enough to sit through a restaurant meal
        . family has no dietary restrictions
        . kids will eat ordinary family meals
  Assumptions?
    . time allows cooking at home or eating out
    . eating out costs more than cooking at home

---

Tree Complete. You decided to cook at home for a family of 4. Does this tree help you settle dinner? Yes=., No=0.

✻ Churned for 4s · done 10:11 PM

❯ .

Persist the current tree? Yes=., No=0.

✻ Crunched for 1s · done 10:11 PM
```

## Challenges
I encountered a few challenges using the original:
- **Scannability:** Paragraphs of free-form text and inline suggestions are slow to scan vs lists.
- **Consistency:** The default skill sometimes outputs lists to choose from, sometimes not. The inconsistent formatting creats unpredictability that slows down entry and comprehension speed.
- **Traceability:** Untyped options and assumptions go unrecorded, leaving no trace for decision records and specs.
- **Shareability:** The linear Q# format and spacing are too verbose and indirect for practical usage in decision records and specs.
- **Understandability:** Questions paragraphs mix options, pros, cons, and sub-questions inconsistently, slowing reasoning about the tree. The linear+batch format obscures tree relationships. Question batches overflow the visible window and require scrolling. "Q#" indexes + batching require remembering numbers and mixing them with typed concepts. The default skill inconsistently outputs lists, sometimes not. All of these slow comprehension through [extraneous cognitive load](https://thedecisionlab.com/reference-guide/psychology/cognitive-load-theory).
- **Anchoring bias:** A single recommendation anchors on that option, and missing null options anchor on "fixing what ain't broke".
- **Usability:** Answering by Q number takes lookups, scrolling, and typing. Good alternative suggestions show up inconsistently.

## Benefits
In addition to solving the above challenges, this variant adds a few additional benefits (and personally amusing grilling metaphors):
- **Fast heating:** Explore, generate, rescope, and decide options with hotkeys.
- **Pause any time:** Defer questions and stop/restart when convenient.
- **Perfectly cooked:** Stay laser-focused on key decisions with visible context paths.
- **Serves groups:** Maintain shared context in meetings with [IBIS notation](https://en.wikipedia.org/wiki/Issue-based_information_system) \[1].
- **Easy cleanup:** Store concise decision traces in specs, ADRs, and other decision records.

1. IBIS was designed to maintain shared group understanding when solving wicked problems like "What should we do about climate change?". I've used it to keep meetings of 2-30 attendees on track and productive.

## Tradeoffs
One benefit of free-form paragraphs is that they support intermingling decision traces with supporting data visualizations like images and tables. If you prefer mixing alternate data formats with your decision traces, semantic decision trees like IBIS will feel awkward. I prefer separating the decision traces from their supporting resources with a references section, so free-form paragraphs vs. decision trees don't matter.


## ⚖️ Differences from Grill-me

| Feature | Original Project | This Project |
| :--- | :--- | :--- |
| **Directed Focus** | Many at once | One at a time |
| **Context Structure** | Unstructured design tree | Semantically structured issue tree |
| **Context Presentation** | Unstructured paragraphs | logic paths + relevant context colocated when needed |
| **Context Location** | Scattered across split paragraphs | Paired with question |
| **Context Finding** | Asking, remembering Q#s + scrolling + reading, ctrl+f in session history | scanning latest response |
| **Suggestions** | Inconsistent, unstructured, unrecorded | Consistent, structured, automatically suggested then confirmed and recorded |
| **Assumptions** | thinking + manual typing, unrecorded | Consistent, structured, automatically suggested then confirmed and recorded |
| **Responding** | "Q#" references + typing | Hotkeys |
| **Usage Contexts** | Individual | Individual, Group, Decision Records |
| **Logical Conflict Resolution** | - | automated detection, suggestion, and hotkeyed resolution |
| **Pausing** | — | Defer questions, stop and resume |

## 📜 Credits
- Inspired by [@mattpocock](https://github.com/mattpocock)'s [grill-me skill](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md).

## 📄 License
MIT © Adam Laughlin
