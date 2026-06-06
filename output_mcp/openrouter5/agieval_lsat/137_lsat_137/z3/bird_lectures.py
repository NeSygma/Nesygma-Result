from z3 import *

solver = Solver()

# 5 lectures, positions 0..4 (1st=0, 2nd=1, 3rd=2, 4th=3, 5th=4)
# Birds: oystercatchers (O), petrels (P), rails (R), sandpipers (S), terns (T)
# Locations: Gladwyn Hall (G), Howard Auditorium (H)

# Variables: for each position, which bird and which location
bird = [Int(f'bird_{i}') for i in range(5)]
loc = [Int(f'loc_{i}') for i in range(5)]

# Bird domain: 0=O, 1=P, 2=R, 3=S, 4=T
for i in range(5):
    solver.add(bird[i] >= 0, bird[i] <= 4)

# Location domain: 0=Gladwyn, 1=Howard
for i in range(5):
    solver.add(loc[i] >= 0, loc[i] <= 1)

# All birds distinct
solver.add(Distinct(bird))

# The first lecture (position 0) is in Gladwyn Hall
solver.add(loc[0] == 0)

# The fourth lecture (position 3) is in Howard Auditorium
solver.add(loc[3] == 1)

# Exactly three of the lectures are in Gladwyn Hall
solver.add(Sum([If(loc[i] == 0, 1, 0) for i in range(5)]) == 3)

# The lecture on sandpipers (S=3) is in Howard Auditorium and is given earlier than the lecture on oystercatchers (O=0)
# sandpipers in Howard
solver.add(Or([And(bird[i] == 3, loc[i] == 1) for i in range(5)]))
# sandpipers earlier than oystercatchers
solver.add(Or([And(bird[i] == 3, bird[j] == 0, i < j) for i in range(5) for j in range(5)]))

# The lecture on terns (T=4) is given earlier than the lecture on petrels (P=1), which is in Gladwyn Hall
# petrels in Gladwyn
solver.add(Or([And(bird[i] == 1, loc[i] == 0) for i in range(5)]))
# terns earlier than petrels
solver.add(Or([And(bird[i] == 4, bird[j] == 1, i < j) for i in range(5) for j in range(5)]))

# Now evaluate each option for the fifth lecture (position 4)

# Option A: It is on oystercatchers (0) and is in Gladwyn Hall (0)
opt_a = And(bird[4] == 0, loc[4] == 0)

# Option B: It is on petrels (1) and is in Howard Auditorium (1)
opt_b = And(bird[4] == 1, loc[4] == 1)

# Option C: It is on rails (2) and is in Howard Auditorium (1)
opt_c = And(bird[4] == 2, loc[4] == 1)

# Option D: It is on sandpipers (3) and is in Howard Auditorium (1)
opt_d = And(bird[4] == 3, loc[4] == 1)

# Option E: It is on terns (4) and is in Gladwyn Hall (0)
opt_e = And(bird[4] == 4, loc[4] == 0)

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