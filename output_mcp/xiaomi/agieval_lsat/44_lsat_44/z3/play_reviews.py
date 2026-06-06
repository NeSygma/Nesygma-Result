from z3 import *

solver = Solver()

# Define the plays
plays = ['S', 'T', 'U']  # Sunset, Tamerlane, Undulation
students = ['J', 'K', 'L', 'M', 'O']  # Jiang, Kramer, Lopez, Megregian, O'Neill

# For each student, define whether they review each play (Bool)
review = {}
for s in students:
    for p in plays:
        review[(s, p)] = Bool(f'review_{s}_{p}')

# Each student reviews at least one play
for s in students:
    solver.add(Or([review[(s, p)] for p in plays]))

# Count of plays reviewed by each student
count = {}
for s in students:
    count[s] = Sum([If(review[(s, p)], 1, 0) for p in plays])

# Condition 1: Kramer and Lopez each review fewer plays than Megregian
solver.add(count['K'] < count['M'])
solver.add(count['L'] < count['M'])

# Condition 2: Neither Lopez nor Megregian reviews any play Jiang reviews
for p in plays:
    solver.add(Implies(review[('J', p)], Not(review[('L', p)])))
    solver.add(Implies(review[('J', p)], Not(review[('M', p)])))

# Condition 3: Kramer and O'Neill both review Tamerlane
solver.add(review[('K', 'T')] == True)
solver.add(review[('O', 'T')] == True)

# Condition 4: Exactly two of the students review exactly the same play or plays as each other
# This means exactly one pair of students has identical review sets, and all other pairs differ
def same_reviews(s1, s2):
    return And([review[(s1, p)] == review[(s2, p)] for p in plays])

pairs = []
for i in range(len(students)):
    for j in range(i+1, len(students)):
        pairs.append((students[i], students[j]))

pair_same = [same_reviews(s1, s2) for (s1, s2) in pairs]
solver.add(Sum([If(ps, 1, 0) for ps in pair_same]) == 1)

# Now evaluate each answer choice
# (A) Jiang reviews more plays than Lopez
opt_a = count['J'] > count['L']
# (B) Megregian reviews more plays than Jiang
opt_b = count['M'] > count['J']
# (C) Megregian reviews more plays than O'Neill
opt_c = count['M'] > count['O']
# (D) O'Neill reviews more plays than Jiang
opt_d = count['O'] > count['J']
# (E) O'Neill reviews more plays than Kramer
opt_e = count['O'] > count['K']

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