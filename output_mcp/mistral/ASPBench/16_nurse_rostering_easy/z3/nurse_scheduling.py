from z3 import *

# Create optimizer for minimization
opt = Optimize()

# Parameters
num_nurses = 4
num_days = 7
num_shifts = 3

# Shift types: 0=morning (2 nurses), 1=evening (1 nurse), 2=night (1 nurse)
coverage_required = [2, 1, 1]

# Decision variables: roster[d][s][n] = True if nurse n assigned to shift s on day d
# Using 0-indexed nurses internally, will convert to 1-indexed in output
roster = [[[Bool(f'roster_{d}_{s}_{n}') for n in range(num_nurses)] for s in range(num_shifts)] for d in range(num_days)]

# Hard constraints

# 1. Coverage requirement: Each shift must have exactly the required number of nurses
for d in range(num_days):
    for s in range(num_shifts):
        opt.add(Sum([roster[d][s][n] for n in range(num_nurses)]) == coverage_required[s])

# 2. Single assignment: A nurse can work at most one shift per day
for d in range(num_days):
    for n in range(num_nurses):
        opt.add(Sum([roster[d][s][n] for s in range(num_shifts)]) <= 1)

# 3. Rest period: Nurse cannot work night shift (shift 2) then morning shift (shift 0) next day
for d in range(num_days - 1):
    for n in range(num_nurses):
        opt.add(Implies(roster[d][2][n], Not(roster[d+1][0][n])))

# Soft constraints (violations to minimize)

# 4. Max consecutive days: Count violations where a nurse works > 3 consecutive days
# Track consecutive days for each nurse
consec = [[Int(f'consec_{d}_{n}') for n in range(num_nurses)] for d in range(num_days)]

# Base case: day 0
for n in range(num_nurses):
    works_day0 = Sum([roster[0][s][n] for s in range(num_shifts)])
    opt.add(consec[0][n] == If(works_day0 > 0, 1, 0))

# Recurrence: for days 1-6
for d in range(1, num_days):
    for n in range(num_nurses):
        works_day = Sum([roster[d][s][n] for s in range(num_shifts)])
        opt.add(consec[d][n] == If(works_day > 0, consec[d-1][n] + 1, 0))

# Count violations: each day where consec[d][n] > 3 adds 1 violation
consec_violations = Sum([If(consec[d][n] > 3, 1, 0) for d in range(num_days) for n in range(num_nurses)])

# 5. Fair distribution: Each nurse should work 6-8 shifts
# Total shifts per nurse
total_shifts = [Int(f'total_shifts_{n}') for n in range(num_nurses)]
for n in range(num_nurses):
    opt.add(total_shifts[n] == Sum([roster[d][s][n] for d in range(num_days) for s in range(num_shifts)]))
    # Violation if < 6 or > 8

fair_violations = Sum([If(Or(total_shifts[n] < 6, total_shifts[n] > 8), 1, 0) for n in range(num_nurses)])

# 6. Weekend coverage: At least 2 different nurses must work weekend shifts (days 6-7, 0-indexed 5-6)
weekend_nurse = [Bool(f'weekend_nurse_{n}') for n in range(num_nurses)]
for n in range(num_nurses):
    # Nurse works weekend if assigned to any shift on day 5 or 6
    works_weekend = Or([roster[d][s][n] for d in [5, 6] for s in range(num_shifts)])
    opt.add(weekend_nurse[n] == works_weekend)

weekend_count = Sum([If(weekend_nurse[n], 1, 0) for n in range(num_nurses)])
weekend_violations = If(weekend_count < 2, 1, 0)

# Total violations
total_violations = consec_violations + fair_violations + weekend_violations

# Objective: Minimize total violations
opt.minimize(total_violations)

# Check if there's a solution
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract roster
    print("roster = [")
    for d in range(num_days):
        print(f"  [  # Day {d+1}")
        for s in range(num_shifts):
            shift_name = ['morning', 'evening', 'night'][s]
            assigned_nurse = None
            for n in range(num_nurses):
                if is_true(model[roster[d][s][n]]):
                    assigned_nurse = n + 1  # Convert to 1-indexed
                    break
            print(f"    ['{shift_name}', {assigned_nurse}],  # Shift {s+1}")
        print("  ],")
    print("]")
    
    # Extract violations
    consec_viol = model.eval(consec_violations)
    fair_viol = model.eval(fair_violations)
    weekend_viol = model.eval(weekend_violations)
    total_viol = model.eval(total_violations)
    
    print(f"violations = {total_viol}")
    print(f"  - consecutive_days_violations = {consec_viol}")
    print(f"  - fair_distribution_violations = {fair_viol}")
    print(f"  - weekend_coverage_violations = {weekend_viol}")
    
    # Check coverage_met (should be True due to hard constraints)
    coverage_met = True
    print(f"coverage_met = {coverage_met}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat")
else:
    print("STATUS: unknown")