from z3 import *

solver = Solver()

# Positions 1-5
# bird[i] = which bird type at position i (0=oystercatchers, 1=petrels, 2=rails, 3=sandpipers, 4=terns)
# hall[i] = which hall at position i (0=Gladwyn, 1=Howard)

bird = [Int(f'bird_{i}') for i in range(1, 6)]
hall = [Int(f'hall_{i}') for i in range(1, 6)]

# Each bird is 0-4, all different
for i in range(5):
    solver.add(bird[i] >= 0, bird[i] <= 4)
solver.add(Distinct(bird))

# Each hall is 0 or 1
for i in range(5):
    solver.add(Or(hall[i] == 0, hall[i] == 1))

# Condition 1: First lecture is in Gladwyn Hall
solver.add(hall[0] == 0)

# Condition 2: Fourth lecture is in Howard Auditorium
solver.add(hall[3] == 1)

# Condition 3: Exactly three lectures in Gladwyn Hall
solver.add(Sum([If(hall[i] == 0, 1, 0) for i in range(5)]) == 3)

# Condition 4: Sandpipers (3) is in Howard and earlier than oystercatchers (0)
# Find position of sandpipers and oystercatchers
sand_pos = Int('sand_pos')
oyst_pos = Int('oyst_pos')
solver.add(Or([And(bird[i] == 3, sand_pos == i+1) for i in range(5)]))
solver.add(Or([And(bird[i] == 0, oyst_pos == i+1) for i in range(5)]))
solver.add(sand_pos < oyst_pos)

# Sandpipers is in Howard
solver.add(Or([And(bird[i] == 3, hall[i] == 1) for i in range(5)]))

# Condition 5: Terns (4) earlier than petrels (1), and petrels in Gladwyn
tern_pos = Int('tern_pos')
petr_pos = Int('petr_pos')
solver.add(Or([And(bird[i] == 4, tern_pos == i+1) for i in range(5)]))
solver.add(Or([And(bird[i] == 1, petr_pos == i+1) for i in range(5)]))
solver.add(tern_pos < petr_pos)

# Petrels in Gladwyn
solver.add(Or([And(bird[i] == 1, hall[i] == 0) for i in range(5)]))

# Now evaluate each option for the 5th lecture (index 4)
# (A) oystercatchers in Gladwyn Hall
opt_a = And(bird[4] == 0, hall[4] == 0)
# (B) petrels in Howard Auditorium
opt_b = And(bird[4] == 1, hall[4] == 1)
# (C) rails in Howard Auditorium
opt_c = And(bird[4] == 2, hall[4] == 1)
# (D) sandpipers in Howard Auditorium
opt_d = And(bird[4] == 3, hall[4] == 1)
# (E) terns in Gladwyn Hall
opt_e = And(bird[4] == 4, hall[4] == 0)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for i in range(5):
            bird_names = ['oystercatchers', 'petrels', 'rails', 'sandpipers', 'terns']
            hall_names = ['Gladwyn', 'Howard']
            bv = m[bird[i]].as_long()
            hv = m[hall[i]].as_long()
            print(f"  Lecture {i+1}: {bird_names[bv]} in {hall_names[hv]}")
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