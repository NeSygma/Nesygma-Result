from z3 import *

# Students: Jiang, Kramer, Lopez, Megregian, O'Neill
# Plays: Sunset, Tamerlane, Undulation

J, K, L, M, O = 0, 1, 2, 3, 4
S, T, U = 0, 1, 2

students = [J, K, L, M, O]
student_names = ["Jiang", "Kramer", "Lopez", "Megregian", "O'Neill"]

# reviews[student][play] is True if student reviews that play
reviews = [[Bool(f"r_{i}_{j}") for j in range(3)] for i in range(5)]

def count_plays(student):
    """Number of plays reviewed by a student"""
    return Sum([If(reviews[student][p], 1, 0) for p in range(3)])

def same_set(i, j):
    """Returns True iff students i and j review exactly the same plays"""
    return And([reviews[i][p] == reviews[j][p] for p in range(3)])

solver = Solver()

# Constraint 1: Each student reviews at least one play
for i in range(5):
    solver.add(Or([reviews[i][p] for p in range(3)]))

# Constraint 2: Kramer and Lopez each review fewer plays than Megregian
solver.add(count_plays(K) < count_plays(M))
solver.add(count_plays(L) < count_plays(M))

# Constraint 3: Neither Lopez nor Megregian reviews any play Jiang reviews
# For each play, if Jiang reviews it, Lopez doesn't, and Megregian doesn't
for p in range(3):
    solver.add(Implies(reviews[J][p], Not(reviews[L][p])))
    solver.add(Implies(reviews[J][p], Not(reviews[M][p])))

# Constraint 4: Kramer and O'Neill both review Tamerlane
solver.add(reviews[K][T] == True)
solver.add(reviews[O][T] == True)

# Constraint 5: Exactly two students review exactly the same plays as each other
# This means exactly one pair has same_set=True, all other pairs have same_set=False
# Also, if two students share a set, the other three must all have different sets.
# The simplest encoding: exactly one pair is True.
solver.add(AtMost(*[same_set(i, j) for i in range(5) for j in range(i+1, 5)], 1))

# There must be at least one pair that matches
pairs = [same_set(i, j) for i in range(5) for j in range(i+1, 5)]
solver.add(Or(pairs))

# Now evaluate each option

# Helper: student reviews only Sunset
def only_sunset(student):
    return And(reviews[student][S] == True, reviews[student][T] == False, reviews[student][U] == False)

# Helper: student does NOT review only Sunset
def not_only_sunset(student):
    return Or(reviews[student][S] == False, reviews[student][T] == True, reviews[student][U] == True)

# Option A: Lopez
opt_a = And(
    only_sunset(L),
    not_only_sunset(J),
    not_only_sunset(K),
    not_only_sunset(M),
    not_only_sunset(O)
)

# Option B: O'Neill
opt_b = And(
    only_sunset(O),
    not_only_sunset(J),
    not_only_sunset(K),
    not_only_sunset(L),
    not_only_sunset(M)
)

# Option C: Jiang, Lopez
opt_c = And(
    only_sunset(J),
    only_sunset(L),
    not_only_sunset(K),
    not_only_sunset(M),
    not_only_sunset(O)
)

# Option D: Kramer, O'Neill
opt_d = And(
    only_sunset(K),
    only_sunset(O),
    not_only_sunset(J),
    not_only_sunset(L),
    not_only_sunset(M)
)

# Option E: Lopez, Megregian
opt_e = And(
    only_sunset(L),
    only_sunset(M),
    not_only_sunset(J),
    not_only_sunset(K),
    not_only_sunset(O)
)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        # Print model for debugging
        m = solver.model()
        print(f"Option {letter} is SAT")
        for i in range(5):
            plays_reviewed = []
            for p in range(3):
                if m.eval(reviews[i][p]):
                    plays_reviewed.append(["Sunset", "Tamerlane", "Undulation"][p])
            print(f"  {student_names[i]}: {plays_reviewed}")
    else:
        print(f"Option {letter} is UNSAT")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")