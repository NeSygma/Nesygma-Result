# Benchmark Report (SELECTOR): ASPBench - 46_metroidvania_generation_hard

**Provider:** openrouter6
**Model:** xiaomi/mimo-v2-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: high
**Duration:** 16.85s


 SELECTOR META EVALUATOR AGENT

 Query: # Problem Statement

Design a complete, valid Metroidvania-style game world with complex mechanics. The level must be fully solvable without soft-locks and must satisfy advanced design constraints including special room types, item-based traversal abilities, one-way paths, and item acquisition prerequisites.

## Instance Data

**Rooms:** 12 fixed rooms: `Start`, `R1`, `R2`, `R3`, `R4`, `R5`, `R6`, `R7`, `R8`, `R9`, `R10`, `Goal`.

**Items:** 6 items to be placed:
- 4 Keys: `RedKey`, `BlueKey`, `GreenKey`, `YellowKey`
- 2 Equipment: `Boots` (for flooded rooms), `Grapple` (for chasms)

**Special Room Types:** Two rooms from `R1-R10` must be assigned special types: one `Flooded` and one `Chasm`.

## Constraints

1. **Item Placement:** All 6 items must be placed in rooms `R1-R10`. The `Start` and `Goal` rooms cannot contain items or have special types.
2. **Connections:** The level graph must have 10-15 bidirectional connections and exactly one one-way connection **(this is in addition to the mandatory one-way path to the `Goal` room, for a total of two one-way edges in the final graph)**. For each pair of rooms connected bidirectionally, if any connection in one direction requires a key, there **must exist** at least one connection in the return direction that is keyless (`requires: null`). The `Goal` room must have exactly one incoming connection and no outgoing connections.

   **Example:**
   ```json
   // VALID: A key-required path has a corresponding keyless return path.
   {"from": "R1", "to": "R2", "requires": "RedKey"},
   {"from": "R2", "to": "R1", "requires": null}

   // INVALID: A key-required path's return path also requires a key.
   {"from": "R3", "to": "R4", "requires": "BlueKey"},
   {"from": "R4", "to": "R3", "requires": "GreenKey"}
   ```
3. **Traversal Rules:**
   - Key-locked doors require the corresponding key
   - To **enter** a `Flooded` room, player must possess `Boots`
   - To **enter** a `Chasm` room, player must possess `Grapple`
   - An equipment item cannot be placed in a room of the type it enables (e.g., `Boots` cannot be in the `Flooded` room)
4. **Item Prerequisites:** The `YellowKey` must be located in the `Chasm` room, creating a hard dependency: player must acquire `Grapple` before acquiring `YellowKey`.
5. **Reachability & Progression:**
   - All 12 rooms must be reachable from `Start`
   - The `Goal` room must be the **last** new room the player can reach. All other 11 rooms must be accessible before the path to `Goal` is open.

## Objective

Find any valid solution that satisfies all constraints.

**Field Descriptions:**
- `special_room_types`: Object mapping special type names to room names
- `item_locations`: Object mapping item names to room names
- `connections`: Array of connection objects, each with `from`, `to`, and `requires` fields
- `solution_validity`: Object with boolean flags for reachability and goal timing


### Thinking

