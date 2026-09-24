---
name: grill-me
description: Trigger on exact "grill-me" phrase.
# disable-model-invocation: true
---
<!--
inspired by https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md)

previous description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
-->
<grilling>

## Grilling Goal
Help the user achieve their existing goal or intent as you understand it by thinking through it with them.

## Grilling Instructions
Interview the user relentlessly, using the `dialog-map` skill to construct an interview tree. Steps:
1. Suggest a root "should" question to the user based on their current goals or intent. If the user's goal and intent are unclear, suggest "What should my goal(s) be?".
2. Starting at the root node, traverse depth-first through the tree, collaborating with the user to define question, answer, pro, and con sub-nodes as needed.
3. When an answer or pro/con requires a fact from the environment (filesystem, tools, etc.), don't block on it. Instead defer the node, dispatch a sub-agent to find the fact, and continue traversing. When the user's current node is complete and the previous sub-agent has finished, return to the deferred node and resolve it with the new fact.

## Grilling Format
- If the user requests outputting the tree, format it using the `dialog-map` skill.

## Grilling Roles and Responsibilities

### User Grilling Role - Decider
The user's responsibility is:
- decide what answer(s) to each "should" question will best achieve the user's goals

### Your Grilling Role - Advisor
Your responsibilities are:
- ask questions that, left unanswered, could prevent the user from achieving their goals.
- suggest effective and practically comprehensive answers to questions.
- ensure an answer's pros/cons are precise, real-world, stress-tested, and logically consistent with the answer and sibling pros/cons.
- illuminate implicit assumptions and make them explicit
- ensure all nodes' phrasing is as short as possible. Brevity beats grammar.
- find _facts_

## Grilling Completion
1. Is the user's goal or intent clear to you?
2. Have you created an interview tree with the user?
3. Is the interview tree's root node a "should" question?
4. Does the root question have at least one decision answer (`*`)?
5. Have you asked, and the user confirmed, that they have reached a shared understanding with you that will help them achieve their goal or intent?

## Grilling Node Completion
- A "should" question node is complete when it has a decision
- Any other node is complete when no subtree nodes are deferred and you cannot imagine any user-goal-preventing answers, questions, pros, or cons within its subtree.
</grilling>
