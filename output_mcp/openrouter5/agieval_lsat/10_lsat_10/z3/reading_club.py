from z3 import *

# We have 9 works:
# French novels: FN1, FN2, FN3
# Russian novels: RN1, RN2, RN3
# French plays: FP1, FP2
# Russian play: RP1

# Boolean variables: True if selected
FN = [Bool(f'FN{i}') for i in range(1, 4)]
RN = [Bool(f'RN{i}') for i in range(1, 4)]
FP = [Bool(f'FP{i}') for i in range(1, 3)]
RP = Bool('RP1')

solver = Solver()

# Total selected: at least 5, at most 6
total_selected = Sum([If(v, 1, 0) for v in FN + RN + FP + [RP]])
solver.add(total_selected >= 5)
solver.add(total_selected <= 6)

# No more than 4 French works selected
# French works: FN1-3, FP1-2
french_selected = Sum([If(v, 1, 0) for v in FN + FP])
solver.add(french_selected <= 4)

# At least 3 but no more than 4 novels selected
# Novels: FN1-3, RN1-3
novels_selected = Sum([If(v, 1, 0) for v in FN + RN])
solver.add(novels_selected >= 3)
solver.add(novels_selected <= 4)

# At least as many French novels as Russian novels selected
french_novels_selected = Sum([If(v, 1, 0) for v in FN])
russian_novels_selected = Sum([If(v, 1, 0) for v in RN])
solver.add(french_novels_selected >= russian_novels_selected)

# If both French plays are selected, then the Russian play is not selected
solver.add(Implies(And(FP[0], FP[1]), Not(RP)))

# Now evaluate each option.
# Each option says "the organizer must at least select X".
# This means: in EVERY valid selection, X must be selected.
# So we test: is it possible to have a valid selection WITHOUT X?
# If NOT possible (unsat), then X is mandatory.
# If possible (sat), then X is not mandatory.

# Option A: one French novel and one French play
# "Must at least select one French novel and one French play"
# Means: at least one FN and at least one FP are mandatory.
# Test: can we have a valid selection with zero French novels OR zero French plays?
opt_a_constr = Or(
    Sum([If(v, 1, 0) for v in FN]) == 0,
    Sum([If(v, 1, 0) for v in FP]) == 0
)

# Option B: one French novel and one Russian play
opt_b_constr = Or(
    Sum([If(v, 1, 0) for v in FN]) == 0,
    RP == False
)

# Option C: one Russian novel and one French play
opt_c_constr = Or(
    Sum([If(v, 1, 0) for v in RN]) == 0,
    Sum([If(v, 1, 0) for v in FP]) == 0
)

# Option D: two French novels
opt_d_constr = Sum([If(v, 1, 0) for v in FN]) <= 1

# Option E: two Russian novels
opt_e_constr = Sum([If(v, 1, 0) for v in RN]) <= 1

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        # It IS possible to have a valid selection without the required items,
        # so the option is NOT mandatory -> not the answer
        pass
    else:
        # It is NOT possible to have a valid selection without the required items,
        # so the option IS mandatory -> this is the answer
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