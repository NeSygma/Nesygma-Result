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
# Lopez and Jiang: disjoint sets - for each play, not both review it
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

# Count pairs with identical play sets
pair_matches = []
for i in range(5):
    for j in range(i+1, 5):
        match = Bool(f'match_{i}_{j}')
        play_conditions = []
        for k in range(3):
            play_conditions.append(students_plays[i][k] == students_plays[j][k])
        solver.add(match == And(play_conditions))
        pair_matches.append(match)

# Exactly one pair matches
solver.add(Sum([If(m, 1, 0) for m in pair_matches]) == 1)

print("=== Checking each option for 'must be true' ===")
print("(Testing if the negation of the option is UNSAT)")

# (A) Jiang reviews more of the plays than Lopez does.
solver.push()
solver.add(Not(J_count > L_count))  # J <= L
res = solver.check()
print(f"A (Not: J <= L): {res}")
if res == unsat:
    print("  -> A must be true")
solver.pop()

# (B) Megregian reviews more of the plays than Jiang does.
solver.push()
solver.add(Not(M_count > J_count))  # M <= J
res = solver.check()
print(f"B (Not: M <= J): {res}")
if res == unsat:
    print("  -> B must be true")
solver.pop()

# (C) Megregian reviews more of the plays than O'Neill does.
solver.push()
solver.add(Not(M_count > O_count))  # M <= O
res = solver.check()
print(f"C (Not: M <= O): {res}")
if res == unsat:
    print("  -> C must be true")
solver.pop()

# (D) O'Neill reviews more of the plays than Jiang does.
solver.push()
solver.add(Not(O_count > J_count))  # O <= J
res = solver.check()
print(f"D (Not: O <= J): {res}")
if res == unsat:
    print("  -> D must be true")
solver.pop()

# (E) O'Neill reviews more of the plays than Kramer does.
solver.push()
solver.add(Not(O_count > K_count))  # O <= K
res = solver.check()
print(f"E (Not: O <= K): {res}")
if res == unsat:
    print("  -> E must be true")
solver.pop()

# Now also print a sample model to verify understanding
print("\n=== Sample model ===")
solver.push()
if solver.check() == sat:
    m = solver.model()
    print(f"J: S={m[J_S]}, T={m[J_T]}, U={m[J_U]} -> count={m.eval(J_count)}")
    print(f"K: S={m[K_S]}, T={m[K_T]}, U={m[K_U]} -> count={m.eval(K_count)}")
    print(f"L: S={m[L_S]}, T={m[L_T]}, U={m[L_U]} -> count={m.eval(L_count)}")
    print(f"M: S={m[M_S]}, T={m[M_T]}, U={m[M_U]} -> count={m.eval(M_count)}")
    print(f"O: S={m[O_S]}, T={m[O_T]}, U={m[O_U]} -> count={m.eval(O_count)}")
solver.pop()