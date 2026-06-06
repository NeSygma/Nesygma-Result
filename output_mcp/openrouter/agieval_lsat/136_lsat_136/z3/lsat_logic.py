from z3 import *

solver = Solver()

# Positions for each bird type: 1..5
pos_oyst = Int('pos_oyst')
pos_pet = Int('pos_pet')
pos_rail = Int('pos_rail')
pos_sand = Int('pos_sand')
pos_tern = Int('pos_tern')
positions = [pos_oyst, pos_pet, pos_rail, pos_sand, pos_tern]
for p in positions:
    solver.add(p >= 1, p <= 5)
solver.add(Distinct(positions))

# Location for each lecture position 1..5: True=Gladwyn, False=Howard
loc = [Bool(f'loc_{i}') for i in range(1,6)]  # loc[0] corresponds to position 1
# First lecture in Gladwyn Hall
solver.add(loc[0] == True)
# Fourth lecture in Howard Auditorium
solver.add(loc[3] == False)
# Exactly three Gladwyn lectures
solver.add(Sum([If(l, 1, 0) for l in loc]) == 3)

# Sandpipers in Howard and earlier than oystercatchers
solver.add(Or([And(pos_sand == i, loc[i-1] == False) for i in range(1,6)]))
solver.add(pos_sand < pos_oyst)

# Terns earlier than petrels, petrels in Gladwyn, terns in Howard (question condition)
solver.add(pos_tern < pos_pet)
solver.add(Or([And(pos_pet == i, loc[i-1] == True) for i in range(1,6)]))
solver.add(Or([And(pos_tern == i, loc[i-1] == False) for i in range(1,6)]))

# Options constraints for third lecture (position 3)
options = []
# A: third lecture is oystercatchers and Gladwyn
opt_a = And(pos_oyst == 3, loc[2] == True)
options.append(("A", opt_a))
# B: third lecture is rails and Howard
opt_b = And(pos_rail == 3, loc[2] == False)
options.append(("B", opt_b))
# C: third lecture is rails and Gladwyn
opt_c = And(pos_rail == 3, loc[2] == True)
options.append(("C", opt_c))
# D: third lecture is sandpipers and Howard
opt_d = And(pos_sand == 3, loc[2] == False)
options.append(("D", opt_d))
# E: third lecture is terns and Howard
opt_e = And(pos_tern == 3, loc[2] == False)
options.append(("E", opt_e))

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