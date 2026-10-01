# grill-me

> **A Claude Code skill that interviews you until your intent is clear and your decisions coherent.** Inspired by Matt Pocock's [grill-me skill](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md).

## 💡 Why This Exists
I encountered a few challenges using the original:
* **Scannability:** Paragraphs of free-form text are slow to scan, and options buried in inline lists are slow to comprehend.
* **Traceability:** Untyped options go unrecorded, leaving no trace for decision records and specs.
* **Shareability:** The linear Q# format and spacing are too verbose and indirect for practical usage in decision records and specs.
* **Understandability:** Questions paragraphs mix options, pros, cons, and sub-questions inconsistently, slowing reasoning about the tree. The linear+batch format obscures tree relationships. Question batches overflow the visible window and require scrolling. "Q#" indexes + batching require remembering numbers and mixing them with typed concepts. All of these introduce preventable, [extraneous cognitive load](https://thedecisionlab.com/reference-guide/psychology/cognitive-load-theory).
* **Anchoring bias:** A single recommendation anchors on that option, and missing null options anchor on "fixing what ain't broke".
* **Usability:** Answering by Q number takes lookups and typing. Good alternative suggestions show up inconsistently.

In addition to solving the above, this variant adds additional benefits (and grilling metaphors):
* **Fast heating:** Explore, generate, rescope, and decide options with hotkeys.
* **Pause any time:** Defer questions and stop/restart when convenient.
* **Perfectly cooked:** Stay laser-focused on key decisions with visible context paths.
* **Serves groups:** Maintain shared context in meetings with [IBIS notation](https://en.wikipedia.org/wiki/Issue-based_information_system) \[1].
* **Easy cleanup:** Store concise, intuitive decision traces in specs, ADRs, and other decision records.

1. IBIS was designed to maintain shared group understanding when solving wicked problems like "What should we do about climate change?". I've used it to keep meetings of 2-30 attendees on track and productive.

## ⚖️ Key differences

| Feature | Original Project | This Project |
| :--- | :--- | :--- |
| **Visual Format** | Linear, free-form paragraphs | Tree, scannable separate concepts |
| **Structure** | indirect, hidden, unstructured design tree | direct, visible, semantically-structured issue tree |
| **Suggestions** | Inconsistent, single, unrecorded | Consistent, multiple, explored suggestions recorded |
| **Responding** | "Q#" references + remembering + typing | Hotkeys |
| **Usage Scenario** | Individual | Individual + Group |
| **Logical Conflict Resolution** | - | automated detection and one-key suggested resolutions |
| **Pausing** | — | Defer questions, stop and resume |

## 🚀 Quick Start
### Installation
```txt
TBD (just copy it for now)
```

### Usage (in terminal)
```txt
grill-me <your problem or idea>
```


## Example

Notation: `?` question, `.` answer, `+` pro, `-` con, `*` decision.

Here's one grilling session with Opus 5.5. Completed without leaving the number pad:
```txt
> grill-me about dinner

What should we do about dinner?
  1 . cook at home
  2 . eat at a restaurant
  3 . eat leftovers
  4 . nothing (don't eat)
  5 ? What's the occasion?
  6 ? What ingredients do we have at home?
  7 ? How much more does a restaurant meal cost than cooking?
  8 ? What leftovers do we have at home?

Type ".": keep all, "123 11": keep "1,2,3,11", "d1": decide "1", "-|g": more general, "+|s": more specific, "++|m": more, "defer", "tree", or ____.
```

Choosing questions, answers, pros, and cons builds the tree. The path back to the root question remains visible for both human and LLM context.

```txt
What should we do about dinner?
  . eat at a restaurant
    - costs more
      ? How much more does a restaurant meal cost than cooking?
        1 . ~$24–30 more per person (~5.5–7x), US average: home ~$5–6, restaurant ~$30–35 incl. tax and tip

Type ".": keep all, "123 11": keep "1,2,3,11", "d1": decide "1", "-|g": more general, "+|s": more specific, "++|m": more, "defer", "tree", or ____.
```

Here's tree after exploring all chosen questions and making decisions. To get it, I kept some suggested answers, pros, and cons, skipped multiple questions about assumptions made by them, kept the "How much more?" suggestion, and kept a web-researched answer on relative cost. All without leaving the number pad.

```txt
What should we do about dinner?
  . cook at home
    + costs less
    - takes prep time
    - requires cleanup
  * eat at a restaurant
    + no prep time
    + no cleanup
    - requires travel
    - costs more
      ? How much more does a restaurant meal cost than cooking?
        . ~$24–30 more per person (~5.5–7x), US average: home ~$5–6, restaurant ~$30–35 incl. tax and tip
```


## 📜 Credits
* Inspired by [@mattpocock](https://github.com/mattpocock)'s [grill-me skill](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md).
* Notation from [IBIS (Issue-Based Information System)](https://en.wikipedia.org/wiki/Issue-based_information_system).

## 📄 License
MIT © Adam Laughlin
