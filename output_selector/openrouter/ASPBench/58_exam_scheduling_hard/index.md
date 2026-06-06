# Benchmark Report (SELECTOR): ASPBench - 58_exam_scheduling_hard

**Provider:** openrouter
**Model:** openai/gpt-oss-120b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 7.52s


 SELECTOR META EVALUATOR AGENT

 Query: # Problem Statement

Schedule 8 exams for 6 students across 4 time slots and 3 specialized rooms. Exams have specific room type requirements (e.g., lab exams must be in labs). Find any valid schedule that satisfies all constraints.

## Instance Data

**Exams:** 8 exams, identified as E1 through E8.

**Students:** 6 students (S1 through S6) with the following enrollments:
- S1: E1, E3, E7
- S2: E2, E4, E8
- S3: E1, E5
- S4: E2, E6
- S5: E3, E5, E8
- S6: E4, E6, E7

**Time Slots:** 4 distinct time slots (1, 2, 3, 4).

**Rooms:** 3 rooms with specific types and capacities:
- R1: type classroom, capacity 2
- R2: type classroom, capacity 2
- R3: type lab, capacity 2

**Exam Requirements:** Room type requirements per exam:
- Classroom required: E1, E2, E3, E4, E5, E6
- Lab required: E7, E8

## Constraints

1. **Complete Scheduling:** Every exam must be assigned to exactly one time slot and one room.
2. **Student Conflict:** A student cannot be scheduled for two different exams in the same time slot.
3. **Room Conflict:** A room cannot host more than one exam in the same time slot.
4. **Room Type:** An exam must be scheduled in a room that matches its required type (classroom or lab).
5. **Room Capacity:** The number of students enrolled in an exam cannot exceed the capacity of the room it is assigned to.

## Objective

Find any valid solution that satisfies all constraints.

**Field Descriptions:**
- `status`: String value indicating whether a solution was found ("SATISFIABLE" or "UNSATISFIABLE")
- `schedule`: Array of exam assignments, where each entry contains:
  - `exam`: Exam identifier (E1-E8)
  - `time_slot`: Time slot number (1-4)
  - `room`: Room identifier (R1-R3)


### Thinking

- We need to rank solvers for this problem. The problem is scheduling exams for students across time slots and rooms with constraints: each exam assigned to a time slot and room, student conflict, room conflict, room type, capacity. This is a combinatorial assignment problem with discrete variables (exam -> time slot, room). It involves constraints like capacity (numeric bound) and type matching. This is typical CSP/SMT or ASP. Which solver is most suitable? Let's consider each:
- VAMPIRE: First-order logic theorem prover, open-world, not good for numeric counting bounds, capacity constraints, assignment. Could encode but not ideal. So likely least suitable.
- CLINGO: ASP, good for combinatorial search, closed-world, can handle constraints, capacity via counting aggregates, room type, etc. It is suitable.
- Z3: SMT solver, can handle integer variables for time slots and rooms, capacity constraints, etc. Also suitable. Which is more suitable? Both CLINGO and Z3 can solve. Z3 is good for numeric constraints and assignment; CLINGO is also good for combinatorial scheduling. The problem includes capacity constraints (max 2) and type constraints (rooms have types). Both can handle. However, the problem is essentially a finite domain CSP with small domain (4 slots, 3 rooms, 8 exams). ASP is often used for scheduling puzzles. Z3 also works. Which is more appropriate? The problem includes "room capacity" which is a numeric bound; Z3 handles arithmetic naturally. CLINGO can handle via aggregates (#count) but also fine. The problem does not involve complex arithmetic beyond small integers. Both are okay. The ranking: Most suitable likely CLINGO because it's a classic scheduling CSP with discrete choices and constraints, and ASP is designed for such. Z3 is also suitable but maybe second. VAMPIRE least.
- Thus ranking: ["CLINGO", "Z3", "VAMPIRE"].
- Return JSON.


{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}

### TOKEN USAGE

  Input tokens:  1,712
  Output tokens: 434
  Total tokens:  2,146

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}
```
