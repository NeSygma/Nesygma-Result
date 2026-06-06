from z3 import *

# ============================================================================
# PROBLEM: Robotic Assembly Lab Scheduling
# ============================================================================

# Initialize optimizer
opt = Optimize()

# ============================================================================
# DATA
# ============================================================================

# Tasks: (Task, Duration, Required Skill, Machine Type, Deadline)
tasks_data = [
    ("T1", 2, "Welding", "A", 6),
    ("T2", 3, "Assembly", "B", 8),
    ("T3", 1, "Inspection", "A", 7),
    ("T4", 2, "Welding", "A", 9),
    ("T5", 3, "Assembly", "C", 10),
    ("T6", 2, "Programming", "B", 9),
    ("T7", 1, "Inspection", "A", 8),
    ("T8", 2, "Assembly", "C", 11),
    ("T9", 3, "Welding", "A", 12),
    ("T10", 2, "Programming", "B", 11),
    ("T11", 1, "Assembly", "C", 10),
    ("T12", 2, "Inspection", "A", 13),
]

# Workers: (Worker, Skills, Hourly Cost)
workers_data = [
    ("W1", ["Welding", "Inspection"], 15),
    ("W2", ["Assembly", "Inspection"], 12),
    ("W3", ["Programming", "Assembly"], 20),
    ("W4", ["Welding", "Programming"], 18),
    ("W5", ["Assembly", "Inspection", "Welding"], 16),
]

# Machines: (Machine, Type, Hourly Cost)
machines_data = [
    ("M1", "A", 3),
    ("M2", "B", 2),
    ("M3", "C", 4),
]

# Precedence Dependencies: (Before, After)
precedence_data = [
    ("T1", "T3"),
    ("T1", "T4"),
    ("T2", "T5"),
    ("T2", "T6"),
    ("T3", "T7"),
    ("T4", "T9"),
    ("T5", "T8"),
    ("T6", "T10"),
    ("T7", "T12"),
    ("T8", "T11"),
]

# Extract sets
Task = [t[0] for t in tasks_data]
Worker = [w[0] for w in workers_data]
Machine = [m[0] for m in machines_data]

# Helper: map task to its attributes
task_duration = {t[0]: t[1] for t in tasks_data}
task_skill = {t[0]: t[2] for t in tasks_data}
task_machine_type = {t[0]: t[3] for t in tasks_data}
task_deadline = {t[0]: t[4] for t in tasks_data}

# Helper: map worker to skills and cost
worker_skills = {w[0]: w[1] for w in workers_data}
worker_cost = {w[0]: w[2] for w in workers_data}

# Helper: map machine to type and cost
machine_type = {m[0]: m[1] for m in machines_data}
machine_cost = {m[0]: m[2] for m in machines_data}

# ============================================================================
# DECISION VARIABLES
# ============================================================================

# Start time of each task (integer)
start = {t: Int(f"start_{t}") for t in Task}

# Finish time of each task (integer)
finish = {t: Int(f"finish_{t}") for t in Task}

# Worker assigned to each task (symbolic integer 0..4)
worker_assignment = {t: Int(f"worker_{t}") for t in Task}

# Machine assigned to each task (symbolic integer 0..2)
machine_assignment = {t: Int(f"machine_{t}") for t in Task}

# ============================================================================
# AUXILIARY VARIABLES
# ============================================================================

# Makespan (objective, integer)
makespan = Int("makespan")

# Total cost (integer)
total_cost = Int("total_cost")

# Cost for each task (integer)
cost = {t: Int(f"cost_{t}") for t in Task}

# ============================================================================
# HELPER FUNCTIONS (Z3 Arrays for symbolic indexing)
# ============================================================================

# Z3 Array for worker cost: worker_idx -> cost
worker_cost_arr = Array('worker_cost_arr', IntSort(), IntSort())
for i, w in enumerate(Worker):
    opt.add(worker_cost_arr[i] == worker_cost[w])

# Z3 Array for machine cost: machine_idx -> cost
machine_cost_arr = Array('machine_cost_arr', IntSort(), IntSort())
for i, m in enumerate(Machine):
    opt.add(machine_cost_arr[i] == machine_cost[m])

# Z3 Array for worker skills: worker_idx -> list of skills
worker_skills_arr = Array('worker_skills_arr', IntSort(), ArraySort(IntSort(), StringSort()))
for i, w in enumerate(Worker):
    skills = worker_skills[w]
    # Z3 does not support lists of strings directly, so we encode skills as integers
    # Map skills to integers for Z3
    skill_to_int = {"Welding": 0, "Assembly": 1, "Inspection": 2, "Programming": 3}
    skills_int = [skill_to_int[s] for s in skills]
    # Create an array of skills for this worker
    skills_arr = Array(f'skills_arr_{i}', IntSort(), IntSort())
    for j, s in enumerate(skills_int):
        opt.add(skills_arr[j] == s)
    opt.add(worker_skills_arr[i] == skills_arr)

