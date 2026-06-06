from z3 import *

solver = Solver()

# Boolean variables for each work
# French novels
FN = [Bool(f"FN_{i}") for i in range(3)]
# Russian novels
RN = [Bool(f"RN_{i}") for i in range(3)]
# French plays
FP = [Bool(f"FP_{i}") for i in range(2)]
# Russian play
RP = Bool("RP")

# Helper: count selected = sum of If(var, 1, 0)
selected_FN = Sum([If(fn, 1, 0) for fn in FN])
selected_RN = Sum([If(rn, 1, 0) for rn in RN])
selected_FP = Sum([If(fp, 1, 0) for fp in FP])
selected_RP = If(RP, 1, 0)

total_selected = selected_FN + selected_RN + selected_FP + selected_RP

# Constraint 1: At least 5 and at most 6 works selected
solver.add(total_selected >= 5)
solver.add(total_selected <= 6)

# Constraint 2: No more than 4 French works
solver.add(selected_FN + selected_FP <= 4)

# Constraint 3: At least 3 but no more than 4 novels
solver.add(selected_FN + selected_RN >= 3)
solver.add(selected_FN + selected_RN <= 4)

# Constraint 4: At least as many French novels as Russian novels
solver.add(selected_FN >= selected_RN)

# Constraint 5: If both French plays are selected, then Russian play is not selected
solver.add(Implies(selected_FP == 2, selected_RP == 0))

# Now evaluate each option
found_options = []

# Option A: No Russian novels and exactly one play
opt_a_constr = And(selected_RN == 0, selected_FP + selected_RP == 1)

# Option B: Exactly one Russian novel and both French plays
opt_b_constr = And(selected_RN == 1, selected_FP == 2)

# Option C: Exactly two French novels and the Russian play
opt_c_constr = And(selected_FN == 2, selected_RP == 1)

# Option D: Exactly two French novels and exactly two plays
opt_d_constr = And(selected_FN == 2, selected_FP + selected_RP == 2)

# Option E: Exactly two Russian novels and exactly one play
opt_e_constr = And(selected_RN == 2, selected_FP + selected_RP == 1)

for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")