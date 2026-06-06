from z3 import *

solver = Solver()

# Students: Franz (F), Greene (G), Hidalgo (H), Isaacs (I)
# Each student has exactly two paintings: an oil and a watercolor
# Walls: 1, 2, 3, 4. Each wall has upper and lower position.
# So we have 8 paintings total: each student's oil and watercolor.

# Let's model each painting's wall and position.
# We'll use integer variables for wall (1-4) and position (0=upper, 1=lower).

# For each student, we have two paintings: oil and watercolor
# Variables: wall_F_oil, pos_F_oil, wall_F_wc, pos_F_wc, etc.

students = ['F', 'G', 'H', 'I']
types = ['oil', 'wc']  # watercolor

# Wall and position for each painting
wall = {}
pos = {}
for s in students:
    for t in types:
        wall[(s, t)] = Int(f'wall_{s}_{t}')
        pos[(s, t)] = Int(f'pos_{s}_{t}')

# Domain constraints: walls 1-4, positions 0 (upper) or 1 (lower)
for s in students:
    for t in types:
        solver.add(wall[(s, t)] >= 1, wall[(s, t)] <= 4)
        solver.add(pos[(s, t)] >= 0, pos[(s, t)] <= 1)

# Each student displays exactly two paintings (already encoded by having exactly one oil and one wc)

# Exactly two paintings on each wall (one upper, one lower)
# So for each wall w, exactly two paintings have wall = w, one with pos=0 and one with pos=1
for w in range(1, 5):
    # Count paintings on wall w
    count_on_wall = Sum([If(wall[(s, t)] == w, 1, 0) for s in students for t in types])
    solver.add(count_on_wall == 2)
    # Exactly one upper on wall w
    count_upper = Sum([If(And(wall[(s, t)] == w, pos[(s, t)] == 0), 1, 0) for s in students for t in types])
    solver.add(count_upper == 1)
    # Exactly one lower on wall w
    count_lower = Sum([If(And(wall[(s, t)] == w, pos[(s, t)] == 1), 1, 0) for s in students for t in types])
    solver.add(count_lower == 1)

# Condition 1: No wall has only watercolors displayed on it.
# i.e., every wall has at least one oil painting.
for w in range(1, 5):
    has_oil = Or([And(wall[(s, 'oil')] == w) for s in students])
    solver.add(has_oil)

# Condition 2: No wall has the work of only one student displayed on it.
# i.e., every wall has paintings from at least two different students.
for w in range(1, 5):
    # Count distinct students on wall w
    # For each student, check if they have at least one painting on wall w
    student_on_wall = [Or([And(wall[(s, t)] == w) for t in types]) for s in students]
    # At least two students on each wall
    solver.add(Sum([If(stu, 1, 0) for stu in student_on_wall]) >= 2)

# Condition 3: No wall has both a painting by Franz and a painting by Isaacs displayed on it.
for w in range(1, 5):
    franz_on_w = Or([And(wall[('F', t)] == w) for t in types])
    isaacs_on_w = Or([And(wall[('I', t)] == w) for t in types])
    solver.add(Not(And(franz_on_w, isaacs_on_w)))

# Condition 4: Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed.
# So: wall(G, wc) = wall(F, oil) AND pos(G, wc) = 0
solver.add(wall[('G', 'wc')] == wall[('F', 'oil')])
solver.add(pos[('G', 'wc')] == 0)

# Condition 5: Isaacs's oil is displayed in the lower position of wall 4.
solver.add(wall[('I', 'oil')] == 4)
solver.add(pos[('I', 'oil')] == 1)

# Additional constraint from the question: Hidalgo's oil is displayed on wall 2.
solver.add(wall[('H', 'oil')] == 2)

# Now evaluate each option: which painting could ALSO be on wall 2?
# Options:
# (A) Franz's oil
# (B) Greene's watercolor
# (C) Greene's oil
# (D) Hidalgo's watercolor
# (E) Isaacs's watercolor

# For each option, we add the constraint that the given painting is on wall 2,
# and check if the whole system is satisfiable.

options = [
    ("A", wall[('F', 'oil')] == 2),
    ("B", wall[('G', 'wc')] == 2),
    ("C", wall[('G', 'oil')] == 2),
    ("D", wall[('H', 'wc')] == 2),
    ("E", wall[('I', 'wc')] == 2),
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