from z3 import *

# 0-indexed positions 0-4 (corresponding to 1st-5th)
# Birds: O(0), P(1), R(2), S(3), T(4)
# Locations: G(0), H(1)

bird = [Int(f'bird_{i}') for i in range(5)]
loc = [Int(f'loc_{i}') for i in range(5)]

solver = Solver()

# Domain constraints
for i in range(5):
    solver.add(And(bird[i] >= 0, bird[i] <= 4))
    solver.add(And(loc[i] >= 0, loc[i] <= 1))

# All birds are different (one per position)
solver.add(Distinct(bird))

# Constraint 1: First lecture (position 0) is in Gladwyn Hall (0)
solver.add(loc[0] == 0)

# Constraint 2: Fourth lecture (position 3) is in Howard Auditorium (1)
solver.add(loc[3] == 1)

# Constraint 3: Exactly three lectures are in Gladwyn Hall (0)
solver.add(Sum([If(loc[i] == 0, 1, 0) for i in range(5)]) == 3)

# Constraint 4: Sandpipers (3) is in Howard (1) and earlier than Oystercatchers (0)
# S is in H
for i in range(5):
    solver.add(Implies(bird[i] == 3, loc[i] == 1))
# S is earlier than O: for all i,j where bird[i]==S and bird[j]==O, i<j
for i in range(5):
    for j in range(5):
        solver.add(Implies(And(bird[i] == 3, bird[j] == 0), i < j))

# Constraint 5: Terns (4) is earlier than Petrels (1), and Petrels (1) is in Gladwyn (0)
# P is in G
for i in range(5):
    solver.add(Implies(bird[i] == 1, loc[i] == 0))
# T is earlier than P
for i in range(5):
    for j in range(5):
        solver.add(Implies(And(bird[i] == 4, bird[j] == 1), i < j))

# Additional condition: Terns (4) is in Howard (1)
for i in range(5):
    solver.add(Implies(bird[i] == 4, loc[i] == 1))

# Now evaluate each option - what could be true of the third lecture (position 2)?

# Option A: Third lecture (pos 2) is on oystercatchers (0) and is in Gladwyn Hall (0)
opt_a = And(bird[2] == 0, loc[2] == 0)

# Option B: Third lecture (pos 2) is on rails (2) and is in Howard Auditorium (1)
opt_b = And(bird[2] == 2, loc[2] == 1)

# Option C: Third lecture (pos 2) is on rails (2) and is in Gladwyn Hall (0)
opt_c = And(bird[2] == 2, loc[2] == 0)

# Option D: Third lecture (pos 2) is on sandpipers (3) and is in Howard Auditorium (1)
opt_d = And(bird[2] == 3, loc[2] == 1)

# Option E: Third lecture (pos 2) is on terns (4) and is in Howard Auditorium (1)
opt_e = And(bird[2] == 4, loc[2] == 1)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        # Print model for debugging
        m = solver.model()
        print(f"Option {letter} is possible. Model: birds={[m.eval(bird[i]) for i in range(5)]}, locs={[m.eval(loc[i]) for i in range(5)]}")
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