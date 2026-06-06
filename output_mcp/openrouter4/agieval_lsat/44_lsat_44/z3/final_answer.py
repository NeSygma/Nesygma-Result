from z3 import *

solver = Solver()

# Variables
J_S, J_T, J_U = Bools('J_S J_T J_U')
K_S, K_T, K_U = Bools('K_S K_T K_U')
L_S, L_T, L_U = Bools('L_S L_T L_U')
M_S, M_T, M_U = Bools('M_S M_T M_U')
O_S, O_T, O_U = Bools('O_S O_T O_U')

J_plays = [J_S, J_T, J_U]
K_plays = [K_S, K_T, K_U]
L_plays = [L_S, L_T, L_U]
M_plays = [M_S, M_T, M_U]
O_plays = [O_S, O_T, O_U]

J_count = Sum([If(p, 1, 0) for p in J_plays])
K_count = Sum([If(p, 1, 0) for p in K_plays])
L_count = Sum([If(p, 1, 0) for p in L_plays])
M_count = Sum([If(p, 1, 0) for p in M_plays])
O_count = Sum([If(p, 1, 0) for p in O_plays])

# Each reviews at least 1 play
for plist in [J_plays, K_plays, L_plays, M_plays, O_plays]:
    solver.add(Sum([If(p, 1, 0) for p in plist]) >= 1)

# K and L each review fewer than M
solver.add(K_count < M_count)
solver.add(L_count < M_count)

# Lopez and Megregian do NOT review any play Jiang reviews
for p in [J_S, J_T, J_U]:
    # Lopez
    solver.add(Not(And(p, {'J_S': L_S, 'J_T': L_T, 'J_U': L_U}[str(p).split('_')[0] + '_' + str(p).split('_')[1]])))
# Let me do this more directly
solver.add(Not(And(J_S, L_S)))
solver.add(Not(And(J_T, L_T)))
solver.add(Not(And(J_U, L_U)))
solver.add(Not(And(J_S, M_S)))
solver.add(Not(And(J_T, M_T)))
solver.add(Not(And(J_U, M_U)))

# Kramer and O'Neill both review Tamerlane
solver.add(K_T == True)
solver.add(O_T == True)

# Exactly two students review exactly the same play or plays as each other
students_plays = [J_plays, K_plays, L_plays, M_plays, O_plays]
pair_matches = []
for i in range(5):
    for j in range(i+1, 5):
        match = Bool(f'match_{i}_{j}')
        same = And([students_plays[i][k] == students_plays[j][k] for k in range(3)])
        solver.add(match == same)
        pair_matches.append(match)

solver.add(Sum([If(m, 1, 0) for m in pair_matches]) == 1)

# Options
# (A) Jiang reviews more plays than Lopez
opt_a = J_count > L_count
# (B) Megregian reviews more plays than Jiang
opt_b = M_count > J_count
# (C) Megregian reviews more plays than O'Neill
opt_c = M_count > O_count
# (D) O'Neill reviews more plays than Jiang
opt_d = O_count > J_count
# (E) O'Neill reviews more plays than Kramer
opt_e = O_count > K_count

# Test each option: "must be true" means Not(option) is UNSAT
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    # To check if option MUST be true, we see if its negation is UNSAT
    solver.add(Not(constr))
    if solver.check() == unsat:
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