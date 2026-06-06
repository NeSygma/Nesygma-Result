from z3 import *

# Problem: 5 nurses, 10 days, 3 shifts per day
# Nurses: 1..5
# Days: 1..10
# Shifts: 1=Morning, 2=Evening, 3=Night

NURSES = 5
DAYS = 10
SHIFTS = 3

# Decision variables: roster[d][s][n] = Bool (True if nurse n+1 works shift s+1 on day d+1)
# Using 0-indexed internally
roster = [[[Bool(f"day_{d+1}_shift_{s+1}_nurse_{n+1}") for n in range(NURSES)] for s in range(SHIFTS)] for d in range(DAYS)]

solver = Solver()

# Constraint 1: Coverage Requirements
# Morning shift (s=0): exactly 2 nurses
# Evening shift (s=1): exactly 1 nurse
# Night shift (s=2): exactly 1 nurse
coverage = [2, 1, 1]
for d in range(DAYS):
    for s in range(SHIFTS):
        solver.add(Sum([If(roster[d][s][n], 1, 0) for n in range(NURSES)]) == coverage[s])

# Constraint 2: Single Assignment per Day - at most one shift per nurse per day
for d in range(DAYS):
    for n in range(NURSES):
        # Sum across shifts for this nurse on this day <= 1
        solver.add(Sum([If(roster[d][s][n], 1, 0) for s in range(SHIFTS)]) <= 1)

# Constraint 3: Rest Period - night shift (s=2) on day d prevents morning shift (s=0) on day d+1
for d in range(DAYS - 1):
    for n in range(NURSES):
        # If nurse n works night shift on day d, then cannot work morning shift on day d+1
        solver.add(Implies(roster[d][2][n], Not(roster[d+1][0][n])))

# Solve
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Valid roster found!")
    print()
    # Print roster in a readable format
    for d in range(DAYS):
        morning = [n+1 for n in range(NURSES) if is_true(m.eval(roster[d][0][n]))]
        evening = [n+1 for n in range(NURSES) if is_true(m.eval(roster[d][1][n]))]
        night = [n+1 for n in range(NURSES) if is_true(m.eval(roster[d][2][n]))]
        print(f"Day {d+1}: Morning={morning}, Evening={evening}, Night={night}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")