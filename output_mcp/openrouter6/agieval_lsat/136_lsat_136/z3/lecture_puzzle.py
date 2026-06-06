from z3 import *

solver = Solver()

# Bird types: 0=oystercatchers, 1=petrels, 2=rails, 3=sandpipers, 4=terns
birds = [Int(f'bird_{i}') for i in range(1,6)]
venues = [Int(f'venue_{i}') for i in range(1,6)]

# Domain constraints
for b in birds:
    solver.add(b >= 0, b <= 4)
for v in venues:
    solver.add(v >= 0, v <= 1)

# All birds distinct
solver.add(Distinct(birds))

# Base constraints from problem
# 1. First lecture in Gladwyn Hall (venue 0)
solver.add(venues[0] == 0)
# 2. Fourth lecture in Howard Auditorium (venue 1)
solver.add(venues[3] == 1)
# 3. Exactly three lectures in Gladwyn Hall
solver.add(Sum([If(v == 0, 1, 0) for v in venues]) == 3)

# 4. Sandpipers (3) in Howard and earlier than oystercatchers (0)
#    - Sandpipers in Howard
for i in range(5):
    solver.add(Implies(birds[i] == 3, venues[i] == 1))
#    - Sandpipers earlier than oystercatchers
for i in range(5):
    for j in range(5):
        solver.add(Implies(And(birds[i] == 3, birds[j] == 0), i < j))

# 5. Terns (4) earlier than petrels (1), and petrels in Gladwyn
#    - Petrels in Gladwyn
for i in range(5):
    solver.add(Implies(birds[i] == 1, venues[i] == 0))
#    - Terns earlier than petrels
for i in range(5):
    for j in range(5):
        solver.add(Implies(And(birds[i] == 4, birds[j] == 1), i < j))

# Additional condition: terns lecture is in Howard Auditorium (for the question)
for i in range(5):
    solver.add(Implies(birds[i] == 4, venues[i] == 1))

# Now test each answer choice about the third lecture (index 2)
options = [
    ("A", And(birds[2] == 0, venues[2] == 0)),   # oystercatchers and Gladwyn
    ("B", And(birds[2] == 2, venues[2] == 1)),   # rails and Howard
    ("C", And(birds[2] == 2, venues[2] == 0)),   # rails and Gladwyn
    ("D", And(birds[2] == 3, venues[2] == 1)),   # sandpipers and Howard
    ("E", And(birds[2] == 4, venues[2] == 1)),   # terns and Howard
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