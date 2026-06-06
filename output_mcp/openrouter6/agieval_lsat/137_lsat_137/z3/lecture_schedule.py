from z3 import *

solver = Solver()

# Bird types: oystercatchers (O), petrels (P), rails (R), sandpipers (S), terns (T)
pos_O = Int('pos_O')
pos_P = Int('pos_P')
pos_R = Int('pos_R')
pos_S = Int('pos_S')
pos_T = Int('pos_T')

venue_O = Bool('venue_O')
venue_P = Bool('venue_P')
venue_R = Bool('venue_R')
venue_S = Bool('venue_S')
venue_T = Bool('venue_T')

# Positions are between 1 and 5
solver.add(pos_O >= 1, pos_O <= 5)
solver.add(pos_P >= 1, pos_P <= 5)
solver.add(pos_R >= 1, pos_R <= 5)
solver.add(pos_S >= 1, pos_S <= 5)
solver.add(pos_T >= 1, pos_T <= 5)

# All positions distinct
solver.add(Distinct([pos_O, pos_P, pos_R, pos_S, pos_T]))

# First lecture in Gladwyn Hall (True)
# For each bird, if its position is 1, then its venue is True
solver.add(Implies(pos_O == 1, venue_O == True))
solver.add(Implies(pos_P == 1, venue_P == True))
solver.add(Implies(pos_R == 1, venue_R == True))
solver.add(Implies(pos_S == 1, venue_S == True))
solver.add(Implies(pos_T == 1, venue_T == True))

# Fourth lecture in Howard Auditorium (False)
solver.add(Implies(pos_O == 4, venue_O == False))
solver.add(Implies(pos_P == 4, venue_P == False))
solver.add(Implies(pos_R == 4, venue_R == False))
solver.add(Implies(pos_S == 4, venue_S == False))
solver.add(Implies(pos_T == 4, venue_T == False))

# Exactly three lectures in Gladwyn Hall
venues = [venue_O, venue_P, venue_R, venue_S, venue_T]
solver.add(Sum([If(v, 1, 0) for v in venues]) == 3)

# Sandpipers in Howard Auditorium and earlier than oystercatchers
solver.add(venue_S == False)
solver.add(pos_S < pos_O)

# Terns earlier than petrels, and petrels in Gladwyn Hall
solver.add(pos_T < pos_P)
solver.add(venue_P == True)

# Now test each option for the fifth lecture
found_options = []

# Option A: oystercatchers in Gladwyn Hall at position 5
opt_a = And(pos_O == 5, venue_O == True)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: petrels in Howard Auditorium at position 5
opt_b = And(pos_P == 5, venue_P == False)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: rails in Howard Auditorium at position 5
opt_c = And(pos_R == 5, venue_R == False)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: sandpipers in Howard Auditorium at position 5
opt_d = And(pos_S == 5, venue_S == False)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: terns in Gladwyn Hall at position 5
opt_e = And(pos_T == 5, venue_T == True)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append('E')
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")