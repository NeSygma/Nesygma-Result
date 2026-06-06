from z3 import *

solver = Solver()

# Variables: position (1-5) for each bird type
# Bird types: oystercatchers, petrels, rails, sandpipers, terns
oystercatchers = Int('oystercatchers')
petrels = Int('petrels')
rails = Int('rails')
sandpipers = Int('sandpipers')
terns = Int('terns')

birds = [oystercatchers, petrels, rails, sandpipers, terns]

# Each bird is assigned to a position 1-5, all different
for b in birds:
    solver.add(b >= 1, b <= 5)
solver.add(Distinct(birds))

# Variables: location for each position (True = Gladwyn Hall, False = Howard Auditorium)
loc = [Bool(f'loc_{i}') for i in range(1, 6)]

# Constraint 1: The first lecture is in Gladwyn Hall
solver.add(loc[0] == True)

# Constraint 2: The fourth lecture is in Howard Auditorium
solver.add(loc[3] == False)

# Constraint 3: Exactly three of the lectures are in Gladwyn Hall
solver.add(Sum([If(loc[i], 1, 0) for i in range(5)]) == 3)

# Constraint 4: The lecture on sandpipers is in Howard Auditorium
# We need to express: location of sandpipers' position is Howard
# sandpipers is at position sandpipers, so loc[sandpipers-1] == False
# Use Or-loop pattern to avoid indexing with Z3 variable
solver.add(Or([And(sandpipers == i+1, loc[i] == False) for i in range(5)]))

# Constraint 5: sandpipers is given earlier than oystercatchers
solver.add(sandpipers < oystercatchers)

# Constraint 6: terns is given earlier than petrels
solver.add(terns < petrels)

# Constraint 7: petrels is in Gladwyn Hall
solver.add(Or([And(petrels == i+1, loc[i] == True) for i in range(5)]))

# Now evaluate each option for the fifth lecture
# Option A: It is on oystercatchers and is in Gladwyn Hall
opt_a = And(oystercatchers == 5, loc[4] == True)

# Option B: It is on petrels and is in Howard Auditorium
opt_b = And(petrels == 5, loc[4] == False)

# Option C: It is on rails and is in Howard Auditorium
opt_c = And(rails == 5, loc[4] == False)

# Option D: It is on sandpipers and is in Howard Auditorium
opt_d = And(sandpipers == 5, loc[4] == False)

# Option E: It is on terns and is in Gladwyn Hall
opt_e = And(terns == 5, loc[4] == True)

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