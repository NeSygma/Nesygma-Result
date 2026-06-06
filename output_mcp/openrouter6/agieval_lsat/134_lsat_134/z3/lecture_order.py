from z3 import *

solver = Solver()

# Declare position variables for each bird
pos_O = Int('pos_O')  # oystercatchers
pos_P = Int('pos_P')  # petrels
pos_R = Int('pos_R')  # rails
pos_S = Int('pos_S')  # sandpipers
pos_T = Int('pos_T')  # terns

# Domain constraints: positions between 1 and 5
solver.add(pos_O >= 1, pos_O <= 5)
solver.add(pos_P >= 1, pos_P <= 5)
solver.add(pos_R >= 1, pos_R <= 5)
solver.add(pos_S >= 1, pos_S <= 5)
solver.add(pos_T >= 1, pos_T <= 5)

# All positions distinct
solver.add(Distinct([pos_O, pos_P, pos_R, pos_S, pos_T]))

# Venue array: indexed by position (1..5), value True for Howard, False for Gladwyn
venue = Array('venue', IntSort(), BoolSort())

# Constraint 1: First lecture in Gladwyn Hall
solver.add(venue[1] == False)

# Constraint 2: Fourth lecture in Howard Auditorium
solver.add(venue[4] == True)

# Constraint 3: Exactly three lectures in Gladwyn Hall
# Count positions where venue is False (Gladwyn)
gladwyn_count = Sum([If(venue[i], 0, 1) for i in range(1, 6)])
solver.add(gladwyn_count == 3)

# Constraint 4: Sandpipers in Howard and earlier than oystercatchers
solver.add(venue[pos_S] == True)
solver.add(pos_S < pos_O)

# Constraint 5: Terns earlier than petrels, and petrels in Gladwyn
solver.add(pos_T < pos_P)
solver.add(venue[pos_P] == False)

# Now evaluate each answer choice
found_options = []

# Option A: oystercatchers, petrels, rails, sandpipers, terns
solver.push()
solver.add(pos_O == 1, pos_P == 2, pos_R == 3, pos_S == 4, pos_T == 5)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: petrels, sandpipers, oystercatchers, terns, rails
solver.push()
solver.add(pos_P == 1, pos_S == 2, pos_O == 3, pos_T == 4, pos_R == 5)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: rails, sandpipers, terns, petrels, oystercatchers
solver.push()
solver.add(pos_R == 1, pos_S == 2, pos_T == 3, pos_P == 4, pos_O == 5)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: sandpipers, terns, oystercatchers, rails, petrels
solver.push()
solver.add(pos_S == 1, pos_T == 2, pos_O == 3, pos_R == 4, pos_P == 5)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: terns, petrels, sandpipers, oystercatchers, rails
solver.push()
solver.add(pos_T == 1, pos_P == 2, pos_S == 3, pos_O == 4, pos_R == 5)
if solver.check() == sat:
    found_options.append('E')
solver.pop()

# Output result according to the required logic
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")