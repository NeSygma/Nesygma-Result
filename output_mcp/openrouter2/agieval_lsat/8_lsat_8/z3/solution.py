from z3 import *

solver = Solver()
# Define selection variables for each work
FN1 = Bool('FN1')
FN2 = Bool('FN2')
FN3 = Bool('FN3')
RN1 = Bool('RN1')
RN2 = Bool('RN2')
RN3 = Bool('RN3')
FP1 = Bool('FP1')
FP2 = Bool('FP2')
RP  = Bool('RP')

# Base constraints
# Total selected between 5 and 6
total_selected = Sum([If(FN1,1,0), If(FN2,1,0), If(FN3,1,0), If(RN1,1,0), If(RN2,1,0), If(RN3,1,0), If(FP1,1,0), If(FP2,1,0), If(RP,1,0)])
solver.add(total_selected >= 5, total_selected <= 6)

# No more than 4 French works
french_works = Sum([If(FN1,1,0), If(FN2,1,0), If(FN3,1,0), If(FP1,1,0), If(FP2,1,0)])
solver.add(french_works <= 4)

# At least 3 but no more than 4 novels
novels = Sum([If(FN1,1,0), If(FN2,1,0), If(FN3,1,0), If(RN1,1,0), If(RN2,1,0), If(RN3,1,0)])
solver.add(novels >= 3, novels <= 4)

# At least as many French novels as Russian novels
french_novels = Sum([If(FN1,1,0), If(FN2,1,0), If(FN3,1,0)])
russian_novels = Sum([If(RN1,1,0), If(RN2,1,0), If(RN3,1,0)])
solver.add(french_novels >= russian_novels)

# If both French plays selected, then Russian play not selected
solver.add(Or(Not(FP1), Not(FP2), Not(RP)))

# Option constraints
opt_a_constr = russian_novels == 0
opt_b_constr = french_novels == 1
opt_c_constr = And(FP1, FP2, RP)
opt_d_constr = russian_novels == 3
opt_e_constr = french_works == 5

# Evaluate options
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