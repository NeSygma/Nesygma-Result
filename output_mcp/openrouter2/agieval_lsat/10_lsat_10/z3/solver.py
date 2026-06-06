from z3 import *

# Define boolean variables for each work
FN1, FN2, FN3 = Bools('FN1 FN2 FN3')  # French novels
RN1, RN2, RN3 = Bools('RN1 RN2 RN3')  # Russian novels
FP1, FP2 = Bools('FP1 FP2')            # French plays
RP = Bool('RP')                        # Russian play

# Helper to sum booleans as integers
bools_to_int = lambda lst: Sum([If(b, 1, 0) for b in lst])

solver = Solver()

# Total selected between 5 and 6
solver.add(bools_to_int([FN1, FN2, FN3, RN1, RN2, RN3, FP1, FP2, RP]) >= 5)
solver.add(bools_to_int([FN1, FN2, FN3, RN1, RN2, RN3, FP1, FP2, RP]) <= 6)

# No more than 4 French works (French novels + French plays)
solver.add(bools_to_int([FN1, FN2, FN3, FP1, FP2]) <= 4)

# At least 3 but no more than 4 novels (French novels + Russian novels)
solver.add(bools_to_int([FN1, FN2, FN3, RN1, RN2, RN3]) >= 3)
solver.add(bools_to_int([FN1, FN2, FN3, RN1, RN2, RN3]) <= 4)

# At least as many French novels as Russian novels
solver.add(bools_to_int([FN1, FN2, FN3]) >= bools_to_int([RN1, RN2, RN3]))

# If both French plays selected, then Russian play not selected
solver.add(Implies(And(FP1, FP2), Not(RP)))

# Define negated constraints for each option
# Option A: at least one French novel and one French play
opt_a_constr = Or(And(Not(FN1), Not(FN2), Not(FN3)),  # no French novel
                  And(Not(FP1), Not(FP2)))          # no French play

# Option B: at least one French novel and one Russian play
opt_b_constr = Or(And(Not(FN1), Not(FN2), Not(FN3)),  # no French novel
                  Not(RP))                            # no Russian play

# Option C: at least one Russian novel and one French play
opt_c_constr = Or(And(Not(RN1), Not(RN2), Not(RN3)),  # no Russian novel
                  And(Not(FP1), Not(FP2)))          # no French play

# Option D: at least two French novels
opt_d_constr = bools_to_int([FN1, FN2, FN3]) <= 1

# Option E: at least two Russian novels
opt_e_constr = bools_to_int([RN1, RN2, RN3]) <= 1

# Evaluate each option
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