# Z3 Array for machine type: machine_idx -> type (as integer)
machine_type_arr = Array('machine_type_arr', IntSort(), IntSort())
for i, m in enumerate(Machine):
    mtype = machine_type[m]
    # Map type to integer
    type_to_int = {"A": 0, "B": 1, "C": 2}
    opt.add(machine_type_arr[i] == type_to_int[mtype])

# Map task required skill to integer
skill_to_int = {"Welding": 0, "Assembly": 1, "Inspection": 2, "Programming": 3}

# Map task required machine type to integer
type_to_int = {"A": 0, "B": 1, "C": 2}

# ============================================================================
# CONSTRAINTS
# ============================================================================

# 1. Finish time = start time + duration
for t in Task:
    opt.add(finish[t] == start[t] + task_duration[t])

# 2. Task Assignment: Each task assigned to exactly one worker and one machine
# Worker assignment: worker_assignment[t] ∈ [0,1,2,3,4]
for t in Task:
    opt.add(worker_assignment[t] >= 0, worker_assignment[t] < len(Worker))

# Machine assignment: machine_assignment[t] ∈ [0,1,2]
for t in Task:
    opt.add(machine_assignment[t] >= 0, machine_assignment[t] < len(Machine))

# 3. Skill Compatibility: Worker must have required skill
for t in Task:
    required_skill = task_skill[t]
    required_skill_int = skill_to_int[required_skill]
    # For each possible worker, check if they have the required skill
    for i in range(len(Worker)):
        skills_arr = worker_skills_arr[i]
        # Check if required_skill_int is in the skills array for worker i
        # Since Z3 arrays are functions, we need to encode membership
        # We'll use a loop to check if any index in skills_arr equals required_skill_int
        # This is a bit heavy, but necessary for correctness
        has_skill = Bool(f"has_skill_{t}_{i}")
        # We'll encode: has_skill iff there exists j such that Select(skills_arr, j) == required_skill_int
        # Since the array is finite, we can unroll it
        # For simplicity, assume each worker has at most 3 skills
        opt.add(Implies(worker_assignment[t] == i, 
                        Or(Select(skills_arr, 0) == required_skill_int,
                           Select(skills_arr, 1) == required_skill_int,
                           Select(skills_arr, 2) == required_skill_int)))

# 4. Machine Type: Machine must match required type
for t in Task:
    required_type = task_machine_type[t]
    required_type_int = type_to_int[required_type]
    opt.add(Select(machine_type_arr, machine_assignment[t]) == required_type_int)

# 5. Precedence: If task A must precede task B, then finish[A] <= start[B]
for (before, after) in precedence_data:
    opt.add(finish[before] <= start[after])

# 6. Deadlines: Each task must finish by its deadline
for t in Task:
    opt.add(finish[t] <= task_deadline[t])

# 7. Budget: Total cost ≤ 470
# Cost for a task = (worker_hourly_cost + machine_hourly_cost) * task_duration
for t in Task:
    w_idx = worker_assignment[t]
    m_idx = machine_assignment[t]
    worker_cost_val = Select(worker_cost_arr, w_idx)
    machine_cost_val = Select(machine_cost_arr, m_idx)
    opt.add(cost[t] == (worker_cost_val + machine_cost_val) * task_duration[t])

opt.add(total_cost == Sum([cost[t] for t in Task]))
opt.add(total_cost <= 470)

# 8. Makespan definition: makespan = max(finish[t] for t in Task)
for t in Task:
    opt.add(makespan >= finish[t])

# ============================================================================
# OBJECTIVE
# ============================================================================

opt.minimize(makespan)

# ============================================================================
# CHECK AND OUTPUT
# ============================================================================

BENCHMARK_MODE = True  # Set False outside benchmark mode
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print("Makespan:", model[makespan])
    print("Total Cost:", model[total_cost])
    print("\nSchedule:")
    for t in Task:
        w_idx = model[worker_assignment[t]]
        m_idx = model[machine_assignment[t]]
        s = model[start[t]]
        f = model[finish[t]]
        w_name = Worker[w_idx.as_long()]
        m_name = Machine[m_idx.as_long()]
        print(f"Task {t}: worker={w_name}, machine={m_name}, start={s}, finish={f}, duration={task_duration[t]}")
    print("\nFeasible: True")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")