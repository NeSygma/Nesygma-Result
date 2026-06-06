from z3 import *

# Mapping indices to names
idx_to_name = {0: 'A', 1: 'B', 2: 'C', 3: 'table'}

max_steps = 5  # upper bound for plan length

solution_found = False

for plan_length in range(0, max_steps+1):
    solver = Solver()
    # Variables: loc[block][t] where block 0..2, t 0..plan_length
    loc = [[Int(f'loc_{i}_{t}') for t in range(plan_length+1)] for i in range(3)]
    # Variables: moved[block][t] for t 1..plan_length
    moved = [[Bool(f'moved_{i}_{t}') for t in range(1, plan_length+1)] for i in range(3)]

    # Bounds for locations
    for i in range(3):
        for t in range(plan_length+1):
            solver.add(loc[i][t] >= 0, loc[i][t] <= 3)

    # Initial state
    solver.add(loc[0][0] == 3)  # A on table
    solver.add(loc[1][0] == 3)  # B on table
    solver.add(loc[2][0] == 0)  # C on A

    # Goal state
    solver.add(loc[0][plan_length] == 1)  # A on B
    solver.add(loc[1][plan_length] == 2)  # B on C
    solver.add(loc[2][plan_length] == 3)  # C on table

    # No block on itself
    for i in range(3):
        for t in range(plan_length+1):
            solver.add(loc[i][t] != i)

    # At most one block on top of each block (except table)
    for t in range(plan_length+1):
        for X in range(3):  # blocks A,B,C
            solver.add(Sum([If(loc[Y][t] == X, 1, 0) for Y in range(3)]) <= 1)

    # Moved definition and exactly one block moves per step
    for t in range(1, plan_length+1):
        for i in range(3):
            solver.add(moved[i][t-1] == (loc[i][t] != loc[i][t-1]))
        solver.add(Sum([If(moved[i][t-1], 1, 0) for i in range(3)]) == 1)

    # Clear constraints for moved block and target (ignore table)
    for t in range(1, plan_length+1):
        for i in range(3):
            # block i must be clear before moving
            solver.add(Implies(moved[i][t-1], And([loc[j][t-1] != i for j in range(3) if j != i])))
            # target must be clear before moving if target is a block
            solver.add(Implies(moved[i][t-1] & (loc[i][t] != 3), And([loc[j][t-1] != loc[i][t] for j in range(3) if j != i])))
            # cannot move onto itself
            solver.add(Implies(moved[i][t-1], loc[i][t] != i))

    # If not moved, location stays the same
    for t in range(1, plan_length+1):
        for i in range(3):
            solver.add(Implies(Not(moved[i][t-1]), loc[i][t] == loc[i][t-1]))

    # Check satisfiability
    if solver.check() == sat:
        model = solver.model()
        print("STATUS: sat")
        print(f"plan_length: {plan_length}")
        for t in range(1, plan_length+1):
            moved_block = None
            for i in range(3):
                if is_true(model[moved[i][t-1]]):
                    moved_block = i
                    break
            if moved_block is None:
                continue
            from_loc = model[loc[moved_block][t-1]]
            to_loc = model[loc[moved_block][t]]
            print(f"step: {t}")
            print("action: move")
            print(f"block: {idx_to_name[moved_block]}")
            print(f"from: {idx_to_name[from_loc.as_long()]}")
            print(f"to: {idx_to_name[to_loc.as_long()]}")
        solution_found = True
        break

if not solution_found:
    print("STATUS: unsat")