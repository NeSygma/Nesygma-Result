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

# The question asks: "Any one of the following could be true EXCEPT"
# So we need to find which option CANNOT be true (i.e., is unsat).
# We test each option. The one that is unsat is the answer.

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

# Find which options are SAT (could be true) and which are UNSAT (cannot be true)
results = {}
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    s = Solver()
    # Add base constraints
    s.add(Sum([If(w, 1, 0) for w in all_works]) >= 5)
    s.add(Sum([If(w, 1, 0) for w in all_works]) <= 6)
    s.add(Sum([If(w, 1, 0) for w in french_works]) <= 4)
    s.add(Sum([If(w, 1, 0) for w in novels]) >= 3)
    s.add(Sum([If(w, 1, 0) for w in novels]) <= 4)
    s.add(Sum([If(w, 1, 0) for w in FN]) >= Sum([If(w, 1, 0) for w in RN]))
    s.add(Implies(And(FP[0], FP[1]), Not(RP[0])))
    s.add(constr)
    res = s.check()
    results[letter] = res
    print(f"Option {letter}: {res}")
    if res == sat:
        print(f"  Model: {s.model()}")

# The answer is the one that is UNSAT (cannot be true)
unsat_options = [k for k, v in results.items() if v == unsat]
if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
else:
    print("STATUS: unsat")
    print(f"Refine: Expected exactly 1 unsat option, got {unsat_options}")