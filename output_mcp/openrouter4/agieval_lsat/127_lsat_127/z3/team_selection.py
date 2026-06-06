from z3 import *

solver = Solver()

# Boolean variables for each employee
M = Bool('Myers')
O = Bool('Ortega')
P = Bool('Paine')
S = Bool('Schmidt')
T = Bool('Thomson')
W = Bool('Wong')
Y = Bool('Yoder')  # Yoder
Z = Bool('Zayre')

# At least 4 employees on the team
solver.add(Sum([If(M, 1, 0), If(O, 1, 0), If(P, 1, 0), If(S, 1, 0), 
                If(T, 1, 0), If(W, 1, 0), If(Y, 1, 0), If(Z, 1, 0)]) >= 4)

# If Myers is on the team, neither Ortega nor Paine can be
solver.add(Implies(M, Not(Or(O, P))))

# If Schmidt is on the team, both Paine and Thomson must also be
solver.add(Implies(S, And(P, T)))

# If Wong is on the team, both Myers and Yoder must also be
solver.add(Implies(W, And(M, Y)))

# Now test each option: is it possible for BOTH employees in the pair to be OFF the team?
# If it's UNSAT, then at least one MUST be on the team.

found_options = []

# Option A: Ortega and Schmidt
opt_a_constr = And(Not(O), Not(S))
# Option B: Ortega and Wong
opt_b_constr = And(Not(O), Not(W))
# Option C: Paine and Schmidt
opt_c_constr = And(Not(P), Not(S))
# Option D: Thomson and Yoder
opt_d_constr = And(Not(T), Not(Y))
# Option E: Yoder and Zayre
opt_e_constr = And(Not(Y), Not(Z))

for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    # We add the constraint that both are NOT on the team
    solver.add(constr)
    if solver.check() == sat:
        m = solver.model()
        # It IS possible for both to be off the team, so this pair does NOT work
        # We don't add to found_options
        pass
    else:
        # UNSAT - it's impossible for both to be off the team, so at least one must be on the team
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