from z3 import *

# Students: J, K, L, M, O
# Plays: S (Sunset), T (Tamerlane), U (Undulation)

# Create Bool variables
J_S, J_T, J_U = Bools('J_S J_T J_U')
K_S, K_T, K_U = Bools('K_S K_T K_U')
L_S, L_T, L_U = Bools('L_S L_T L_U')
M_S, M_T, M_U = Bools('M_S M_T M_U')
O_S, O_T, O_U = Bools('O_S O_T O_U')

solver = Solver()

# Each student reviews at least one play
students = [(J_S, J_T, J_U), (K_S, K_T, K_U), (L_S, L_T, L_U), (M_S, M_T, M_U), (O_S, O_T, O_U)]
for s in students:
    solver.add(Or(s))

# Kramer and O'Neill both review Tamerlane
solver.add(K_T == True)
solver.add(O_T == True)

# Kramer and Lopez each review fewer plays than Megregian
sum_K = Sum([If(K_S, 1, 0), If(K_T, 1, 0), If(K_U, 1, 0)])
sum_L = Sum([If(L_S, 1, 0), If(L_T, 1, 0), If(L_U, 1, 0)])
sum_M = Sum([If(M_S, 1, 0), If(M_T, 1, 0), If(M_U, 1, 0)])
solver.add(sum_K < sum_M)
solver.add(sum_L < sum_M)

# Neither Lopez nor Megregian reviews any play Jiang reviews
for play_J, play_L, play_M in [(J_S, L_S, M_S), (J_T, L_T, M_T), (J_U, L_U, M_U)]:
    solver.add(Implies(play_J, Not(play_L)))
    solver.add(Implies(play_J, Not(play_M)))

# Exactly two of the students review exactly the same play(s) as each other
# Compute equality for each unordered pair
pairs = []
names = ['J','K','L','M','O']
vars = {
    'J': (J_S, J_T, J_U),
    'K': (K_S, K_T, K_U),
    'L': (L_S, L_T, L_U),
    'M': (M_S, M_T, M_U),
    'O': (O_S, O_T, O_U)
}
for i in range(5):
    for j in range(i+1,5):
        vi = vars[names[i]]
        vj = vars[names[j]]
        eq = And(vi[0] == vj[0], vi[1] == vj[1], vi[2] == vj[2])
        pairs.append(eq)
# Exactly one pair equal
solver.add(Sum([If(p, 1, 0) for p in pairs]) == 1)

# Exactly three students review Undulation
sum_U = Sum([If(J_U,1,0), If(K_U,1,0), If(L_U,1,0), If(M_U,1,0), If(O_U,1,0)])
solver.add(sum_U == 3)

# Define option constraints
opt_a = M_U == False
opt_b = O_U == False
opt_c = J_U == True
opt_d = L_T == True
opt_e = O_S == True

found_options = []
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