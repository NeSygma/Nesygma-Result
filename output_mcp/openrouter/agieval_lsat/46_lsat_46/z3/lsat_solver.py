from z3 import *

# Students indices
J, K, L, M, O = range(5)
# Plays indices: 0 Sunset, 1 Tamerlane, 2 Undulation
plays = range(3)

# Create Bool variables rev[student][play]
rev = [[Bool(f"rev_{s}_{p}") for p in plays] for s in range(5)]

solver = Solver()

# Each student reviews at least one play
for s in range(5):
    solver.add(Or([rev[s][p] for p in plays]))

# Constraint: Kramer and O'Neill both review Tamerlane (play 1)
solver.add(rev[K][1] == True)
solver.add(rev[O][1] == True)

# Constraint 1: Kramer and Lopez each review fewer plays than Megregian
solver.add(Sum([If(rev[K][p], 1, 0) for p in plays]) < Sum([If(rev[M][p], 1, 0) for p in plays]))
solver.add(Sum([If(rev[L][p], 1, 0) for p in plays]) < Sum([If(rev[M][p], 1, 0) for p in plays]))

# Constraint 2: Neither Lopez nor Megregian reviews any play Jiang reviews
for p in plays:
    solver.add(Implies(rev[J][p], Not(rev[L][p])))
    solver.add(Implies(rev[J][p], Not(rev[M][p])))

# Constraint 4: Exactly one pair of students have identical review sets
pair_eq = []
for i in range(5):
    for j in range(i+1,5):
        eq_ij = And([rev[i][p] == rev[j][p] for p in plays])
        pair_eq.append(eq_ij)
# Exactly one equality true
solver.add(Sum([If(eq, 1, 0) for eq in pair_eq]) == 1)

# Define option constraints for Tamerlane reviewers
options = {}
# A: Jiang, Kramer
options['A'] = And(
    rev[J][1] == True,
    rev[K][1] == True,
    rev[L][1] == False,
    rev[M][1] == False,
    rev[O][1] == False
)
# B: Kramer, O'Neill
options['B'] = And(
    rev[J][1] == False,
    rev[K][1] == True,
    rev[L][1] == False,
    rev[M][1] == False,
    rev[O][1] == True
)
# C: Kramer, Lopez, O'Neill
options['C'] = And(
    rev[J][1] == False,
    rev[K][1] == True,
    rev[L][1] == True,
    rev[M][1] == False,
    rev[O][1] == True
)
# D: Kramer, Megregian, O'Neill
options['D'] = And(
    rev[J][1] == False,
    rev[K][1] == True,
    rev[L][1] == False,
    rev[M][1] == True,
    rev[O][1] == True
)
# E: Lopez, Megregian, O'Neill
options['E'] = And(
    rev[J][1] == False,
    rev[K][1] == False,
    rev[L][1] == True,
    rev[M][1] == True,
    rev[O][1] == True
)

found_options = []
for letter, constr in [("A", options['A']), ("B", options['B']), ("C", options['C']), ("D", options['D']), ("E", options['E'])]:
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