from z3 import *

solver = Solver()

# Birds: oystercatchers=0, petrels=1, rails=2, sandpipers=3, terns=4
# Positions: 1..5 (first to fifth)
# Halls: G=0 (Gladwyn), H=1 (Howard)

birds = [Int(f'bird_{i}') for i in range(5)]  # bird at position i
halls = [Int(f'hall_{i}') for i in range(5)]  # hall at position i

# Each bird appears exactly once (permutation of 0..4)
solver.add(Distinct(birds))
for i in range(5):
    solver.add(birds[i] >= 0, birds[i] <= 4)
    solver.add(Or(halls[i] == 0, halls[i] == 1))

# Condition 1: First lecture is in Gladwyn Hall
solver.add(halls[0] == 0)

# Condition 2: Fourth lecture is in Howard Auditorium
solver.add(halls[3] == 1)

# Condition 3: Exactly three lectures in Gladwyn Hall
solver.add(Sum([If(halls[i] == 0, 1, 0) for i in range(5)]) == 3)

# Condition 4: Sandpipers (3) is in Howard and earlier than oystercatchers (0)
# Find position of sandpipers and oystercatchers
sand_pos = Int('sand_pos')
oyst_pos = Int('oyst_pos')
for i in range(5):
    solver.add(Implies(birds[i] == 3, sand_pos == i))
    solver.add(Implies(birds[i] == 0, oyst_pos == i))
solver.add(sand_pos < oyst_pos)
# Sandpipers in Howard
solver.add(Or([And(birds[i] == 3, halls[i] == 1) for i in range(5)]))

# Condition 5: Terns (4) earlier than petrels (1), petrels in Gladwyn
tern_pos = Int('tern_pos')
petr_pos = Int('petr_pos')
for i in range(5):
    solver.add(Implies(birds[i] == 4, tern_pos == i))
    solver.add(Implies(birds[i] == 1, petr_pos == i))
solver.add(tern_pos < petr_pos)
# Petrels in Gladwyn
solver.add(Or([And(birds[i] == 1, halls[i] == 0) for i in range(5)]))

# Define each option as a constraint on the bird ordering
# (A) oystercatchers, petrels, rails, sandpipers, terns
opt_a = And(birds[0]==0, birds[1]==1, birds[2]==2, birds[3]==3, birds[4]==4)
# (B) petrels, sandpipers, oystercatchers, terns, rails
opt_b = And(birds[0]==1, birds[1]==3, birds[2]==0, birds[3]==4, birds[4]==2)
# (C) rails, sandpipers, terns, petrels, oystercatchers
opt_c = And(birds[0]==2, birds[1]==3, birds[2]==4, birds[3]==1, birds[4]==0)
# (D) sandpipers, terns, oystercatchers, rails, petrels
opt_d = And(birds[0]==3, birds[1]==4, birds[2]==0, birds[3]==2, birds[4]==1)
# (E) terns, petrels, sandpipers, oystercatchers, rails
opt_e = And(birds[0]==4, birds[1]==1, birds[2]==3, birds[3]==0, birds[4]==2)

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