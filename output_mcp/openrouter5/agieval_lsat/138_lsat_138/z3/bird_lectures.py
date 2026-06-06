from z3 import *

solver = Solver()

# 5 lectures, positions 1..5
# Birds: oystercatchers (O), petrels (P), rails (R), sandpipers (S), terns (T)
# Locations: Gladwyn Hall (G), Howard Auditorium (H)

# We'll use integer variables for each position: bird at position i, location at position i
bird = [Int(f"bird_{i}") for i in range(1, 6)]  # 1..5
loc = [Int(f"loc_{i}") for i in range(1, 6)]    # 1..5

# Domains
for i in range(1, 6):
    solver.add(bird[i-1] >= 0, bird[i-1] <= 4)  # 0=O, 1=P, 2=R, 3=S, 4=T
    solver.add(loc[i-1] >= 0, loc[i-1] <= 1)    # 0=G, 1=H

# All birds distinct
solver.add(Distinct(bird))

# Condition 1: The first lecture is in Gladwyn Hall.
solver.add(loc[0] == 0)  # G

# Condition 2: The fourth lecture is in Howard Auditorium.
solver.add(loc[3] == 1)  # H

# Condition 3: Exactly three of the lectures are in Gladwyn Hall.
solver.add(Sum([If(loc[i] == 0, 1, 0) for i in range(5)]) == 3)

# Condition 4: The lecture on sandpipers is in Howard Auditorium and is given earlier than the lecture on oystercatchers.
# sandpipers = 3, oystercatchers = 0
# Find position of sandpipers and oystercatchers
pos_S = Int('pos_S')
pos_O = Int('pos_O')
solver.add(Or([And(bird[i] == 3, pos_S == i+1) for i in range(5)]))
solver.add(Or([And(bird[i] == 0, pos_O == i+1) for i in range(5)]))
solver.add(pos_S < pos_O)
# sandpipers in Howard
solver.add(Or([And(bird[i] == 3, loc[i] == 1) for i in range(5)]))

# Condition 5: The lecture on terns is given earlier than the lecture on petrels, which is in Gladwyn Hall.
# terns = 4, petrels = 1
pos_T = Int('pos_T')
pos_P = Int('pos_P')
solver.add(Or([And(bird[i] == 4, pos_T == i+1) for i in range(5)]))
solver.add(Or([And(bird[i] == 1, pos_P == i+1) for i in range(5)]))
solver.add(pos_T < pos_P)
# petrels in Gladwyn
solver.add(Or([And(bird[i] == 1, loc[i] == 0) for i in range(5)]))

# Additional condition from the question: The third lecture is on sandpipers.
solver.add(bird[2] == 3)  # position 3 is sandpipers

# Now evaluate each option

# Option A: The second lecture is on oystercatchers and is in Gladwyn Hall.
opt_a = And(bird[1] == 0, loc[1] == 0)

# Option B: The fifth lecture is on oystercatchers and is in Howard Auditorium.
opt_b = And(bird[4] == 0, loc[4] == 1)

# Option C: The second lecture is on rails and is in Howard Auditorium.
opt_c = And(bird[1] == 2, loc[1] == 1)

# Option D: The second lecture is on terns and is in Gladwyn Hall.
opt_d = And(bird[1] == 4, loc[1] == 0)

# Option E: The fourth lecture is on terns and is in Howard Auditorium.
opt_e = And(bird[3] == 4, loc[3] == 1)

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