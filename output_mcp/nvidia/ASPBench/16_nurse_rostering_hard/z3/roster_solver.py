from z3 import *

solver = Solver()
BENCHMARK_MODE = True

# Create variables for each day (1-10)
morning1 = {}
morning2 = {}
evening = {}
night = {}
for d in range(1, 11):
    morning1[d] = Int(f"m1_{d}")
    morning2[d] = Int(f"m2_{d}")
    evening[d] = Int(f"e_{d}")
    night[d] = Int(f"n_{d}")

    # domain constraints
    solver.add(morning1[d] >= 1, morning1[d] <= 5)
    solver.add(morning2[d] >= 1, morning2[d] <= 5)
    solver.add(evening[d] >= 1, evening[d] <= 5)
    solver.add(night[d] >= 1, night[d] <= 5)

    # all-different across the four shift slots for the day
    solver.add(Distinct(morning1[d], morning2[d], evening[d], night[d]))

    # rest period: night shift on day d cannot be followed by morning shift on day d+1
    if d < 10:
        solver.add(night[d] != morning1[d+1])
        solver.add(night[d] != morning2[d+1])

# Check satisfiability
result = solver.check()

if result == sat:
    print("STATUS: sat")
    model = solver.model()
    # Output the roster
    for d in range(1, 11):
        m1 = model.evaluate(morning1[d])
        m2 = model.evaluate(morning2[d])
        e = model.evaluate(evening[d])
        n = model.evaluate(night[d])
        print(f"day{d}_morning = [{m1}, {m2}]")
        print(f"day{d}_evening = [{e}]")
        print(f"day{d}_night = [{n}]")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")