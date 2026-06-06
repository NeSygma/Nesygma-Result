# Benchmark Report (SELECTOR): ASPBench - 46_metroidvania_generation_hard

**Provider:** google
**Model:** gemini-3.1-flash-lite-preview
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 7.61s


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

- **Planning the Metroidvania World**
- I'm currently focused on designing a Metroidvania game world. My initial constraints are 12 rooms, with a starting and goal room that do not contain items. I need to place 6 unique items, and design 2 special rooms. Currently, I am focused on the layout of rooms R1-R10 for item placement.
- **Modeling the Environment**
- I've been wrestling with how best to represent the game world's structure, and CLINGO seems like the perfect tool. My constraints, especially regarding item placement, room types, and connection logic, lend themselves well to Answer Set Programming. The "generate-define-test" approach feels like a great fit, and I'm confident I can model reachability using it. I'm focusing on defining the room types, item placement, and graph structure.


The problem requires constructing a valid game world configuration (graph structure, item placement, and room properties) that satisfies complex reachability and progression constraints. This is a classic combinatorial search and constraint satisfaction problem involving graph topology and state-based reachability.

1.  **CLINGO (Answer Set Programming):** This is the most suitable solver. ASP is specifically designed for "generate-define-test" problems where you need to construct a valid configuration (a graph and an assignment) that satisfies a set of logical rules. It handles the reachability constraints (transitive closure) and the "Goal is last" condition naturally using recursive rules. The constraints regarding item placement, room types, and the specific bidirectional/one-way connection rules can be expressed as integrity constraints, making it highly efficient for this type of design problem.

2.  **Z3 (SMT Solver):** Z3 is a strong second choice. It is excellent at handling the numeric and logical constraints (e.g., "exactly 10-15 connections," "exactly one one-way connection"). However, expressing graph reachability and ensuring the "Goal is last" condition in SMT is significantly more cumbersome than in ASP, often requiring unrolling or complex bit-vector/array logic to simulate pathfinding.

3.  **VAMPIRE (Automated Theorem Prover):** Vampire is designed for proving whether a conclusion follows from a set of premises in first-order logic. It is not designed for constructing valid configurations or solving combinatorial search problems. While it could theoretically verify if a *given* configuration is valid, it is not suitable for *finding* a valid configuration from scratch.

{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}

### TOKEN USAGE

  Input tokens:  1,976
  Output tokens: 1,033
  Total tokens:  3,009

COMPLETE

## Selector Final Answer

```json
The problem requires constructing a valid game world configuration (graph structure, item placement, and room properties) that satisfies complex reachability and progression constraints. This is a classic combinatorial search and constraint satisfaction problem involving graph topology and state-based reachability.

1.  **CLINGO (Answer Set Programming):** This is the most suitable solver. ASP is specifically designed for "generate-define-test" problems where you need to construct a valid configuration (a graph and an assignment) that satisfies a set of logical rules. It handles the reachability constraints (transitive closure) and the "Goal is last" condition naturally using recursive rules. The constraints regarding item placement, room types, and the specific bidirectional/one-way connection rules can be expressed as integrity constraints, making it highly efficient for this type of design problem.

2.  **Z3 (SMT Solver):** Z3 is a strong second choice. It is excellent at handling the numeric and logical constraints (e.g., "exactly 10-15 connections," "exactly one one-way connection"). However, expressing graph reachability and ensuring the "Goal is last" condition in SMT is significantly more cumbersome than in ASP, often requiring unrolling or complex bit-vector/array logic to simulate pathfinding.

3.  **VAMPIRE (Automated Theorem Prover):** Vampire is designed for proving whether a conclusion follows from a set of premises in first-order logic. It is not designed for constructing valid configurations or solving combinatorial search problems. While it could theoretically verify if a *given* configuration is valid, it is not suitable for *finding* a valid configuration from scratch.

{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}
```