- First, the user has given me a problem about designing a Metroidvania-style game world. I need to analyze this problem and rank the three solvers: VAMPIRE, CLINGO, and Z3 from most suitable to least suitable. I must not solve the problem, only analyze its type and structure.
- Key elements from the problem:
- - It's a design problem: find a valid configuration for rooms, items, connections, etc.
- - Constraints involve:
- - Placing items in specific rooms.
- - Assigning special room types (Flooded and Chasm).
- - Defining connections with bidirectional and one-way rules.
- - Traversal rules based on items.
- - Item prerequisites (YellowKey in Chasm room).
- - Reachability and progression constraints.
- - The output should be specific fields: special_room_types, item_locations, connections, solution_validity.
- Now, I need to match this to the solvers:
- 1. **VAMPIRE (Automated Theorem Prover - First-Order Logic)**:
- - Best for entailment checks, True/False/Uncertain, yes/no questions.
- - Handles universal and existential quantifiers, predicates, logical connectives.
- - Open-world assumption: anything not asserted is unknown.
- - Not ideal for numeric counting bounds, entity-to-position assignment, or explicit integer arithmetic.
- - Typical problems: categorical reasoning, property inheritance, logical entailments.
- - This problem is about constructing a valid configuration, not checking entailment. It's a search for a solution, not a proof of validity from premises. So, VAMPIRE might not be suitable.
- 2. **CLINGO (Answer Set Programming - Logic Programming)**:
- - Best for constructed configurations, enumeration of valid states, planning problems.
- - Closed-world assumption: anything not stated is false.
- - Features: facts, rules, integrity constraints, choice rules, aggregates.
- - Typical problems: logic puzzles, graph coloring, action planning, combinatorial search.
- - This problem involves finding a valid arrangement of rooms, items, connections under constraints. It sounds like a combinatorial search problem with rules, which CLINGO is designed for.
- 3. **Z3 (SMT Solver - Satisfiability Modulo Theories)**:
- - Best for constraint satisfaction, entity-to-slot scheduling, numeric bounds, ordering.
- - Handles Boolean, integer, real variables, arithmetic constraints, optimization.
- - Typical problems: scheduling, allocation, ordering under constraints.
- - This problem has constraints like "10-15 bidirectional connections", "exactly one one-way connection", which involve counting and bounds. Also, entity placement (items to rooms) and ordering (reachability).
- Now, analyze the problem structure:
- - It's a configuration problem: assign items to rooms, assign special types, define connections.
- - Constraints include:
- - Numeric bounds: 10-15 bidirectional connections, exactly one one-way (plus mandatory one to Goal, so total two one-way).
- - Conditional constraints: if a connection requires a key, return must be keyless.
- - Traversal rules based on items.
- - Prerequisites: YellowKey in Chasm room.
- - Reachability: all rooms reachable from Start, Goal last.
- This involves:
- - Discrete entities: rooms, items.
- - Relations: connections between rooms.
- - Constraints on counts and conditions.
- CLINGO is good for logic programming with rules and constraints, especially for combinatorial search. It can handle choice rules for placing items and defining connections, and integrity constraints to ensure validity.
- Z3 is good for constraint satisfaction with numeric bounds and ordering. It can handle the connection count constraints and reachability as logical constraints.
- VAMPIRE is for theorem proving, which is more about verifying entailment rather than constructing solutions. This problem is about finding a solution, not proving a statement from premises.
- The problem says "Find any valid solution", which is a construction task, not an entailment check.
- So, CLINGO and Z3 are both suitable, but I need to rank them.
- Consider the specific constraints:
- - "10-15 bidirectional connections" – this is a numeric bound, which Z3 handles well with integer variables and constraints.
- - "exactly one one-way connection" – similar.
- - Connections have conditions (requires key or null).
- - Item placement with prerequisites.
- CLINGO can handle this with rules and aggregates, but Z3 might be more straightforward for numeric constraints.
- However, CLINGO is designed for answer set programming, which is ideal for problems with multiple choices and constraints, like logic puzzles. This problem resembles a logic puzzle with rooms and items.
- Z3 is more for SMT, which can handle arithmetic and logical constraints together.
- But note: the problem involves "reachability" which might require path finding or graph traversal. CLINGO has features for recursive reachability/path finding, while Z3 might need to model it with constraints.
- CLINGO has "recursive reachability/path finding" as a typical problem, so it might be better for the reachability constraint.
- Z3 can model reachability using transitive closure or constraints, but it might be more complex.
- The problem also has "one-way paths" and "item-based traversal abilities", which are graph-related.
- CLINGO is explicitly mentioned for "multi-step action planning" and "graph coloring", so it might be better for graph-based constraints.
- Z3 is for "entity-to-slot scheduling" and "ordering/sequencing", which could apply here.
- But let's see the output: we need to output special_room_types, item_locations, connections, solution_validity. This is a structured output, which both CLINGO and Z3 can generate, but CLINGO might be more natural for logic programming outputs.
- Now, for VAMPIRE: it's for entailment checks, not construction. The problem is not about checking if a conclusion follows from premises; it's about finding a configuration. So, VAMPIRE is least suitable.
- Between CLINGO and Z3:
- - CLINGO: closed-world assumption, which might be fine since we're defining all facts. It handles choice rules for generating solutions, which is perfect for "find any valid solution".
- - Z3: can handle the constraints, but might require more setup for the graph and reachability.
- The problem has "advanced design constraints" including special room types and item prerequisites, which are logical rules. CLINGO is designed for such rule-based systems.
- Also, CLINGO is mentioned for "logic puzzles" and "deductive reasoning", which this resembles.
- Z3 is better for numeric bounds and scheduling, but here the numeric bounds are simple (counts of connections), and the main challenge is the logical constraints.
- Moreover, the problem says "Design a complete, valid Metroidvania-style game world", which is a creative design task, but with strict constraints. CLINGO's generate-define-test methodology is ideal for this.
- Now, for the ranking:
- - Most suitable: CLINGO, because it's designed for combinatorial search with rules and constraints, and this problem is essentially a logic puzzle with rooms and items.
- - Second choice: Z3, because it can handle the numeric constraints and constraint satisfaction, but might be less natural for the graph reachability part.
- - Least suitable: VAMPIRE, as it's for theorem proving, not construction.
- So, ranking: CLINGO, Z3, VAMPIRE.
- But let's confirm if Z3 could be better. The problem has "exactly one one-way connection" which is a precise count, and Z3 is good at that. However, CLINGO can also handle counts with aggregates.
- CLINGO has #count and #sum aggregates, so it can enforce connection counts.
- Also, the reachability constraint: "all rooms reachable from Start" and "Goal last" – CLINGO can model this with path finding rules.
- Z3 might require encoding the graph and using transitive closure, which can be done but might be more complex.
- In practice, for such problems, answer set programming (CLINGO) is often used for puzzle solving, while SMT (Z3) is for more arithmetic-heavy constraints.
- Here, the constraints are mostly logical with some counts, so CLINGO might be more appropriate.
- Finally, the output must be a JSON object with solver_ranking.
- So, I'll go with CLINGO as most suitable, Z3 as second, VAMPIRE as least.


{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}

### TOKEN USAGE

  Input tokens:  1,957
  Output tokens: 1,792
  Total tokens:  3,749

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}
```
