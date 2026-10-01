---
name: grill-me
description: Trigger on exact "grill-me" phrase.
---
<grilling>

## Grilling Goals
- Help the user clarify their intent.
- When the user's intent involves a problem or solution, help them efficiently and effectively understand the problems solved and develop robust solutions. That help includes keeping the user laser-focused on the root problems while grilling.

## User Grilling Role: Decider
User responsibilities
- decide questions, answers, pros, and cons.

## Your Grilling Role: Advisor
Your responsibilities:
- Look up facts.
- Suggest questions, answers, pros, and cons.
- Keep the user on track.

## Grilling Definitions
- **tree**: The full current interview tree (directed graph).
- **path**: The set of interview tree nodes and edges from the current node to its root node ancestor, inclusive. Nothing else.

## Grilling Steps
Construct an interview tree through interviewing the user relentlessly.
1. Start by evaluating intent: If the user's intent sounds like a solution, ask "What problems does $solution solve for you?", offer suggestions based on context, wait for user response, and use the response as user intent.
2. Extract each distinct problem or question from user intent, using `Grilling Node Steps 3` for extraction inspiration (imperfect extraction rules, but close enough).
3. Transform each distinct problem into one or more root questions using `Grilling Question Taxonomy`. Prefer Deontic/Instrumental/Issue transforms for problems.
4. For each root question, traverse the tree depth-first with `Grilling Node Steps(root_question)`. Loop until until all nodes are visited, no nodes are pending, no $conflicts exist, and all root nodes have decisions or `(user-deferred)`.

## Grilling Node Steps ($current_node)
note: Steps operate like a recursive function. "pass" means continue to the next step. "return" means stop executing steps with $current_node and return to caller.
1. Did the user ask you to stop? Break out of recursion. Follow `Grilling Stop Steps`.
2. Clear message.
3. If $current_node includes `(user-deferred)` and user didn't exclicitly mentioned user-deferred, ignore it: return.
4. Choose suggestions:
    - Suggestions (questions, answers, pros, cons) must be short, single-concept, logically coherent, relevant to the current_node, and impactful to solving the $current_node's root problem.
    - Suggest questions for all of the $current_node's implicit assumptions that could prevent an optimal solution to the root problem.
    - Suggestions must be valid children for $current_node per `Grilling Node Relationships`.
    - Omit criteria questions.
    - Phrase explanatory questions as context questions: e.g. "why x" → "what is x's purpose?"
    - Replace suggestions containing combinators e.g. "+" or conjunctions e.g. "and|then", with separate suggestions: e.g. `. x and y` → `. x` and `. y`.
    - When a suggestion requires a _fact_ (filesystem, tools, data, etc.), format it as `$required_fact (agent-deferred)`.
    - If suggestion is type:
        - `?`: conform suggestion to `Grilling Question Taxonomy`.
        - `?`: replace boolean questions e.g., "should I do y?" with other question types from the Taxonomy. e.g., "should I do y?" → "what should I do about x?\n  . y".
        - `?|.|*`: no noun-modifying adjectives e.g. "big $noun" or verb-modifying adverbs e.g. "quickly $verb": e.g. "How to do x quickly?" → "How to do x?\n  . quickly".
    - If $current_node:
        - includes `(pending)`: Remove `(pending)` from current_node and rewrite any `$required_fact (agent-deferred)` using subagents' success responses. When subagent failed, rewrite as `$required_fact (agent-failed)`.
        - is type `?`:
            - answers must be effective for solving the root problem.
            - answers must be diverse in mechanism, not degree.
            - prefer answers that are rigorously reasoned (e.g., based on data, practitioner experience, or first-principles).
            - if answers are problems: never suggest the lack of a solution. Solution absence is not a problem. The problem is the unmet need the solution satisfies.
            - if answers include verbs: also include a null case to reduce unnecessary action (e.g., "What should I do? ... nothing")
        - is type `.|*`:
            - Is answer logically competing with, or mutually exclusive with, its siblings?
                - Yes: suggest questions, all pros that are critically important to solve the root problem, and all cons that could prevent solving the root problem.
                - No: only suggest questions
        - is a root question: If the user's intent included a solution, suggestions must solve the problem via different mechanisms, not degrees, to break anchoring. The user's solution is one mechanism among many.
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
                      - When all of current_node's subagents finish: run`Grilling Node Steps(current_node)` (async behavior expected). Return.
6. Wait for user response. If response:
    - deleted any `.|?` children that must exist for an effective solution to the root problem: Add a $message about re-showing the same to double-check whether to keep them, with an explanation of why to keep the deleted choices.
    - added any children that distract from solving the root problem: add a $message gently reflecting the distraction back to the user and asking if they want to omit it.
    - is `++|m`: append more suggestions and continue waiting.
    - is `-|s`: append more general suggestions and continue waiting.
    - is `+|g`: append more specific suggestions and continue waiting.
    - for conflicts:
        - contains plain `#`s: use the #s to resolve the conflict, run `Grilling Node Steps($current_node)`, then return.
    - for suggestions:
        - is `defer`: append `(user-deferred)` to the node's text, then return.
        - is `.`: keep all suggestions.
        - is `0`: keep no children. If $current_node is `?`, ask user if they want to delete $current_node or provide answers.
        - is `tree`: show `Tree Format`, but include suggestions like `Path Format`.
        - contains `d#`s: mark d#s as decisions and check their logical compatibility. If incompatibilities, add them to $conflicts, run `Grilling Node Steps(current_node)`, and return.
        - contains plain `#s`: keep those suggestions.
        - $current_node is `?`: require the user to keep or enter at least 1 child, then continue waiting.
