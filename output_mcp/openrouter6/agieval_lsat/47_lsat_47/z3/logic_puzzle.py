from z3 import *

solver = Solver()

# Define students and plays
students = ['Jiang', 'Kramer', 'Lopez', 'Megregian', 'O\'Neill']
plays = ['Sunset', 'Tamerlane', 'Undulation']

# Create Boolean variables for each student-play pair
vars = {}
for s in students:
    for p in plays:
        vars[(s, p)] = Bool(f'{s}_{p}')

# Helper to get list of three Booleans for a student
def student_vars(s):
    return [vars[(s, p)] for p in plays]

# Each student reviews at least one play
for s in students:
    solver.add(Or(student_vars(s)))

# Condition 3: Kramer and O'Neill both review Tamerlane
solver.add(vars[('Kramer', 'Tamerlane')])
solver.add(vars[('O\'Neill', 'Tamerlane')])

# Additional premise: Jiang does not review Tamerlane
solver.add(Not(vars[('Jiang', 'Tamerlane')]))

# Condition 2: Neither Lopez nor Megregian reviews any play Jiang reviews
for p in plays:
    solver.add(Implies(vars[('Jiang', p)], Not(vars[('Lopez', p)])))
    solver.add(Implies(vars[('Jiang', p)], Not(vars[('Megregian', p)])))

# Condition 1: Kramer and Lopez each review fewer plays than Megregian
def count(student):
    return Sum([If(vars[(student, p)], 1, 0) for p in plays])

count_K = count('Kramer')
count_L = count('Lopez')
count_M = count('Megregian')
solver.add(count_K < count_M)
solver.add(count_L < count_M)

# Exactly two students review exactly the same play or plays as each other
# Enumerate all pairs of students
pairs = []
for i in range(len(students)):
    for j in range(i+1, len(students)):
        s1 = students[i]
        s2 = students[j]
        eq = And([vars[(s1, p)] == vars[(s2, p)] for p in plays])
        pairs.append(eq)

# Exactly one pair must be equal
solver.add(Sum([If(eq, 1, 0) for eq in pairs]) == 1)

# Now evaluate multiple choice options
found_options = []
options = [
    ('A', vars[('Jiang', 'Sunset')]),
    ('B', vars[('Lopez', 'Undulation')]),
    ('C', vars[('Megregian', 'Sunset')]),
    ('D', vars[('Megregian', 'Tamerlane')]),
    ('E', vars[('O\'Neill', 'Undulation')])
]

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