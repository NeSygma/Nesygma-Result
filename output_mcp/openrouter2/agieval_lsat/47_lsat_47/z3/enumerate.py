from z3 import *

# Define solver and constraints as before
solver = Solver()
J_S, J_T, J_U = Bools('J_S J_T J_U')
K_S, K_T, K_U = Bools('K_S K_T K_U')
L_S, L_T, L_U = Bools('L_S L_T L_U')
M_S, M_T, M_U = Bools('M_S M_T M_U')
O_S, O_T, O_U = Bools('O_S O_T O_U')

solver.add(Or(J_S, J_T, J_U))
solver.add(Or(K_S, K_T, K_U))
solver.add(Or(L_S, L_T, L_U))
solver.add(Or(M_S, M_T, M_U))
solver.add(Or(O_S, O_T, O_U))

solver.add(J_T == False)
solver.add(K_T == True)
solver.add(O_T == True)

solver.add(Or(Not(L_S), Not(J_S)))
solver.add(Or(Not(L_T), Not(J_T)))
solver.add(Or(Not(L_U), Not(J_U)))
solver.add(Or(Not(M_S), Not(J_S)))
solver.add(Or(Not(M_T), Not(J_T)))
solver.add(Or(Not(M_U), Not(J_U)))

solver.add(Sum([If(K_S,1,0), If(K_T,1,0), If(K_U,1,0)]) <
          Sum([If(M_S,1,0), If(M_T,1,0), If(M_U,1,0)]))
solver.add(Sum([If(L_S,1,0), If(L_T,1,0), If(L_U,1,0)]) <
          Sum([If(M_S,1,0), If(M_T,1,0), If(M_U,1,0)]))

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

# Enumerate all models
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {v: m[v] for v in [J_S,J_T,J_U,K_S,K_T,K_U,L_S,L_T,L_U,M_S,M_T,M_U,O_S,O_T,O_U]}
    solutions.append(sol)
    # block
    solver.add(Or([v != m[v] for v in [J_S,J_T,J_U,K_S,K_T,K_U,L_S,L_T,L_U,M_S,M_T,M_U,O_S,O_T,O_U]]))

print('Total solutions:', len(solutions))
# Evaluate options
options = {
    'A': J_S,  # Jiang reviews Sunset
    'B': L_U,  # Lopez reviews Undulation
    'C': M_S,  # Megregian reviews Sunset
    'D': M_T,  # Megregian reviews Tamerlane
    'E': O_U   # O'Neill reviews Undulation
}
for letter, var in options.items():
    true_count = sum(1 for sol in solutions if sol[var])
    false_count = len(solutions) - true_count
    print(letter, true_count, false_count)