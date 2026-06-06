from z3 import *

solver = Solver()

# 5 lectures, positions 0..4 (first=0, fourth=3)
# Birds: 0=oystercatchers, 1=petrels, 2=rails, 3=sandpipers, 4=terns
# Locations: 0=Gladwyn Hall, 1=Howard Auditorium

# Decision variables: bird at each position, location at each position
bird = [Int(f'bird_{i}') for i in range(5)]
loc = [Int(f'loc_{i}') for i in range(5)]

# Domains
for i in range(5):
    solver.add(bird[i] >= 0, bird[i] <= 4)
    solver.add(loc[i] >= 0, loc[i] <= 1)

# All birds distinct
solver.add(Distinct(bird))

# Exactly three lectures in Gladwyn Hall (loc=0)
solver.add(Sum([If(loc[i] == 0, 1, 0) for i in range(5)]) == 3)

# First lecture (position 0) is in Gladwyn Hall
solver.add(loc[0] == 0)

# Fourth lecture (position 3) is in Howard Auditorium
solver.add(loc[3] == 1)

# Sandpipers (bird=3) is in Howard Auditorium and earlier than oystercatchers (bird=0)
# sandpipers location = 1
solver.add(Or([And(bird[i] == 3, loc[i] == 1) for i in range(5)]))
# sandpipers earlier than oystercatchers
solver.add(Or([And(bird[i] == 3, bird[j] == 0, i < j) for i in range(5) for j in range(5)]))

# Terns (bird=4) earlier than petrels (bird=1), and petrels in Gladwyn Hall (loc=0)
solver.add(Or([And(bird[i] == 4, bird[j] == 1, i < j) for i in range(5) for j in range(5)]))
solver.add(Or([And(bird[i] == 1, loc[i] == 0) for i in range(5)]))

# Additional condition from the question: terns (bird=4) is in Howard Auditorium (loc=1)
solver.add(Or([And(bird[i] == 4, loc[i] == 1) for i in range(5)]))

# Now evaluate each option about the third lecture (position 2)
# Option A: third lecture is on oystercatchers (bird=0) and in Gladwyn Hall (loc=0)
opt_a = And(bird[2] == 0, loc[2] == 0)

# Option B: third lecture is on rails (bird=2) and in Howard Auditorium (loc=1)
opt_b = And(bird[2] == 2, loc[2] == 1)

# Option C: third lecture is on rails (bird=2) and in Gladwyn Hall (loc=0)
opt_c = And(bird[2] == 2, loc[2] == 0)

# Option D: third lecture is on sandpipers (bird=3) and in Howard Auditorium (loc=1)
opt_d = And(bird[2] == 3, loc[2] == 1)

# Option E: third lecture is on terns (bird=4) and in Howard Auditorium (loc=1)
opt_e = And(bird[2] == 4, loc[2] == 1)

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