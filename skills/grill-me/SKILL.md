---
name: grill-me
description: Trigger on exact "grill-me" phrase.
---
<!--
inspired by https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md)
Its description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.

This version also provides:
- Rabbit hole prevention, scope creep prevention, and existing scope refinement via a clear user-goal focus
- A concise decision output format for ADRs and Specs (upon user request)
- Thorough tree exploration via precise roles and responsibilities
- A <grilling/> wrapper tag and grilling-specific headlines to limit context poisoning

This version also depends on (../dialog-map/SKILL.md).

-->

<grilling>

## Grilling Goal
Help the user achieve their existing goal or intent as you understand it.

## Grilling Instructions
Interview the user relentlessly, using the `dialog-map` skill to construct an interview tree until `## Grilling Completion` or `## Grilling Interruption`.

Steps:
1. Suggest a root "should" question to the user based on their current goals or intent. If the user's goal and intent are unclear to you, suggest "What should my goal(s) be?".
2. Starting at the root node, traverse depth-first through the tree, collaborating with the user to define question, answer, pro, and con sub-nodes as needed.
3. When an answer or pro/con requires a fact from the environment (filesystem, tools, etc.), don't block on it. Instead defer the node, dispatch a sub-agent to find the fact, and continue traversing. When the user's current node is complete and the previous sub-agent has finished, return to the deferred node and resolve it with the new fact.

## Grilling Format
- If the user requests outputting the tree, format it using the `dialog-map` skill.

## Grilling Roles and Responsibilities
Adopt these roles and responsibilities until `## Grilling Completion` or `## Grilling Interruption`.

### User Grilling Role - Decider
While grilling, the user's only responsibility is:
- decide answer(s) to each "should" question.

### Your Grilling Role - Advisor
While grilling, your responsibilities are:
- ask questions that, left unanswered, could prevent the user from achieving their goals.
- provide effective and practically comprehensive answers to each question
- provide any pros/cons that could render an answer ineffective
- ensure pros/cons are precise, real-world, stress-tested, and logically consistent with their parent answer and sibling pros/cons.
- illuminate implicit assumptions as explicit tree nodes
- ensure all nodes' phrasing is as short as possible. Brevity beats grammar.
- find _facts_

## Grilling Interruption
When the user explicitly asks you to stop, pause, or otherwise interrupt grilling:
1. offer to persist the current interview tree as a dialog map.
2. if the user accepts your offer, then persist the tree.
3. stop grilling and cease all grilling roles and responsibilities.
4. suggest clearing context.

## Grilling Completion
1. Is the user's goal or intent clear to you?
2. Have you created an interview tree with the user?
3. Is the interview tree's root node a "should" question?
4. Does the root question have at least one decision answer (`*`)?
5. Have you asked, and the user confirmed, that they have reached a shared understanding with you that will help them achieve their goal or intent?
6. Have you asked the user if they want to output the interview tree (and, if so, outputted it)?

## Grilling Node Completion
- A "should" question node is complete when it has a decision
- Any other node is complete when no subtree nodes are deferred and you cannot imagine any user-goal-preventing answers, questions, pros, or cons within its subtree.

</grilling>
