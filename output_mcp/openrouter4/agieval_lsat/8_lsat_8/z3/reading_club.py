from z3 import *

solver = Solver()

# Boolean variables for each work
fn1, fn2, fn3 = Bools('fn1 fn2 fn3')  # French novels
rn1, rn2, rn3 = Bools('rn1 rn2 rn3')  # Russian novels
fp1, fp2 = Bools('fp1 fp2')            # French plays
rp = Bool('rp')                        # Russian play

french_novels = [fn1, fn2, fn3]
russian_novels = [rn1, rn2, rn3]
french_plays = [fp1, fp2]
all_french = french_novels + french_plays
all_novels = french_novels + russian_novels
all_works = french_novels + russian_novels + french_plays + [rp]

# Constraint: total selected between 5 and 6
solver.add(Sum([If(w, 1, 0) for w in all_works]) >= 5)
solver.add(Sum([If(w, 1, 0) for w in all_works]) <= 6)

# Constraint: No more than 4 French works selected
solver.add(Sum([If(w, 1, 0) for w in all_french]) <= 4)

# Constraint: At least 3 but no more than 4 novels selected
solver.add(Sum([If(w, 1, 0) for w in all_novels]) >= 3)
solver.add(Sum([If(w, 1, 0) for w in all_novels]) <= 4)

# Constraint: At least as many French novels as Russian novels
solver.add(Sum([If(w, 1, 0) for w in french_novels]) >= Sum([If(w, 1, 0) for w in russian_novels]))

# Constraint: If both French plays are selected, then the Russian play is not selected
solver.add(Implies(And(fp1, fp2), Not(rp)))

# Evaluate each option
found_options = []

# Option A: No Russian novels are selected
opt_a = And([Not(rn) for rn in russian_novels])

# Option B: Exactly one French novel is selected
opt_b = Sum([If(fn, 1, 0) for fn in french_novels]) == 1

# Option C: All three plays are selected
opt_c = And(fp1, fp2, rp)

# Option D: All three Russian novels are selected
opt_d = And(rn1, rn2, rn3)

# Option E: All five French works are selected
opt_e = And([w for w in all_french])

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