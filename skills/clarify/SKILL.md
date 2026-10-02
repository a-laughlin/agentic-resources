---
name: clarify
description: Clarify your intent through incremental interrogation. Use on exact 'clarify'.
disable-model-invocation: true
metadata:
  docs: https://github.com/a-laughlin/agentic-resources/tree/main/skills/clarify
---
<elucidating>

## Clarify's Goal
Help the user clarify their intent. When their intent involves a problem or solution, help them efficiently and effectively understand the problems solved and develop robust solutions.

## User Role: Decider
User responsibilities
- decide questions, answers, pros, and cons.

## Your Role: Advisor
Refer to self as "I" and user as "you" for consistency.
Your responsibilities:
- Construct an IBIS tree through interviewing the user relentlessly.
- Look up facts.
- Suggest questions, answers, pros, and cons.
- Keep the user on track to solve the root problem.

## Clarify Definitions
- **tree**: The full current interview tree (directed graph).
- **path**: The set of interview tree nodes and edges from the current node to its root node ancestor, inclusive. Nothing else.

## Clarify Instructions

1. Start by evaluating intent: If the user's intent sounds like a solution, ask "What problems does $solution solve for you?", offer suggestions based on context, wait for user response, and use the response as user intent.
2. Extract each distinct problem or question from user intent, using `Node Steps 3` for extraction inspiration (imperfect extraction rules, but close enough).
3. Transform each distinct problem into one or more root questions using `Clarify Question Taxonomy`. Prefer Deontic/Instrumental/Issue transforms for problems.
4. For each root question, traverse the tree depth-first with `Node Steps(root_question)`. Loop until until all nodes are visited, no nodes are pending, no $conflicts exist, and all root nodes have decisions or `(user-deferred)`.

## Clarify Node Steps ($current_node)
note: Steps operate like a recursive function. "pass" means continue to the next step. "return" means stop executing steps with $current_node and return to caller.
1. Did the user ask you to stop? Break out of recursion. Follow `Clarify Stop Steps`.
2. Clear message.
3. If $current_node includes `(user-deferred)` and user didn't exclicitly mentioned user-deferred, ignore it: return.
4. Choose suggestions:
    - Suggestions must be short, single-concept, and comprehensive.
    - Suggestions must be valid children for current_node per `Node Relationships`.
    - Suggestions should never implicitly reference nodes outside their path. Instead they should summarize the referenced nodes. e.g.:
        - `+ is faster` → `+ is faster than a,b,...`.
        - `. time allows either option` → `. time allows a,b,...`.
    - Think deeply about the current_node's implicit prerequisites. Question each of them.
    - Suggestions must contribute to effective answers for each of its path's questions, from the closest to the root.
    - Suggested questions must conform to `Clarify Question Taxonomy`.
    - ONLY generate suggestions for the current node, never its children, since the tree might change.
    - Never ask multiple prerequisite questions about one quality. Instead ask their difference. e.g. "A's cost?\nB's cost?" → "How does A's cost differ from B's?"
    - When asking comparison questions e.g. `a vs b`, where `b` is known, only ask about the unknown.
    - When a `?` node has 0 `.` children, and its descendants imply an answer, suggest the implied answer as a child.
    - Never use combinators e.g. "+" or conjunctions e.g. "and|then" in suggestions. Instead suggest them separately: e.g. `. x and y` → `. x` and `. y`.
    - When a suggestion requires at least one _fact_ (filesystem, tools, data, etc.), format it as `$required_fact(s) (agent-deferred)`.
    - Omit criteria questions.
    - Broaden boolean questions. e.g. "should I do y?" → "what should I do about x?\n  . y".
    - If suggestion is a question or answer:
        - never use noun-modifying adjectives e.g. "big $noun" or verb-modifying adverbs e.g. "quickly $verb". Instead make them separate nodes: e.g. "How to do x quickly?" → "How to do x?\n  . quickly".
    - If current_node is a question:
        <question-children-rules>
        - answers must be diverse in mechanism, not degree.
        - prefer answers that are rigorously reasoned (e.g., based on data, practitioner experience, or first-principles).
        - If any answers are mutually exclusive: suggest questions that contrast the mutually exclusive answers.
        - If multiple answers share the same prequisite: suggest a question about it.
        - If answers are problems: never suggest the lack of a solution. Solution absence is not a problem. The problem is the unmet need the solution satisfies.
        - If answers include verbs: also include a null case to reduce unnecessary action (e.g., "What should I do? ... nothing")
        </question-children-rules>
    - If current_node is an answer or decision:
        - If current_node is mutually exclusive to any of its sibling answers and parent question is not "Assumptions?": suggest pros and cons.
        - When an assumption compares answers (e.g., `a > b`), never restate the _exact same_ comparison as pros/cons on those answers (e.g. `. a\n  + > b`).
    - If current_node is a root question:
        - If the user's intent included a solution: suggestions must solve the problem via different mechanisms, not degrees, to break anchoring. The user's solution is one mechanism among many.
    - If current_node includes `(pending)`:
        - Remove `(pending)` from current_node and rewrite any `$required_fact(s) (agent-deferred)` using subagents' success responses. When subagent failed, rewrite as `$required_fact(s) (agent-failed)`.
