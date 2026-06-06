from z3 import *

# Parameters
num_nurses = 5
num_days = 10
shifts = [1,2,3]  # 1: morning, 2: evening, 3: night
required = {1:2, 2:1, 3:1}

# Variables: assign[day][nurse] = shift (0 = none, 1..3 actual)
assign = [[Int(f"a_{d}_{n}") for n in range(num_nurses)] for d in range(num_days)]
solver = Solver()

# Domain constraints
for d in range(num_days):
    for n in range(num_nurses):
        solver.add(assign[d][n] >= 0, assign[d][n] <= 3)

# Coverage constraints per day and shift
for d in range(num_days):
    for s in shifts:
        cnt = Sum([If(assign[d][n] == s, 1, 0) for n in range(num_nurses)])
        solver.add(cnt == required[s])

# Single assignment per day is already enforced by domain (0..3) and coverage ensures exactly required numbers, but a nurse could be assigned to multiple shifts if we allowed >0 multiple? Actually each nurse variable is single value, so at most one shift.
# Rest constraint: night (3) cannot be followed by morning (1)
for n in range(num_nurses):
    for d in range(num_days-1):
        solver.add(Implies(assign[d][n] == 3, assign[d+1][n] != 1))

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    # Build roster structure
    roster = []
    for d in range(num_days):
        day_shifts = []
        for s in shifts:
            nurses = []
            for n in range(num_nurses):
                if m.eval(assign[d][n]).as_long() == s:
                    nurses.append(n+1)  # IDs are 1-based
            day_shifts.append(nurses)
        roster.append(day_shifts)
    print("STATUS: sat")
    print("roster =", roster)
else:
    print("STATUS: unsat")