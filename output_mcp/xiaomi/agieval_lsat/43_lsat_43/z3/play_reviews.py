from z3 import *

# Define the students and plays
students = ['Jiang', 'Kramer', 'Lopez', 'Megregian', 'O\'Neill']
plays = ['Sunset', 'Tamerlane', 'Undulation']

# Create Boolean variables: reviews[s][p] = True if student s reviews play p
reviews = {}
for s in students:
    for p in plays:
        reviews[(s, p)] = Bool(f'reviews_{s}_{p}')

solver = Solver()

# Each student reviews at least one play
for s in students:
    solver.add(Or([reviews[(s, p)] for p in plays]))

# Condition 1: Kramer and Lopez each review fewer plays than Megregian
# Count plays per student
def count_plays(s):
    return Sum([If(reviews[(s, p)], 1, 0) for p in plays])

solver.add(count_plays('Kramer') < count_plays('Megregian'))
solver.add(count_plays('Lopez') < count_plays('Megregian'))

# Condition 2: Neither Lopez nor Megregian reviews any play Jiang reviews
for p in plays:
    solver.add(Implies(reviews[('Jiang', p)], Not(reviews[('Lopez', p)])))
    solver.add(Implies(reviews[('Jiang', p)], Not(reviews[('Megregian', p)])))

# Condition 3: Kramer and O'Neill both review Tamerlane
solver.add(reviews[('Kramer', 'Tamerlane')])
solver.add(reviews[('O\'Neill', 'Tamerlane')])

# Condition 4: Exactly two of the students review exactly the same play or plays as each other
# This means there is exactly one pair of students with identical review sets
# and all other pairs have different review sets
pair_same = []
for i in range(len(students)):
    for j in range(i+1, len(students)):
        s1, s2 = students[i], students[j]
        same = And([reviews[(s1, p)] == reviews[(s2, p)] for p in plays])
        pair_same.append(same)

# Exactly one pair is the same
solver.add(Sum([If(ps, 1, 0) for ps in pair_same]) == 1)

# Now evaluate each answer choice
# Each choice specifies which students review ONLY Sunset
# "only Sunset" means: reviews Sunset AND does NOT review Tamerlane AND does NOT review Undulation

def only_sunset(s):
    return And(reviews[(s, 'Sunset')], 
               Not(reviews[(s, 'Tamerlane')]), 
               Not(reviews[(s, 'Undulation')]))

# Option A: Lopez reviews only Sunset (and no other student reviews only Sunset)
opt_a = And(only_sunset('Lopez'),
            Not(only_sunset('Jiang')),
            Not(only_sunset('Kramer')),
            Not(only_sunset('Megregian')),
            Not(only_sunset('O\'Neill')))

# Option B: O'Neill reviews only Sunset (and no other student reviews only Sunset)
opt_b = And(only_sunset('O\'Neill'),
            Not(only_sunset('Jiang')),
            Not(only_sunset('Kramer')),
            Not(only_sunset('Lopez')),
            Not(only_sunset('Megregian')))

# Option C: Jiang and Lopez review only Sunset (and no other student reviews only Sunset)
opt_c = And(only_sunset('Jiang'),
            only_sunset('Lopez'),
            Not(only_sunset('Kramer')),
            Not(only_sunset('Megregian')),
            Not(only_sunset('O\'Neill')))

# Option D: Kramer and O'Neill review only Sunset (and no other student reviews only Sunset)
opt_d = And(only_sunset('Kramer'),
            only_sunset('O\'Neill'),
            Not(only_sunset('Jiang')),
            Not(only_sunset('Lopez')),
            Not(only_sunset('Megregian')))

# Option E: Lopez and Megregian review only Sunset (and no other student reviews only Sunset)
opt_e = And(only_sunset('Lopez'),
            only_sunset('Megregian'),
            Not(only_sunset('Jiang')),
            Not(only_sunset('Kramer')),
            Not(only_sunset('O\'Neill')))

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