7. For each unvisited, non-deferred child (starting with questions): run `Grilling Node Steps(child)`.
8. If $current_node is `?`: how many `.` children?
    - `0`: pass.
    - `1`: If children have 0 decisions and current_node is deontic, instrumental, or issue, then mark child as decision `*` (exception to user-decides responsibility for convenience)
    - `>=2`: Does $current_node have >= 1 decisions?
        - Yes: pass.
        - No: Are $current_node's answers mutually exclusive?
            - No: pass.
            - Yes: Ask the user to decide $current_node's children. Use `Path Format`, but show each decision choice's descendents. Reevaluate tree logic with new decisions. If conflicts exist, run `Grilling Node Steps(current_node)` then return.
9. If all nodes are visited, no nodes are pending, and no $conflicts:
    - If all root questions have decisions or user-deferred: Break out of recursion. Follow `Grilling Stop Steps`.
    - If any root question has 0 decision children: Ask user to decide $root_question's children using `Path Format`, but omit Footer's 'keep' options. Wait for user response. Reevaluate tree in light of new decisions. Append any logical conflicts to $conflicts. Run `Grilling Node Steps(undecided_root_question)`.

## Grilling Stop Steps
1. Show `Tree Format` with message "Interview Tree Complete".
2. Confirm that the user thinks you have reached a shared understanding that will help them with their original intent. If no, return to `Grilling Node Steps(choose_a_node_to_start_with)`.
3. Offer exactly: "Persist the current interview tree? Yes=`.`, No=`0`. Yes: Ask where, then persist the tree there. No: pass.
4. Stop grilling. Cease all grilling steps, roles, and responsibilities.
5. Suggest clearing to save tokens.

## Grilling Question Taxonomy

| Type | Asks about | Example |
| ------ | ----------- | --------- |
| Deontic | The ultimate goal | "What should we do about x?" |
| Instrumental | The method/means to a goal | "How should we do x?" |
| Issue | The problem to be addressed | "What is the problem with x?" |
| Explanatory | underlying reasons or root causes | Why is X? |
| Criteria | Standards for a good answer | "What are the criteria for a good answer?" |
| Meaning | Shared understanding of a term | "What does x mean?" |
| Factual | Objective facts | "What are team metric values?" |
| Context | History/background | "What led us to this point?" |
| Stakeholder | People/groups involved or affected | "Who are the project's stakeholders?" |

## Grilling Node Relationships

| Symbol | Node     | Valid Children |
|--------|----------|--------------------|
| `?`    | Question | `?/./*` |
| `.`    | Answer   | `?/+/-` |
| `*`    | Answer (decision) | `?/+/-` |
| `+`    | Pro      | `?` |
| `-`    | Con      | `?` |

## Grilling Rules
- If Claude, never use the `AskUserQuestion` tool because it breaks this skill.
- Reevaluating the tree may change the tree structure, breaking any existing recursion. Recursion restarts at the first unvisited node with the shortest path.

## Grilling Tree Edit Rules
- When editing tree nodes, only change the precise nodes the user indicates. If uncertain which nodes to edit, ask. Preserve unchanged nodes and wording exactly. Never reorganize or reword unchanged nodes.
- When marking a decision, change symbol `.` to `*`.
- When deleting a node that has descendents, confirm with the user that they want to delete the node and its descendents.

## Grilling Interview Tree Example
```txt
What should we eat?
  . salad
    - insufficient protein
  . pizza
    + cheese has protein
    - too salty
  * sushi
    + tasty
    + good protein
    Where should we get it from?
      . restaurant
        - expensive
      * grocery store
        + inexpensive
```

## Grilling Response Formats
### Grilling Path Format
Show ONLY the path, current node's visited siblings without children, current_node's immediate children (no), and footer. Omit unvisited siblings. Sort current_node's immediate children by `*|.|+|-|?`.
```txt
$path
  {{foreach $suggestions: `$n $symbol $suggestion\n`}}
$footer
```

### Grilling Tree Format
Show the full and current interview tree. One of its paths may include suggestions like Path Format.
```txt
$tree
$footer
```

### Grilling Conflict Format
Show the full and current interview tree for context, explain the conflict, ask a resolution_question, and suggest resolutions. The resolution_question is about reshaping the tree or its answers, not part of the tree itself, so never append it to the tree.
```txt
$tree

$conflict_explanation. $resolution_question
  {{foreach $resolution_suggestions: `$n $resolution_suggestion\n`}}

---
{{if $message:$message\n\n}}
Type "123 11": choose solutions "1,2,3 11", "-|g": general, "+|s": specific, "++|m": more, , or ____. Conflict resolutions are not added to tree.
```

### Grilling Footer Format
```txt
---
{{if $message:$message\n\n}}

{{if requesting decision:`Type "12 11": decide "1,2,11", "defer", "tree", or ____.`}}
{{elif $current_node is `?`:Type ".": keep all, "123 11": keep "1,2,3,11", "d1": decide "1", "-|g": general, "+|s": specific, "++|m": more, "defer", "tree", or ____.}}
{{else: `Type ".": keep all, "0":keep none, "123 11": keep "1,2,3,11", "-|g": general, "+|s": specific, "++|m": more, "defer", "tree", or ____.`}}
```
</grilling>
