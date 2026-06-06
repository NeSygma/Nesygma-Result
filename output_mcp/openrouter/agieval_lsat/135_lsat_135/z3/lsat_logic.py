from z3 import *

solver = Solver()

# Variables: positions of each bird (1..5)
pos_oyst = Int('pos_oyst')
pos_pet = Int('pos_pet')
pos_rail = Int('pos_rail')
pos_sand = Int('pos_sand')
pos_tern = Int('pos_tern')
positions = [pos_oyst, pos_pet, pos_rail, pos_sand, pos_tern]
for p in positions:
    solver.add(p >= 1, p <= 5)
# all distinct
solver.add(Distinct(positions))

# Location booleans for each lecture position (True = Gladwyn, False = Howard)
G = [Bool(f'G_{i}') for i in range(5)]  # indices 0..4 correspond to positions 1..5
# First lecture in Gladwyn Hall
solver.add(G[0] == True)
# Fourth lecture in Howard Auditorium
solver.add(G[3] == False)
# Exactly three lectures in Gladwyn Hall
solver.add(Sum([If(g, 1, 0) for g in G]) == 3)

# Sandpipers in Howard and earlier than Oystercatchers
# location constraint for sandpipers: G[pos_sand-1] == False
for i in range(1,6):
    solver.add(Implies(pos_sand == i, G[i-1] == False))
# order constraint
solver.add(pos_sand < pos_oyst)

# Terns earlier than Petrels, and Petrels in Gladwyn
for i in range(1,6):
    solver.add(Implies(pos_pet == i, G[i-1] == True))
solver.add(pos_tern < pos_pet)

# Define option constraints
opt_a = And(G[0] == True, G[1] == True)  # first and second both Gladwyn
opt_b = And(G[1] == False, G[2] == False)  # second and third both Howard
opt_c = And(G[1] == True, G[4] == True)   # second and fifth both Gladwyn
opt_d = And(G[2] == False, G[3] == False) # third and fourth both Howard
opt_e = And(G[2] == True, G[4] == True)   # third and fifth both Gladwyn

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