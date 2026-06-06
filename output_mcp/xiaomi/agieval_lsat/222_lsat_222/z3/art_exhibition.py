from z3 import *

solver = Solver()

# Define the 8 painting slots: each painting is identified by (student, type)
# Students: F=Franz, G=Greene, H=Hidalgo, I=Isaacs
# Types: O=oil, W=watercolor
# We'll assign each painting to a (wall, position) pair
# Walls: 1,2,3,4; Positions: U=upper(0), L=lower(1)

# Variables: for each painting, which wall and position
# wall[student][type] = wall number (1-4)
# pos[student][type] = position (0=upper, 1=lower)

students = ['F', 'G', 'H', 'I']
types = ['O', 'W']

wall = {}
pos = {}
for s in students:
    for t in types:
        wall[s,t] = Int(f'wall_{s}_{t}')
        pos[s,t] = Int(f'pos_{s}_{t}')
        solver.add(wall[s,t] >= 1, wall[s,t] <= 4)
        solver.add(pos[s,t] >= 0, pos[s,t] <= 1)

# Each wall has exactly 2 paintings (one upper, one lower)
# So each (wall, position) pair has exactly one painting
for w in range(1, 5):
    for p in range(2):
        # Exactly one painting at this wall/position
        paintings_here = [And(wall[s,t] == w, pos[s,t] == p) for s in students for t in types]
        solver.add(Or(paintings_here))  # at least one
        # At most one: pairwise exclusion
        for i in range(len(paintings_here)):
            for j in range(i+1, len(paintings_here)):
                solver.add(Not(And(paintings_here[i], paintings_here[j])))

# Constraint 1: No wall has only watercolors
# Each wall must have at least one oil painting
for w in range(1, 5):
    solver.add(Or([And(wall[s,'O'] == w) for s in students]))

# Constraint 2: No wall has work of only one student
# Each wall must have paintings from at least 2 different students
for w in range(1, 5):
    # For each student, check if they have any painting on wall w
    student_on_wall = {}
    for s in students:
        student_on_wall[s] = Or(wall[s,'O'] == w, wall[s,'W'] == w)
    # At least 2 students must be on this wall
    # We can enforce: not all paintings from same student
    # More precisely: there exist two different students both on wall w
    pairs = []
    for i in range(len(students)):
        for j in range(i+1, len(students)):
            pairs.append(And(student_on_wall[students[i]], student_on_wall[students[j]]))
    solver.add(Or(pairs))

# Constraint 3: No wall has both Franz and Isaacs
for w in range(1, 5):
    franz_on_w = Or(wall['F','O'] == w, wall['F','W'] == w)
    isaacs_on_w = Or(wall['I','O'] == w, wall['I','W'] == w)
    solver.add(Not(And(franz_on_w, isaacs_on_w)))

# Constraint 4: Greene's watercolor is in the upper position of the wall where Franz's oil is
solver.add(wall['G','W'] == wall['F','O'])
solver.add(pos['G','W'] == 0)  # upper position

# Constraint 5: Isaacs's oil is in the lower position of wall 4
solver.add(wall['I','O'] == 4)
solver.add(pos['I','O'] == 1)  # lower position

# Constraint 6 (additional): Greene's oil is on the same wall as Franz's watercolor
solver.add(wall['G','O'] == wall['F','W'])

# Now evaluate each answer choice
# (A) Greene's oil is displayed in an upper position.
opt_a = (pos['G','O'] == 0)

# (B) Hidalgo's watercolor is displayed on the same wall as Isaacs's watercolor.
opt_b = (wall['H','W'] == wall['I','W'])

# (C) Hidalgo's oil is displayed in an upper position.
opt_c = (pos['H','O'] == 0)

# (D) Hidalgo's oil is displayed on the same wall as Isaacs's watercolor.
opt_d = (wall['H','O'] == wall['I','W'])

# (E) Isaacs's watercolor is displayed in a lower position.
opt_e = (pos['I','W'] == 1)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT. Sample assignment:")
        for s in students:
            for t in types:
                w_val = m[wall[s,t]].as_long()
                p_val = m[pos[s,t]].as_long()
                print(f"  {s}'s {t}: wall {w_val}, {'upper' if p_val==0 else 'lower'}")
    else:
        print(f"Option {letter} is UNSAT.")
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