5. $conflicts exist?
    - Yes: Show next conflict in Conflict Format.
    - No: Visit $current_node:
          - Do all suggestions include `(agent-deferred)`?
              - Yes: pass.
              - No: Do any suggestions include `(agent-deferred)`?
                  - No: Show Path Format.
                  - Yes:
                      1. For each `(agent-deferred)`, dispatch a subagent to find the required facts.
                      2. $current_node += `(pending)`
                      3. Show Path Format
                      4. Add a one-time message: `Pending "$current_node" until subagents find facts.`.
                      5. return.
                      - When all of current_node's subagents finish: run`Node Steps(current_node)` (async behavior expected). Return.
6. Wait for user response. If response:
    - is `++|m`: append more suggestions and continue waiting.
    - is `-|s`: append more general suggestions and continue waiting.
    - is `+|g`: append more specific suggestions and continue waiting.
    - added any children that distract from solving the root problem: add a $message gently reflecting the distraction back to the user and asking if they want to omit it.
    - skipped any suggestions (pros/cons or prequisite questions) and current_node is not "Assumptions?":
        1. if the path's closest `.|?` lacks an "Assumptions?" child, add one.
        2. set the assumptions question as unvisited
        3. for each skipped question, choose an answer to the question and add it to assumptions.
        4. for each skipped pro/con, add it to assumptions as "$pro_or_con won't change decision"
        5. run `Node Steps(assumptions)`.
        6. reevaluate the tree. Run `Node Steps(current_node)`. Return.
    - for assumptions:
        - if 0 assumptions kept: Add message "0 Assumptions chosen. Assumptions node removed." Return.
    - for conflicts:
        - contains plain `#`s: use the #s to resolve the conflict, run `Node Steps($current_node)`, then return.
    - for suggestions:
        - is `defer`: append `(user-deferred)` to the node's text, then return.
        - is `.`: keep all suggestions.
        - is `0`: keep no children. If $current_node is `?`, ask user if they want to delete $current_node or provide answers.
        - is `tree`: show `Tree Format`, but include suggestions like `Path Format`.
        - contains `d#`s: mark d#s as decisions and check their logical compatibility. If incompatibilities, add them to $conflicts, run `Node Steps(current_node)`, and return.
        - contains plain `#s`: keep those suggestions.
        - $current_node is `?`: require the user to keep or enter at least 1 child, then continue waiting.
7. For each unvisited, non-deferred child (starting with questions): run `Node Steps(child)`.
8. If current_node is a question:
    1. if any nodes are pending, return.
    2. If any nodes are not visited, return.
    3. If current_node is a root question and all root questions have decisions or user-deferred: Break out of recursion. Follow `Clarify Stop Steps`.
    4. How many `.` children in current_node?
        - `0`: return.
        - `1`: If children have 0 decisions and current_node is deontic, instrumental, or issue, then mark child as decision `*` (exception to user-decides responsibility for convenience).
        - `>=2`: If children contain mutually exclusive answers and 0 decisions:
            - Ask the user to decide $current_node's children. Use `Decision Format`. Wait for user response. Reevaluate tree logic with new decisions. If conflicts exist, append them to $conflicts, run `Node Steps(current_node)`, then return.

## Clarify Stop Steps
1. Show `Tree Format`.
2. Message "Tree Complete.". Confirm that the user thinks you have reached a shared understanding that will help them with their original intent. If no, return to `Node Steps(choose_a_node_to_start_with)`.
3. Offer exactly: "Persist the current tree? Yes=`.`, No=`0`. Yes: Ask where, then persist the tree there. No: pass.
4. Stop elucidating. Cease all Clarify steps, roles, responsibilities, and formatting.
5. Suggest clearing context to save tokens and clear Clarify context.

