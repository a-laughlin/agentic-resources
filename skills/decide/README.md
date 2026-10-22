# Decide

**Decisions: Fast. Thorough. Concise.**

## 💡 Why Decide Exists
While using Matt Pocock's [grill-me skill](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md), I began to notice extraneous cognitive load and other [challenges](#challenges) that slowed me down when reaching a decision. The Decide skill approaches the challenges [differently](#️-differences-from-grill-me), with additional [benefits](#benefits).

The result is 2-4x faster decision speed at similar thoroughness, in a format that's quick to share and read.

## Examples

Notation: `?` question, `.` answer, `+` pro, `-` con, `*` decision.

```txt
> /decide dinner

... 3 minutes and 17 keystrokes later:

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
---
<img src="./decide-example.gif"/>

## Installation
npx skills: `npx skills add https://www.a-laughlin.com/agentic-resources --skill decide -a claude-code -g`\
pnpm: `pnpm dlx skills add https://www.a-laughlin.com/agentic-resources --skill decide -a claude-code -g`\
Claude plugin: `claude plugin marketplace add a-laughlin/agentic-resources` then `claude plugin install decide@agentic-resources`\
gh: `gh skill install a-laughlin/agentic-resources decide`\
curl: `curl -fsSL --create-dirs https://www.a-laughlin.com/agentic-resources/agent-skills/decide/SKILL.md -o ~/.claude/skills/decide/SKILL.md`\
--\
Swap `-a claude-code | ~/.claude/skills` for your agent (e.g.`cursor`, `~/.cursor/skills`, `~/.agents/skills`, …).

## Usage

In your favorite AI chat, `/decide <problems, solutions, questions, ideas, anything...>`

Each response includes shortcuts for fast exploration. For example:
```txt
What should I do for dinner?
    1 . cook at home
    2 . eat at a restaurant
    3 ? Who is eating?
---

Type "123 11": keep "1,2,3,11", "d12": decide "1,2", "e12": explain "1,2", ".": all
     "=[?]": more, "-[?]": more general, "+[?]": more specific, "defer", "tree", or ____.
```

- `12` keeps options #1 and #2 to review pros/cons for before deciding, and assumes an answer for question #3
- `d12` decides options 1,2 (marks them as decisions), and assumes an answer for question #3
- `e12` explains options 1,2 and their pros/cons, to understand unfamiliar options before keeping/deciding
- `.` keeps all options and assumes an answer for question #3
- `0` keeps no option and assumes an answer for question #3
- `=` adds similar options (`=?` adds similar Questions)
- `+` adds more specific options (`+?` adds similar Questions)
- `-` adds more general options (`-?` adds similar Questions)
- `defer` postpones the question to revisit when you choose
- `tree` shows the full tree so far
- `___` type something else

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
In addition to solving the above challenges, Decide adds a few benefits:
- Quickly explore ideas and make decisions with minimal typing.
- Use in meetings to maintain shared context and focus [1](#footnotes).
- Defer questions and stop/restart grilling when convenient.
- Store concise decision traces in specs, ADRs, and other decision records.


## Tradeoffs
One benefit of free-form paragraphs is that they support intermingling decision traces with supporting data visualizations like images and tables. If you prefer mixing alternate data formats with your decision traces, semantic decision trees like IBIS will feel awkward. I prefer separating the decision traces from their supporting resources with a references section, so free-form paragraphs vs. decision trees don't matter.


## ⚖️ Differences from Grill-me

| Aspect | Grill-Me | Decide |
| :--- | :--- | :--- |
| **Focus** | Many questions at once | One question at a time |
| **Context Structure** | Unstructured design tree | Semantically structured issue tree |
| **Context Presentation** | Unstructured paragraphs | logic paths |
| **Context Location** | Spread within and across split paragraphs | Relevant context colocated with latest question |
| **Context Finding** | Asking, remembering Q#s + scrolling + reading, ctrl+f in session history | scanning latest response, "tree" command |
| **Suggestions** | Inconsistent, unstructured | Consistent, structured, automatically suggested then confirmed and recorded |
| **Assumptions** | thinking + manual typing | Consistent, structured, automatically suggested then confirmed and recorded |
| **Responding** | "Q#" references | Hotkeys |
| **Usage Contexts** | Individual | Individual, Meetings, Decision Records, Specs |
| **Logical Conflict Resolution** | - | automated detection, suggestion, and hotkeyed resolution |
| **Pausing** | — | Defer questions, stop and resume |

## Footnotes
1. [IBIS notation](https://en.wikipedia.org/wiki/Issue-based_information_system) was designed to reach fast group decisions on problems as complex as "What should we do about climate change?". I've used it to keep meetings of 2-30 attendees on track and productive.

## 📜 Credits
- Inspired by [@mattpocock](https://github.com/mattpocock)'s [grill-me skill](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md).

## 📄 License
MIT © Adam Laughlin
