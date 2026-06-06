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

pair_eqs = []
for a,b in pairs:
    eq = And([students[a][i] == students[b][i] for i in range(3)])
    pair_eqs.append(eq)

solver.add(Sum([If(eq,1,0) for eq in pair_eqs]) == 1)

print(solver.check())
if solver.check() == sat:
    m = solver.model()
    print(m)