# Benchmark Report (SELECTOR): ASPBench - 46_metroidvania_generation_hard

**Provider:** openrouter4
**Model:** deepseek/deepseek-v4-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: high
**Duration:** 8.26s


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

- We are asked to analyze the problem and rank the solvers: VAMPIRE, CLINGO, Z3. We must not solve the problem, only analyze the problem type and structure.
- The problem is about designing a Metroidvania game world with rooms, items, connections, special room types, and constraints. It involves combinatorial search: assign special types to rooms, place items in rooms, define connections (bidirectional and one-way) with key requirements, ensure reachability and progression constraints. This is a classic constraint satisfaction and planning problem. The domain is discrete: rooms, items, types, connections. Constraints involve logical conditions (if-then, must have, cannot), numeric bounds (10-15 connections, exactly one one-way etc.), and reachability (graph traversal). This is suitable for Answer Set Programming (Clingo) because it can handle generate-and-test with rules, integrity constraints, and reachability via recursive definitions. Z3 could also handle it as a SAT/SMT problem with graph constraints and reachability, but the problem has a complex structure with nested quantifiers and recursive reachability which is more natural in ASP. VAMPIRE is a first-order logic theorem prover, but this problem is not about entailment of a conclusion from premises; it's about constructing a configuration that satisfies many constraints. VAMPIRE is not suitable for constructing solutions, only for checking validity of a given configuration. So VAMPIRE is least suitable.
- Between Clingo and Z3: Clingo is specifically designed for combinatorial search and planning with closed-world assumption, and it handles recursive definitions (reachability) elegantly. Z3 can also solve such problems using SMT with quantifiers or using fixed-point logic, but it's more cumbersome and may require explicit encoding of reachability as a transitive closure, which is harder. Clingo's ASP is more declarative and natural for such problems. Therefore, Clingo is most suitable, Z3 second, VAMPIRE least.
- Thus ranking: ["CLINGO", "Z3", "VAMPIRE"]


{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}

### TOKEN USAGE

  Input tokens:  1,952
  Output tokens: 450
  Total tokens:  2,402

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}
```
