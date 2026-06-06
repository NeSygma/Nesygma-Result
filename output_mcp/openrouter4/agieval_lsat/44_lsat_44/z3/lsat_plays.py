from z3 import *

solver = Solver()

# Students: Jiang, Kramer, Lopez, Megregian, O'Neill
# Plays: Sunset (S), Tamerlane (T), Undulation (U)

# Boolean variables: student_reviews_play
J_S, J_T, J_U = Bools('J_S J_T J_U')
K_S, K_T, K_U = Bools('K_S K_T K_U')
L_S, L_T, L_U = Bools('L_S L_T L_U')
M_S, M_T, M_U = Bools('M_S M_T M_U')
O_S, O_T, O_U = Bools('O_S O_T O_U')

# Group by student
J_plays = [J_S, J_T, J_U]
K_plays = [K_S, K_T, K_U]
L_plays = [L_S, L_T, L_U]
M_plays = [M_S, M_T, M_U]
O_plays = [O_S, O_T, O_U]

# Each student reviews one or more plays (at least 1)
solver.add(Sum([If(p, 1, 0) for p in J_plays]) >= 1)
solver.add(Sum([If(p, 1, 0) for p in K_plays]) >= 1)
solver.add(Sum([If(p, 1, 0) for p in L_plays]) >= 1)
solver.add(Sum([If(p, 1, 0) for p in M_plays]) >= 1)
solver.add(Sum([If(p, 1, 0) for p in O_plays]) >= 1)

# Count of plays each student reviews
J_count = Sum([If(p, 1, 0) for p in J_plays])
K_count = Sum([If(p, 1, 0) for p in K_plays])
L_count = Sum([If(p, 1, 0) for p in L_plays])
M_count = Sum([If(p, 1, 0) for p in M_plays])
O_count = Sum([If(p, 1, 0) for p in O_plays])

# Constraint 1: Kramer and Lopez each review fewer plays than Megregian
solver.add(K_count < M_count)
solver.add(L_count < M_count)

# Constraint 2: Neither Lopez nor Megregian reviews any play Jiang reviews
# Lopez and Jiang: disjoint sets
solver.add(Not(And(J_S, L_S)))
solver.add(Not(And(J_T, L_T)))
solver.add(Not(And(J_U, L_U)))
# Megregian and Jiang: disjoint sets
solver.add(Not(And(J_S, M_S)))
solver.add(Not(And(J_T, M_T)))
solver.add(Not(And(J_U, M_U)))

# Constraint 3: Kramer and O'Neill both review Tamerlane
solver.add(K_T == True)
solver.add(O_T == True)

# Constraint 4: Exactly two of the students review exactly the same play or plays as each other
# This means there is exactly ONE pair of students whose play sets are identical
students_plays = [J_plays, K_plays, L_plays, M_plays, O_plays]
student_names = ['J', 'K', 'L', 'M', 'O']

# Count pairs with identical play sets
pair_matches = []
for i in range(5):
    for j in range(i+1, 5):
        # Are student i and student j's play sets identical?
        match = Bool(f'match_{i}_{j}')
        # They match if for each play, both review it or both don't
        play_conditions = []
        for k in range(3):
            play_conditions.append(students_plays[i][k] == students_plays[j][k])
        solver.add(match == And(play_conditions))
        pair_matches.append(match)

# Exactly one pair matches
solver.add(Sum([If(m, 1, 0) for m in pair_matches]) == 1)

# Now evaluate each answer choice

# (A) Jiang reviews more of the plays than Lopez does.
opt_a = (J_count > L_count)

# (B) Megregian reviews more of the plays than Jiang does.
opt_b = (M_count > J_count)

# (C) Megregian reviews more of the plays than O'Neill does.
opt_c = (M_count > O_count)

# (D) O'Neill reviews more of the plays than Jiang does.
opt_d = (O_count > J_count)

# (E) O'Neill reviews more of the plays than Kramer does.
opt_e = (O_count > K_count)

# Check each option
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