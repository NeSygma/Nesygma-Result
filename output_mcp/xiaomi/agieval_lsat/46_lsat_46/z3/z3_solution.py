from z3 import *

solver = Solver()

# Students: Jiang=0, Kramer=1, Lopez=2, Megregian=3, O'Neill=4
# Plays: Sunset=0, Tamerlane=1, Undulation=2

# review[s][p] = True if student s reviews play p
review = [[Bool(f"review_{s}_{p}") for p in range(3)] for s in range(5)]

# Each student reviews one or more plays
for s in range(5):
    solver.add(Or(review[s][0], review[s][1], review[s][2]))

# Count of plays each student reviews
def play_count(s):
    return If(review[s][0], 1, 0) + If(review[s][1], 1, 0) + If(review[s][2], 1, 0)

# Kramer and Lopez each review fewer plays than Megregian
solver.add(play_count(1) < play_count(3))  # Kramer < Megregian
solver.add(play_count(2) < play_count(3))  # Lopez < Megregian

# Neither Lopez nor Megregian reviews any play Jiang reviews
for p in range(3):
    solver.add(Implies(review[0][p], Not(review[2][p])))  # Jiang -> not Lopez
    solver.add(Implies(review[0][p], Not(review[3][p])))  # Jiang -> not Megregian

# Kramer and O'Neill both review Tamerlane
solver.add(review[1][1] == True)   # Kramer reviews Tamerlane
solver.add(review[4][1] == True)   # O'Neill reviews Tamerlane

# Exactly two of the students review exactly the same play or plays as each other
# This means exactly one pair of students has identical review sets, and no other pair matches
# We need to check all pairs
def same_plays(s1, s2):
    return And([review[s1][p] == review[s2][p] for p in range(3)])

# Count pairs with same plays
pair_same = []
for i in range(5):
    for j in range(i+1, 5):
        pair_same.append(If(same_plays(i, j), 1, 0))

solver.add(Sum(pair_same) == 1)

# Now test each answer choice for who reviews Tamerlane
# A: Jiang, Kramer
opt_a = And(review[0][1] == True, review[1][1] == True, review[2][1] == False, review[3][1] == False, review[4][1] == False)
# B: Kramer, O'Neill
opt_b = And(review[0][1] == False, review[1][1] == True, review[2][1] == False, review[3][1] == False, review[4][1] == True)
# C: Kramer, Lopez, O'Neill
opt_c = And(review[0][1] == False, review[1][1] == True, review[2][1] == True, review[3][1] == False, review[4][1] == True)
# D: Kramer, Megregian, O'Neill
opt_d = And(review[0][1] == False, review[1][1] == True, review[2][1] == False, review[3][1] == True, review[4][1] == True)
# E: Lopez, Megregian, O'Neill
opt_e = And(review[0][1] == False, review[1][1] == False, review[2][1] == True, review[3][1] == True, review[4][1] == True)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for s in range(5):
            plays = []
            for p in range(3):
                if is_true(m.evaluate(review[s][p])):
                    plays.append(["Sunset", "Tamerlane", "Undulation"][p])
            names = ["Jiang", "Kramer", "Lopez", "Megregian", "O'Neill"]
            print(f"  {names[s]}: {plays}")
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