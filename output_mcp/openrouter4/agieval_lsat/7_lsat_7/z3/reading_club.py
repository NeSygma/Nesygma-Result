from z3 import *

solver = Solver()

# Variables for each work
FN = [Bool(f'FN_{i}') for i in range(3)]  # 3 French novels
RN = [Bool(f'RN_{i}') for i in range(3)]  # 3 Russian novels
FP = [Bool(f'FP_{i}') for i in range(2)]  # 2 French plays
RP = Bool('RP')  # 1 Russian play

# Total works selected: at least 5, at most 6
total_selected = Sum([FN[i] for i in range(3)] + [RN[i] for i in range(3)] + [FP[i] for i in range(2)] + [RP])
solver.add(total_selected >= 5)
solver.add(total_selected <= 6)

# Constraint 1: No more than 4 French works are selected
french_works = Sum([FN[i] for i in range(3)] + [FP[i] for i in range(2)])
solver.add(french_works <= 4)

# Constraint 2: At least 3 but no more than 4 novels are selected
novels = Sum([FN[i] for i in range(3)] + [RN[i] for i in range(3)])
solver.add(novels >= 3)
solver.add(novels <= 4)

# Constraint 3: At least as many French novels as Russian novels
french_novels = Sum([FN[i] for i in range(3)])
russian_novels = Sum([RN[i] for i in range(3)])
solver.add(french_novels >= russian_novels)

# Constraint 4: If both French plays are selected, then the Russian play is not selected
solver.add(Implies(And(FP[0], FP[1]), Not(RP)))

# Now test each option
# Option A: one French novel, two Russian novels, one French play, one Russian play
opt_a_constr = And(
    Sum([FN[i] for i in range(3)]) == 1,
    Sum([RN[i] for i in range(3)]) == 2,
    Sum([FP[i] for i in range(2)]) == 1,
    RP == True
)

# Option B: two French novels, one Russian novel, two French plays, one Russian play
opt_b_constr = And(
    Sum([FN[i] for i in range(3)]) == 2,
    Sum([RN[i] for i in range(3)]) == 1,
    Sum([FP[i] for i in range(2)]) == 2,
    RP == True
)

# Option C: two French novels, two Russian novels, two French plays
opt_c_constr = And(
    Sum([FN[i] for i in range(3)]) == 2,
    Sum([RN[i] for i in range(3)]) == 2,
    Sum([FP[i] for i in range(2)]) == 2,
    RP == False
)

# Option D: three French novels, one Russian novel, two French plays
opt_d_constr = And(
    Sum([FN[i] for i in range(3)]) == 3,
    Sum([RN[i] for i in range(3)]) == 1,
    Sum([FP[i] for i in range(2)]) == 2,
    RP == False
)

# Option E: three French novels, two Russian novels, one Russian play
opt_e_constr = And(
    Sum([FN[i] for i in range(3)]) == 3,
    Sum([RN[i] for i in range(3)]) == 2,
    Sum([FP[i] for i in range(2)]) == 0,
    RP == True
)

found_options = []
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