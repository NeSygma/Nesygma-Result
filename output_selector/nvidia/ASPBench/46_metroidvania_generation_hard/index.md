# Benchmark Report (SELECTOR): ASPBench - 46_metroidvania_generation_hard

**Provider:** nvidia
**Model:** nvidia/nemotron-3-nano-30b-a3b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: high
**Duration:** 9.06s


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

- We need to rank solvers suitability for this problem. The problem is designing a game world with constraints, combinatorial placement, connectivity, special types, item prerequisites, etc. It involves placement of items, assignment of special room types, connections with requires fields, constraints about one-way edges, etc. It's a planning / combinatorial design problem with many discrete choices, constraints, possibly counting, ordering, etc. It seems like a classic CSP / planning / scheduling problem with constraints, possibly requiring search over discrete assignments. It involves numeric constraints? Not really numeric counting bounds except maybe number of connections (10-15). That's a cardinality constraint but can be expressed as bounds. It also involves ordering constraints: Goal must be last new room reachable; all other rooms must be reachable before Goal. That's a reachability ordering constraint.
- Which solver is best? Let's examine each:
- - VAMPIRE: Automated theorem prover for first-order logic, open-world, good for entailment, quantifiers, but not for combinatorial search or planning. It can handle logical constraints but not easily encode large combinatorial search or generate models. It is more for proving statements, not for finding a model that satisfies many constraints. It could potentially handle the logical constraints, but the problem is to find any valid solution (a model). Vampire is not a model finder; it's a theorem prover. It could be used to prove unsatisfiability, but not to search for a solution. So not ideal.
- - CLINGO: Answer Set Programming, good for combinatorial search, planning, constraints, generate models. It can handle constraints like item placement, special types, connections, one-way edges, etc. It can encode the problem as ASP with rules, choice rules for generating connections, integrity constraints to enforce conditions, etc. It can find a model (valid solution). It works under closed-world assumption, but can simulate constraints. It can handle cardinality constraints (#count) for number of connections (10-15). It can handle special room types assignment, item location constraints, equipment cannot be placed in its type room, etc. It can handle the one-way connection requirement and the bidirectional key constraints. It can handle reachability and ordering constraints perhaps via additional predicates and maybe use #minimize or #maximize or use constraints on ordering. It can also handle the requirement that Goal must be last new room reachable; that may need some ordering or path constraints, but can be encoded using reachable predicates and a "last" condition. ASP can handle such planning problems. So Clingo seems very suitable.
- - Z3: SMT solver, can handle arithmetic, booleans, integer variables, etc. It can also handle combinatorial constraints, but may struggle with large numbers of discrete variables? It can handle them but may need to encode as booleans. It can handle the constraints, but the problem includes many disjunctive constraints and possibly requires modeling of graph connectivity and reachability, which can be expressed with transitive closure, but that may be heavy. However Z3 can handle it with proper encoding. It can also test options? The problem does not have multiple-choice options; it's just find any valid solution. Z3 can find a model. It can handle cardinality constraints via arithmetic. It can handle the one-way edges and key constraints. It can handle the requirement that Goal must be last reachable; that may need a reachable predicate and ordering; can be encoded with additional variables. Z3 can also handle it.
- Between Clingo and Z3, which is more suitable? The problem is essentially a planning / combinatorial design with many constraints, but also includes a requirement about ordering of reachability (Goal must be last new room). That's a kind of planning constraint that may be easier in ASP with stable models and default reasoning. ASP is designed for such combinatorial problems. Z3 is more generic but may require more complex encoding for reachability (transitive closure). However Z3 can also handle it.
- The question: "Rank ALL three solvers from most suitable to least suitable for this problem regardless of its difficulty." So we need to rank them. Likely Clingo is most suitable, then Z3, then Vampire. Or maybe Z3 is more suitable than Clingo? Let's think.
- Clingo is specifically for combinatorial search, planning, answer set programming. It can handle constraints like "exactly one one-way connection" and "10-15 bidirectional connections". It can handle choice rules to generate connections. It can handle integrity constraints for key constraints. It can handle the requirement that Goal must be last reachable; can be encoded using a "reachability" predicate and a "last" condition maybe using a linear order or a "max" condition. It can also handle the special room types assignment.
- Z3 can also handle these constraints but may need to encode the graph as adjacency matrix with boolean variables, and then define reachability via transitive closure (maybe using recursion). Z3 can handle recursion via fixed-point? It can but may be more complex. However Z3 can also handle cardinality constraints via arithmetic. It can handle the "exactly one one-way connection" and "two one-way edges total" constraints. It can handle the "Goal must be last reachable" maybe using a topological ordering variable.
- But the problem also includes "special room types: one Flooded and one Chasm" and "equipment cannot be placed in a room of the type it enables". That's a simple constraint.
- Thus both Clingo and Z3 are suitable. Which is more suitable? The problem is essentially a planning / combinatorial design with many discrete choices and constraints, but also includes some ordering and reachability constraints that may be more naturally expressed in ASP. ASP is designed for such problems and can handle them elegantly with stable models and default reasoning. Z3 is more generic but may require more manual encoding. However the question likely expects that Clingo is most suitable because it's about combinatorial search and planning, while Z3 is more for constraints with arithmetic and SAT, but still can handle. Vampire is least suitable.
- Thus ranking: ["CLINGO", "Z3", "VAMPIRE"].
- But we must be careful: The problem also includes "multiple-choice options"? No, there are no options given. It's just find any valid solution. So Z3's strength in multiple-choice might be less relevant. But Z3 can still find a model.
- Thus ranking: Clingo most suitable, Z3 second, Vampire least.
- Thus output JSON: {"solver_ranking": ["CLINGO","Z3","VAMPIRE"]}
- We must ensure we only output JSON, no extra text.


{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}

### TOKEN USAGE

  Input tokens:  1,989
  Output tokens: 1,411
  Total tokens:  3,400

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}
```
