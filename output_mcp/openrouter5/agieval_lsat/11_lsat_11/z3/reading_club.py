from z3 import *

# Nine works: 3 French novels (FN0, FN1, FN2), 3 Russian novels (RN0, RN1, RN2),
# 2 French plays (FP0, FP1), 1 Russian play (RP0)

# Boolean variables: True if selected
FN = [Bool(f'FN_{i}') for i in range(3)]
RN = [Bool(f'RN_{i}') for i in range(3)]
FP = [Bool(f'FP_{i}') for i in range(2)]
RP = [Bool(f'RP_{0}') for i in range(1)]  # just one

all_works = FN + RN + FP + RP

solver = Solver()

# At least 5 and at most 6 works selected
solver.add(Sum([If(w, 1, 0) for w in all_works]) >= 5)
solver.add(Sum([If(w, 1, 0) for w in all_works]) <= 6)

# No more than 4 French works selected
french_works = FN + FP
solver.add(Sum([If(w, 1, 0) for w in french_works]) <= 4)

# At least 3 but no more than 4 novels selected
novels = FN + RN
solver.add(Sum([If(w, 1, 0) for w in novels]) >= 3)
solver.add(Sum([If(w, 1, 0) for w in novels]) <= 4)

# At least as many French novels as Russian novels selected
solver.add(Sum([If(w, 1, 0) for w in FN]) >= Sum([If(w, 1, 0) for w in RN]))

# If both French plays are selected, then the Russian play is not selected
solver.add(Implies(And(FP[0], FP[1]), Not(RP[0])))

# Now evaluate each option

# Option A: No Russian novels and exactly one play are selected.
opt_a = And(
    Sum([If(w, 1, 0) for w in RN]) == 0,
    Sum([If(w, 1, 0) for w in FP + RP]) == 1
)

# Option B: Exactly one Russian novel and both French plays are selected.
opt_b = And(
    Sum([If(w, 1, 0) for w in RN]) == 1,
    And(FP[0], FP[1])
)

# Option C: Exactly two French novels and the Russian play are selected.
opt_c = And(
    Sum([If(w, 1, 0) for w in FN]) == 2,
    RP[0]
)

# Option D: Exactly two French novels and exactly two plays are selected.
opt_d = And(
    Sum([If(w, 1, 0) for w in FN]) == 2,
    Sum([If(w, 1, 0) for w in FP + RP]) == 2
)

# Option E: Exactly two Russian novels and exactly one play are selected.
opt_e = And(
    Sum([If(w, 1, 0) for w in RN]) == 2,
    Sum([If(w, 1, 0) for w in FP + RP]) == 1
)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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