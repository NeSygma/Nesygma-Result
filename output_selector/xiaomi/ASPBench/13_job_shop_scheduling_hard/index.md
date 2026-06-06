# Benchmark Report (SELECTOR): ASPBench - 13_job_shop_scheduling_hard

**Provider:** xiaomi
**Model:** mimo-v2.5-pro
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 4.56s


 SELECTOR META EVALUATOR AGENT

 Query: # Problem Statement

Schedule 4 jobs, each with a sequence of 3-4 operations, on 4 machines. The goal is to minimize a combined cost function of makespan and tardiness penalties, while respecting machine maintenance windows, specialized operator constraints, and job precedence requirements.

## Instance Data

### Jobs and Operations

**Job 1 (Due: 20, Penalty Weight: 3):** 3 operations
- Operation 1: Duration 4, Machine 1
- Operation 2: Duration 5, Machine 3, Requires Master Operator
- Operation 3: Duration 3, Machine 2

**Job 2 (Due: 25, Penalty Weight: 1):** 4 operations
- Operation 1: Duration 6, Machine 2
- Operation 2: Duration 4, Machine 4
- Operation 3: Duration 2, Machine 1
- Operation 4: Duration 3, Machine 3

**Job 3 (Due: 22, Penalty Weight: 2):** 3 operations
- Operation 1: Duration 7, Machine 4, Requires Master Operator
- Operation 2: Duration 6, Machine 1
- Operation 3: Duration 2, Machine 3

**Job 4 (Due: 30, Penalty Weight: 1):** 4 operations
- Operation 1: Duration 2, Machine 3
- Operation 2: Duration 5, Machine 2
- Operation 3: Duration 3, Machine 4
- Operation 4: Duration 4, Machine 1, Requires Master Operator

### Machine Maintenance Windows

- **Machine 2:** Unavailable from time 10 to 11 (inclusive)
- **Machine 4:** Unavailable from time 15 to 16 (inclusive)

Operations cannot be in progress during these maintenance windows on the respective machines.

### Time Horizon

Maximum time horizon: 40 time units

## Constraints

1. **Precedence:** Operations within each job must be performed sequentially in order.
2. **Machine Exclusivity:** Each machine can process at most one operation at a time.
3. **Master Operator Exclusivity:** At most one operation requiring the Master Operator can be in progress at any time.
4. **Maintenance:** No operation can be running on a machine during its maintenance window.
5. **Non-preemptive:** Once started, operations cannot be interrupted.

## Objective

Find a solution that **minimizes** the total cost, where `Total Cost = Makespan + Total Weighted Tardiness Penalty`.

- **Makespan:** The completion time of the last operation in the entire schedule
- **Total Weighted Tardiness Penalty:** The sum of penalties for all jobs, where `Penalty(job) = max(0, FinishTime - DueDate) * PenaltyWeight`

**Expected optimal makespan:** 24

### Field Descriptions

- **schedule:** Array of operation assignments, each with job number, operation number, assigned machine, start time, and duration
- **metrics:** Object containing makespan (latest completion time), total_penalty (sum of weighted tardiness), and total_cost (makespan + total_penalty)
- **job_completion:** Array of job completion information with finish time, due date, and tardiness for each job
- **feasible:** Boolean indicating whether the solution is feasible

{
    "solver_ranking": ["Z3", "CLINGO", "VAMPIRE"]
}

### TOKEN USAGE

  Input tokens:  1,903
  Output tokens: 24
  Total tokens:  1,927

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["Z3", "CLINGO", "VAMPIRE"]
}
```
