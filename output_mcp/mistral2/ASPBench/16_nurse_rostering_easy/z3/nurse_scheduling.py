from z3 import *

# Problem size
NUM_NURSES = 4
NUM_DAYS = 7
NUM_SHIFTS = 3  # morning, evening, night

# Nurse IDs: 0,1,2,3 (0-indexed for Z3)
# Day IDs: 0..6 (0-indexed for Z3)
# Shift IDs: 0=morning,1=evening,2=night

# Hard constraints:
# - Exactly 2 nurses for morning, 1 for evening, 1 for night per day
# - No nurse works more than one shift per day
# - No nurse works night shift (ends 8am) then morning shift next day (starts 6am) -> 11-hour rest required

# Soft constraints:
# - Max 3 consecutive days per nurse (penalize 4th+)
# - Total shifts per nurse between 6 and 8 (penalize <6 or >8)
# - At least 2 different nurses on weekend shifts (days 5-6, 0-indexed) (penalize if fewer)

# Optimization objective: minimize total soft violations

# Declare solver
opt = Optimize()

# Decision variables: roster[day][shift] = nurse ID (0..3)
roster = [[Int(f"roster_{d}_{s}") for s in range(NUM_SHIFTS)] for d in range(NUM_DAYS)]

# Helper: is nurse n assigned to day d?
assigned = [[Bool(f"assigned_{d}_{n}") for n in range(NUM_NURSES)] for d in range(NUM_DAYS)]

# Helper: is nurse n working shift s on day d?
working = [[[Bool(f"working_{d}_{s}_{n}") for n in range(NUM_NURSES)] for s in range(NUM_SHIFTS)] for d in range(NUM_DAYS)]

# Consecutive working days per nurse (to enforce max 3)
consecutive = [[Int(f"consecutive_{d}_{n}") for n in range(NUM_NURSES)] for d in range(NUM_DAYS)]

# Total shifts per nurse
shifts_total = [Int(f"shifts_total_{n}") for n in range(NUM_NURSES)]

# Weekend nurses set (days 5-6, shifts 0,1,2)
weekend_nurses = [Bool(f"weekend_nurse_{n}") for n in range(NUM_NURSES)]

# Hard constraint: each shift must have exactly the required number of nurses
# Morning: 2, Evening: 1, Night: 1
for d in range(NUM_DAYS):
    # Morning shift (shift 0): exactly 2 nurses
    opt.add(Sum([working[d][0][n] for n in range(NUM_NURSES)]) == 2)
    # Evening shift (shift 1): exactly 1 nurse
    opt.add(Sum([working[d][1][n] for n in range(NUM_NURSES)]) == 1)
    # Night shift (shift 2): exactly 1 nurse
    opt.add(Sum([working[d][2][n] for n in range(NUM_NURSES)]) == 1)

# Hard constraint: no nurse works more than one shift per day
for d in range(NUM_DAYS):
    for n in range(NUM_NURSES):
        opt.add(Sum([working[d][s][n] for s in range(NUM_SHIFTS)]) <= 1)

# Hard constraint: no nurse works night shift then morning shift next day (11-hour rest)
for d in range(NUM_DAYS - 1):
    for n in range(NUM_NURSES):
        # If nurse n works night shift on day d, they cannot work morning shift on day d+1
        opt.add(Implies(working[d][2][n], Not(working[d+1][0][n])))

# Link roster variables to working variables
for d in range(NUM_DAYS):
    for s in range(NUM_SHIFTS):
        for n in range(NUM_NURSES):
            opt.add(working[d][s][n] == (roster[d][s] == n))

# Link assigned variables
for d in range(NUM_DAYS):
    for n in range(NUM_NURSES):
        opt.add(assigned[d][n] == Or([working[d][s][n] for s in range(NUM_SHIFTS)]))

# Compute consecutive working days per nurse
# Base case: day 0
for n in range(NUM_NURSES):
    opt.add(consecutive[0][n] == If(assigned[0][n], 1, 0))

# Inductive case: for d > 0
for d in range(1, NUM_DAYS):
    for n in range(NUM_NURSES):
        # If nurse n worked on day d-1 and day d, increment consecutive count
        # Else, reset to 1 if worked on day d, else 0
        opt.add(consecutive[d][n] == 
                If(And(assigned[d-1][n], assigned[d][n]), 
                   consecutive[d-1][n] + 1,
                   If(assigned[d][n], 1, 0)))

# Compute total shifts per nurse
for n in range(NUM_NURSES):
    opt.add(shifts_total[n] == Sum([If(assigned[d][n], 1, 0) for d in range(NUM_DAYS)]))

# Soft constraint: max 3 consecutive days per nurse (penalize 4th+)
consecutive_violations = [Int(f"consecutive_violations_{n}") for n in range(NUM_NURSES)]
for n in range(NUM_NURSES):
    # For each day, if consecutive[n][d] >= 4, add 1 violation
    violations = []
    for d in range(NUM_DAYS):
        violations.append(If(consecutive[d][n] >= 4, 1, 0))
    opt.add(consecutive_violations[n] == Sum(violations))

# Soft constraint: total shifts per nurse between 6 and 8 (penalize <6 or >8)
shift_violations = [Int(f"shift_violations_{n}") for n in range(NUM_NURSES)]
for n in range(NUM_NURSES):
    opt.add(shift_violations[n] == 
            If(shifts_total[n] < 6, 6 - shifts_total[n], 
               If(shifts_total[n] > 8, shifts_total[n] - 8, 0)))

# Soft constraint: at least 2 different nurses on weekend shifts (days 5-6)
# Mark which nurses work any shift on weekend
for n in range(NUM_NURSES):
    opt.add(weekend_nurses[n] == Or([assigned[d][n] for d in [5,6]]))  # days 5-6 are indices for days 6-7

# Count number of distinct nurses working weekend
weekend_nurse_count = Sum([If(weekend_nurses[n], 1, 0) for n in range(NUM_NURSES)])
weekend_violations = If(weekend_nurse_count < 2, 1, 0)

# Total soft violations
total_violations = Sum(consecutive_violations) + Sum(shift_violations) + weekend_violations
opt.minimize(total_violations)

# Hard constraint: all shifts must be assigned (no invalid nurse IDs)
for d in range(NUM_DAYS):
    for s in range(NUM_SHIFTS):
        opt.add(roster[d][s] >= 0)
        opt.add(roster[d][s] < NUM_NURSES)

# Check if coverage requirements are satisfied (hard constraints)
coverage_met = True  # We enforce these via hard constraints, so it's always true in feasible solutions

# BENCHMARK_MODE: ON (problem is guaranteed solvable)
BENCHMARK_MODE = True

# Check and print result
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    # Extract roster
    roster_vals = [[model.eval(roster[d][s]) for s in range(NUM_SHIFTS)] for d in range(NUM_DAYS)]
    print("roster =")
    for d in range(NUM_DAYS):
        print([model.eval(roster[d][s]) for s in range(NUM_SHIFTS)])
    
    # Extract violations
    violations = model.eval(total_violations).as_long()
    print(f"violations = {violations}")
    print(f"coverage_met = True")
    print(f"Expected optimal violations: 16")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")