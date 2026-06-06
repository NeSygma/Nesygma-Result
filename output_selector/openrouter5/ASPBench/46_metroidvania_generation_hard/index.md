# Benchmark Report (SELECTOR): ASPBench - 46_metroidvania_generation_hard

**Provider:** openrouter5
**Model:** deepseek/deepseek-v4-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 7.56s


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

Based on the problem structure, here is my analysis:

**Problem Type Analysis:**
- This is a **combinatorial design/configuration problem** with discrete assignments (rooms, items, special types, connections)
- It requires **constructing a valid world** (not just checking entailment or answering true/false)
- There are **strict constraints** with **conditional dependencies** (item prerequisites, traversal rules, reachability)
- The problem involves **graph construction** with **bidirectional and one-way edges**, **key requirements**, and **special room types**
- There is **no numeric counting bounds** or **positional ordering** in the traditional sense (like slots 1–12)
- The constraints are **logical and structural**, not arithmetic
- The goal is to **find a valid configuration** (a single solution), not to enumerate all or optimize

**Solver Suitability:**

1. **CLINGO** is most suitable because:
   - It excels at **combinatorial search** over discrete domains (rooms, items, types)
   - It supports **generate-define-test** methodology perfect for constructing a graph with constraints
   - It handles **conditional dependencies** (item prerequisites, traversal rules) naturally via rules
   - It can model **reachability** (transitive closure) and **graph properties** (incoming/outgoing edges)
   - It works under **closed-world assumption** which fits this design problem
   - It can enforce **integrity constraints** (e.g., no item in Start/Goal, special types only in R1–R10)

2. **Z3** is second choice because:
   - It can handle **constraint satisfaction** with Boolean and integer variables
   - However, the problem lacks **numeric/positional structure** that Z3 handles best
   - Reachability and graph construction are less natural in SMT than in ASP
   - The constraints are more **logical/relational** than arithmetic

3. **VAMPIRE** is least suitable because:
   - It is designed for **entailment checking** (true/false/uncertain), not **constructing configurations**
   - It works under **open-world assumption**, which is inappropriate for a design problem where everything must be fully specified
   - It cannot generate a graph or assign items; it can only verify logical consequences of given premises
   - The problem asks for a **solution**, not a proof of a hypothesis

```json
{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}
```

### TOKEN USAGE

  Input tokens:  1,952
  Output tokens: 537
  Total tokens:  2,489

COMPLETE

## Selector Final Answer

```json
Based on the problem structure, here is my analysis:

**Problem Type Analysis:**
- This is a **combinatorial design/configuration problem** with discrete assignments (rooms, items, special types, connections)
- It requires **constructing a valid world** (not just checking entailment or answering true/false)
- There are **strict constraints** with **conditional dependencies** (item prerequisites, traversal rules, reachability)
- The problem involves **graph construction** with **bidirectional and one-way edges**, **key requirements**, and **special room types**
- There is **no numeric counting bounds** or **positional ordering** in the traditional sense (like slots 1–12)
- The constraints are **logical and structural**, not arithmetic
- The goal is to **find a valid configuration** (a single solution), not to enumerate all or optimize

**Solver Suitability:**

1. **CLINGO** is most suitable because:
   - It excels at **combinatorial search** over discrete domains (rooms, items, types)
   - It supports **generate-define-test** methodology perfect for constructing a graph with constraints
   - It handles **conditional dependencies** (item prerequisites, traversal rules) naturally via rules
   - It can model **reachability** (transitive closure) and **graph properties** (incoming/outgoing edges)
   - It works under **closed-world assumption** which fits this design problem
   - It can enforce **integrity constraints** (e.g., no item in Start/Goal, special types only in R1–R10)

2. **Z3** is second choice because:
   - It can handle **constraint satisfaction** with Boolean and integer variables
   - However, the problem lacks **numeric/positional structure** that Z3 handles best
   - Reachability and graph construction are less natural in SMT than in ASP
   - The constraints are more **logical/relational** than arithmetic

3. **VAMPIRE** is least suitable because:
   - It is designed for **entailment checking** (true/false/uncertain), not **constructing configurations**
   - It works under **open-world assumption**, which is inappropriate for a design problem where everything must be fully specified
   - It cannot generate a graph or assign items; it can only verify logical consequences of given premises
   - The problem asks for a **solution**, not a proof of a hypothesis

```json
{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}
```
```
