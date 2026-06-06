from z3 import *

solver = Solver()

# Booleans for each student-play
J_S, J_T, J_U = Bools('J_S J_T J_U')
K_S, K_T, K_U = Bools('K_S K_T K_U')
L_S, L_T, L_U = Bools('L_S L_T L_U')
M_S, M_T, M_U = Bools('M_S M_T M_U')
O_S, O_T, O_U = Bools('O_S O_T O_U')

# Each student reviews at least one play
solver.add(Or(J_S, J_T, J_U))
solver.add(Or(K_S, K_T, K_U))
solver.add(Or(L_S, L_T, L_U))
solver.add(Or(M_S, M_T, M_U))
solver.add(Or(O_S, O_T, O_U))

# Jiang does not review Tamerlane
solver.add(J_T == False)

# Kramer and O'Neill both review Tamerlane
solver.add(K_T == True)
solver.add(O_T == True)

# Lopez and Megregian do not review any play Jiang reviews
solver.add(Or(Not(L_S), Not(J_S)))
solver.add(Or(Not(L_T), Not(J_T)))
solver.add(Or(Not(L_U), Not(J_U)))
solver.add(Or(Not(M_S), Not(J_S)))
solver.add(Or(Not(M_T), Not(J_T)))
solver.add(Or(Not(M_U), Not(J_U)))

# Kramer and Lopez review fewer plays than Megregian
solver.add(Sum([If(K_S,1,0), If(K_T,1,0), If(K_U,1,0)]) <
          Sum([If(M_S,1,0), If(M_T,1,0), If(M_U,1,0)]))
solver.add(Sum([If(L_S,1,0), If(L_T,1,0), If(L_U,1,0)]) <
          Sum([If(M_S,1,0), If(M_T,1,0), If(M_U,1,0)]))

# Exactly one pair of students review exactly the same set of plays
students = {
    'J': [J_S, J_T, J_U],
    'K': [K_S, K_T, K_U],
    'L': [L_S, L_T, L_U],
    'M': [M_S, M_T, M_U],
    'O': [O_S, O_T, O_U]
}

pairs = [('J','K'), ('J','L'), ('J','M'), ('J','O'),
         ('K','L'), ('K','M'), ('K','O'),
         ('L','M'), ('L','O'),
         ('M','O')]

# Build equality constraints for each pair
pair_eqs = []
for a,b in pairs:
    eq = And([students[a][i] == students[b][i] for i in range(3)])
    pair_eqs.append(eq)

solver.add(Sum([If(eq,1,0) for eq in pair_eqs]) == 1)

# Option constraints
opt_a_constr = J_S == True
opt_b_constr = L_U == True
opt_c_constr = M_S == True
opt_d_constr = M_T == True
opt_e_constr = O_U == True

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