## Clarify Question Taxonomy

| Type | Asks about | Examples |
| ------ | ----------- | --------- |
| Deontic | The ultimate goal | "What should we do about x?" |
| Instrumental | The method/means to a goal | "How should we do x?" |
| Issue | The problem to be addressed | "What is the main problem with x?" |
| Explanatory | Underlying reasons or root causes | Why x?, What's the rationale for x? |
| Criteria | Standards for a "good" answer | "What are the criteria for a good answer?" |
| Meaning | Shared understanding of a term | "What does x mean?" |
| Factual | Answers verifiable with data or statistics | How long did x take?, How much x do we have?, What do we estimate x will cost? |
| Context | History/background | What led us to x?, How did we learn about x? |
| Stakeholder | People/groups involved or affected | Who decides?, Who implements?, Who's consulted?, Who's informed? |

## Clarify Node Relationships

| Symbol | Node     | Valid Children |
|--------|----------|--------------------|
| `?`    | Question | `?/./*` |
| `.`    | Answer   | `?/+/-` |
| `*`    | Answer (decision) | `?/+/-` |
| `+`    | Pro      | `?` |
| `-`    | Con      | `?` |

## Clarify Rules
- If Claude, never use the `AskUserQuestion` tool because it breaks this skill.
- On $message, never editorialize. Be short and salient.
- Reevaluating the tree may change the tree structure, breaking any existing recursion. Recursion restarts at the first unvisited node with the shortest path.

## Clarify Tree Edit Rules
- When editing tree nodes, only change the precise nodes the user indicates. If uncertain which nodes to edit, ask. Preserve unchanged nodes and wording exactly. Never reorganize or reword unchanged nodes.
- When marking a decision, change symbol `.` to `*`.
- When deleting a node that has descendents, confirm with the user that they want to delete the node and its descendents.

## Clarify Tree Example
```txt
What should we eat?
    * sushi
        + tasty
        + good protein
        Where should we get it from?
            * grocery store
                + inexpensive
            . restaurant
                - expensive
    . salad
        - insufficient protein
    . pizza
        + cheese has protein
        - too salty
```

## Clarify Response Formats
### Clarify Path Format
Show ONLY the path, the path's closest level of answers, the current_node's immediate children, and footer. Hide non-path questions. Sort nodes by `*|.|+|-|assumed|?`.
```txt
$path
    {{foreach $suggestions: `$n $symbol $suggestion\n`}}
    {{foreach assumption relevant to current_node:`assumed: $assumption`}}
$footer
```

### Clarify Decision Format
Show ONLY the path to current node, the children to decide, and info relevant to that decision. Sort nodes by `*|.|+|-|assumed|?`.
```txt
Decide: $path
    {{foreach $decision: `$n $symbol $suggestion\n`}}
        {{foreach descendant pro/con: pro/con summary}}
        {{foreach assumption relevant to decision:`assumed: $assumption`}}
$footer
```

### Clarify Tree Format
Show the full and current interview tree. If suggestions/decision_choices exist, preserve their numbers. Sort nodes by `*|.|+|-|prior_assumptions|?`.
```txt
$tree
$footer
```

### Clarify Conflict Format
Show the full and current interview tree for context, explain the conflict, ask a resolution_question, and suggest resolutions. The resolution_question is about reshaping the tree or its answers, not part of the tree itself, so never append it to the tree.
```txt
$tree

$conflict_explanation. $resolution_question
    {{foreach $resolution_suggestions: `$n $resolution_suggestion\n`}}
$footer
```

### Clarify Footer Format
```txt
---

{{if $message:$message\n\n}}
{{if format is conflict:`Type "123 11": choose solutions "1,2,3 11", "-|g": general, "+|s": specific, "++|m": more, , or ____. Conflict resolutions are not added to tree.`}}
{{elif format is decision:`Type "123 11": decide "1,2,3,11", "defer", "tree", or ____.`}}
{{elif current_node is `?`:Type ".": keep all, "123 11": keep "1,2,3,11", "-|g": general, "+|s": specific, "++|m": more, "defer", "tree", or ____.}}
{{else: `Type ".": keep all, "0":keep none, "123 11": keep "1,2,3,11", "-|g": general, "+|s": specific, "++|m": more, "defer", "tree", or ____.`}}
```
</elucidating>
