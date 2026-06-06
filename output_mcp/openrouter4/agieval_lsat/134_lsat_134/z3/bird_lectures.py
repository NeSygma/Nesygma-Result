from z3 import *

solver = Solver()

# Birds: Oystercatchers=0, Petrels=1, Rails=2, Sandpipers=3, Terns=4
pos = [Int(f'pos_{i}') for i in range(5)]  # pos[0]=pos_O, pos[1]=pos_P, etc.

# Each bird is at a position from 1 to 5
for i in range(5):
    solver.add(pos[i] >= 1, pos[i] <= 5)

# All positions are distinct
solver.add(Distinct(pos))

# Location at each position (1-indexed for clarity): loc[i] corresponds to position i
loc = [None] + [Int(f'loc_{i}') for i in range(1, 6)]  # loc[1]..loc[5]
for i in range(1, 6):
    solver.add(loc[i] >= 0, loc[i] <= 1)

# Constraint 1: First lecture is in Gladwyn Hall
solver.add(loc[1] == 0)

# Constraint 2: Fourth lecture is in Howard Auditorium
solver.add(loc[4] == 1)

# Constraint 3: Exactly three lectures are in Gladwyn Hall
solver.add(Sum([If(loc[i] == 0, 1, 0) for i in range(1, 6)]) == 3)

# Constraint 4: Sandpipers (index 3) in Howard, earlier than Oystercatchers (index 0)
solver.add(Or([And(pos[3] == i, loc[i] == 1) for i in range(1, 6)]))
solver.add(pos[3] < pos[0])

# Constraint 5: Terns (index 4) earlier than Petrels (index 1), and Petrels in Gladwyn
solver.add(pos[4] < pos[1])
solver.add(Or([And(pos[1] == i, loc[i] == 0) for i in range(1, 6)]))

# Now evaluate each option
# Option A: oystercatchers, petrels, rails, sandpipers, terns
# pos[0]=1, pos[1]=2, pos[2]=3, pos[3]=4, pos[4]=5
opt_a = And(pos[0] == 1, pos[1] == 2, pos[2] == 3, pos[3] == 4, pos[4] == 5)

# Option B: petrels, sandpipers, oystercatchers, terns, rails
# pos[1]=1, pos[3]=2, pos[0]=3, pos[4]=4, pos[2]=5
opt_b = And(pos[1] == 1, pos[3] == 2, pos[0] == 3, pos[4] == 4, pos[2] == 5)

# Option C: rails, sandpipers, terns, petrels, oystercatchers
# pos[2]=1, pos[3]=2, pos[4]=3, pos[1]=4, pos[0]=5
opt_c = And(pos[2] == 1, pos[3] == 2, pos[4] == 3, pos[1] == 4, pos[0] == 5)

# Option D: sandpipers, terns, oystercatchers, rails, petrels
# pos[3]=1, pos[4]=2, pos[0]=3, pos[2]=4, pos[1]=5
opt_d = And(pos[3] == 1, pos[4] == 2, pos[0] == 3, pos[2] == 4, pos[1] == 5)

# Option E: terns, petrels, sandpipers, oystercatchers, rails
# pos[4]=1, pos[1]=2, pos[3]=3, pos[0]=4, pos[2]=5
opt_e = And(pos[4] == 1, pos[1] == 2, pos[3] == 3, pos[0] == 4, pos[2] == 5)

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