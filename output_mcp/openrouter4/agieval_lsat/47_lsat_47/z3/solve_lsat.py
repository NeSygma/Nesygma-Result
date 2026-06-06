from z3 import *

solver = Solver()

# Variables for each student and each play
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

# Counts
count_K = Sum([K_S, K_T, K_U])
count_L = Sum([L_S, L_T, L_U])
count_M = Sum([M_S, M_T, M_U])

# Kramer and Lopez each review fewer plays than Megregian
solver.add(count_K < count_M)
solver.add(count_L < count_M)

# Neither Lopez nor Megregian reviews any play Jiang reviews
for j_var, l_var, m_var in [(J_S, L_S, M_S), (J_T, L_T, M_T), (J_U, L_U, M_U)]:
    solver.add(Not(And(j_var, l_var)))
    solver.add(Not(And(j_var, m_var)))

# Kramer and O'Neill both review Tamerlane
solver.add(K_T == True)
solver.add(O_T == True)

# Exactly two students review exactly the same play or plays as each other
students = [
    ("Jiang", [J_S, J_T, J_U]),
    ("Kramer", [K_S, K_T, K_U]),
    ("Lopez", [L_S, L_T, L_U]),
    ("Megregian", [M_S, M_T, M_U]),
    ("O'Neill", [O_S, O_T, O_U])
]

pairs = []
for i in range(5):
    for j in range(i+1, 5):
        name_i, vars_i = students[i]
        name_j, vars_j = students[j]
        identical = Bool(f'identical_{name_i}_{name_j}')
        solver.add(identical == And([vars_i[k] == vars_j[k] for k in range(3)]))
        pairs.append(identical)

solver.add(Sum(pairs) == 1)

# Condition: Jiang does not review Tamerlane
solver.add(Not(J_T))

# Options
options = [
    ("A", J_S),
    ("B", L_U),
    ("C", M_S),
    ("D", M_T),
    ("E", O_U)
]

found_options = []
for letter, constr in options:
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