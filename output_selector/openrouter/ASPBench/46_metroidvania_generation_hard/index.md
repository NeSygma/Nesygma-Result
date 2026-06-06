# Benchmark Report (SELECTOR): ASPBench - 46_metroidvania_generation_hard

**Provider:** openrouter
**Model:** openai/gpt-oss-120b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 8.43s


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

- We need to decide which solver is most suitable for this problem. The problem is a design/constraint satisfaction problem: assign items to rooms, assign special types to rooms, create a graph with connections meeting constraints (bidirectional edges with key requirements, one-way edges, reachability, ordering). This is essentially a combinatorial configuration problem with constraints, possibly involving counting (10-15 connections), ordering (Goal last), prerequisites (must have Grapple before YellowKey). This is a classic CSP/SMT problem: assign variables (room types, item locations, edges) subject to constraints, including numeric constraints (number of connections between 10-15). Z3 (SMT) is good for such constraints with integer variables, boolean variables, cardinality constraints, etc. CLINGO (ASP) also could handle combinatorial search with constraints, especially with closed-world assumption and generate/define/test. However, the problem includes numeric counting (10-15 connections) and possibly complex constraints about existence of reverse edges. ASP can handle such constraints using aggregates (#count) and integrity constraints. Both could work. VAMPIRE is for first-order logic entailment, not suitable because this is not entailment but a construction problem.
- Between Z3 and CLINGO, which is more suitable? The problem involves constructing a graph with constraints about existence of reverse edges, one-way edges, reachability ordering. This is a typical planning/graph construction problem; ASP is strong for such combinatorial generation with constraints, especially with reachability (recursive rules). Z3 can also encode reachability via transitive closure but that's more complex. ASP's closed-world and ability to generate candidate edges via choice rules and enforce constraints with integrity constraints is natural. However, the problem also includes numeric counting of edges (10-15) which ASP can handle with #count. So CLINGO seems suitable.
- Z3 could also handle but would require encoding of graph connectivity and reachability, which is more cumbersome. The problem is not primarily arithmetic but combinatorial. So ranking: most suitable CLINGO, second Z3, least VAMPIRE.
- Thus output JSON with ranking: ["CLINGO","Z3","VAMPIRE"]


{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}

### TOKEN USAGE

  Input tokens:  1,998
  Output tokens: 477
  Total tokens:  2,475

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}
```
