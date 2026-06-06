from z3 import *

# Students and Plays
students = ['J', 'K', 'L', 'M', 'O']
plays = ['S', 'T', 'U']

# Variables: reviews[student][play]
reviews = {s: {p: Bool(f'rev_{s}_{p}') for p in plays} for s in students}

solver = Solver()

# Each student reviews 1, 2, or 3 plays
for s in students:
    count = Sum([If(reviews[s][p], 1, 0) for p in plays])
    solver.add(count >= 1)

# Kramer and Lopez each review fewer plays than Megregian
count_K = Sum([If(reviews['K'][p], 1, 0) for p in plays])
count_L = Sum([If(reviews['L'][p], 1, 0) for p in plays])
count_M = Sum([If(reviews['M'][p], 1, 0) for p in plays])
solver.add(count_K < count_M)
solver.add(count_L < count_M)

# Neither Lopez nor Megregian reviews any play Jiang reviews
for p in plays:
    solver.add(Not(And(reviews['L'][p], reviews['J'][p])))
    solver.add(Not(And(reviews['M'][p], reviews['J'][p])))

# Kramer and O'Neill both review Tamerlane
solver.add(reviews['K']['T'] == True)
solver.add(reviews['O']['T'] == True)

# Exactly three students review Undulation
solver.add(Sum([If(reviews[s]['U'], 1, 0) for s in students]) == 3)

# Exactly two of the students review exactly the same play or plays as each other
# Represent each student's set of plays as an integer (bitmask)
def get_set_id(s):
    return If(reviews[s]['S'], 1, 0) + \
           If(reviews[s]['T'], 2, 0) + \
           If(reviews[s]['U'], 4, 0)

set_ids = [get_set_id(s) for s in students]

# Count occurrences of each set_id
# Possible set_ids are 1 to 7 (0 is not possible as count >= 1)
# We need exactly one set_id to appear twice, and three others to appear once.
# This means there are 4 distinct set_ids used.
distinct_ids = [1, 2, 3, 4, 5, 6, 7]
counts = [Sum([If(set_ids[i] == d, 1, 0) for i in range(len(students))]) for d in distinct_ids]
solver.add(Sum([If(c == 2, 1, 0) for c in counts]) == 1)
solver.add(Sum([If(c == 1, 1, 0) for c in counts]) == 3)
solver.add(Sum([If(c > 2, 1, 0) for c in counts]) == 0)

# Options
options = [
    ("A", Not(reviews['M']['U'])),
    ("B", Not(reviews['O']['U'])),
    ("C", reviews['J']['U']),
    ("D", reviews['L']['T']),
    ("E", reviews['O']['S'])
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