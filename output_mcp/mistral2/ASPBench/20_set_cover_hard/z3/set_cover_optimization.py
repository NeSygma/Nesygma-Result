from z3 import *

# Universe and sets
universe = list(range(1, 21))

# Set definitions: (elements, cost, category)
sets = [
    ({1, 2, 3, 4, 5}, 1, "A"),
    ({1, 6, 11, 16}, 1, "A"),
    ({2, 7, 12, 17}, 1, "A"),
    ({3, 8, 13, 18}, 1, "B"),
    ({4, 9, 14, 19}, 1, "B"),
    ({5, 10, 15, 20}, 1, "B"),
    ({6, 7, 8, 9, 10}, 1, "C"),
    ({1, 3, 5, 7, 9}, 1, "C"),
    ({2, 4, 6, 8, 10}, 1, "C"),
    ({1, 2, 3, 4, 5, 6, 7}, 4, "specialized"),
    ({11, 12, 13, 14, 15}, 4, "specialized"),
    ({8, 9, 10}, 4, "specialized"),
    ({1, 5, 10, 15}, 4, "specialized"),
    ({16, 17, 18, 19, 20}, 4, "specialized"),
]

# Initialize optimizer
opt = Optimize()

# Decision variables: whether each set is selected
selected = [Bool(f"selected_{i}") for i in range(len(sets))]

# Base cost: sum of costs of selected sets
base_cost = Sum([If(selected[i], sets[i][1], 0) for i in range(len(sets))])

# Coverage: for each element, count how many selected sets cover it
covered = [Bool(f"covered_{e}") for e in universe]
overcovered = [Bool(f"overcovered_{e}") for e in universe]

# For each element, count the number of selected sets that cover it
for e in universe:
    # Count the number of selected sets that include e
    count = Sum([If(And(selected[i], e in sets[i][0]), 1, 0) for i in range(len(sets))])
    # If count > 0, element is covered
    opt.add(covered[e-1] == (count > 0))
    # If count > 3, element is overcovered
    opt.add(overcovered[e-1] == (count > 3))

# Full coverage: all elements must be covered
for e in universe:
    opt.add(covered[e-1])

# Prerequisites
# Set 9 requires Set 0
opt.add(Implies(selected[9], selected[0]))
# Set 11 requires Set 6
opt.add(Implies(selected[11], selected[6]))

# Mutual exclusion: Set 12 and Set 13 cannot both be selected
opt.add(Not(And(selected[12], selected[13])))

# Category balancing: if any specialized set is selected, ensure at least one set from A, B, and C is selected
specialized_sets = [i for i in range(len(sets)) if sets[i][1] > 1]
standard_A = [i for i in range(len(sets)) if sets[i][2] == "A"]
standard_B = [i for i in range(len(sets)) if sets[i][2] == "B"]
standard_C = [i for i in range(len(sets)) if sets[i][2] == "C"]

# If any specialized set is selected, at least one from A, B, and C must be selected
if specialized_sets:
    any_specialized = Or([selected[i] for i in specialized_sets])
    at_least_one_A = Or([selected[i] for i in standard_A])
    at_least_one_B = Or([selected[i] for i in standard_B])
    at_least_one_C = Or([selected[i] for i in standard_C])
    opt.add(Implies(any_specialized, And(at_least_one_A, at_least_one_B, at_least_one_C)))

# Redundancy penalty: 2 for each overcovered element
redundancy_penalty = Sum([If(overcovered[e-1], 2, 0) for e in universe])

# Total cost
total_cost = base_cost + redundancy_penalty

# Objective: minimize total cost
opt.minimize(total_cost)

# Check and print result
BENCHMARK_MODE = True  # Set False outside benchmark mode
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print("Total cost:", model.eval(total_cost))
    print("Base cost:", model.eval(base_cost))
    print("Redundancy penalty:", model.eval(redundancy_penalty))
    print("Selected sets:", [i for i in range(len(sets)) if is_true(model[selected[i]])])
    print("Covered elements:", [e for e in universe if is_true(model[covered[e-1]])])
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")