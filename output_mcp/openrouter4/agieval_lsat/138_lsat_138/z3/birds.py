from z3 import *

solver = Solver()

# Bird constants
O, P, R, S, T = 0, 1, 2, 3, 4

# Variables: bird at each position (0-indexed positions 0..4)
bird = [Int(f"bird_{i}") for i in range(5)]
loc = [Int(f"loc_{i}") for i in range(5)]  # 0=Gladwyn, 1=Howard

# Domain constraints
for i in range(5):
    solver.add(bird[i] >= 0, bird[i] <= 4)
    solver.add(loc[i] >= 0, loc[i] <= 1)

# All birds distinct
solver.add(Distinct(bird))

# 1. First lecture in Gladwyn Hall
solver.add(loc[0] == 0)

# 2. Fourth lecture in Howard Auditorium
solver.add(loc[3] == 1)

# 3. Exactly three lectures in Gladwyn Hall
solver.add(Sum([If(loc[i] == 0, 1, 0) for i in range(5)]) == 3)

# 4. Sandpipers in Howard, and earlier than oystercatchers
# S in H
for i in range(5):
    solver.add(Implies(bird[i] == S, loc[i] == 1))
# S earlier than O: there exist i,j with bird[i]==S, bird[j]==O, i<j
solver.add(Or([And(bird[i] == S, bird[j] == O, i < j) for i in range(5) for j in range(5) if i < j]))

# 5. Terns earlier than petrels, petrels in Gladwyn Hall
# T earlier than P
solver.add(Or([And(bird[i] == T, bird[j] == P, i < j) for i in range(5) for j in range(5) if i < j]))
# P in G
for i in range(5):
    solver.add(Implies(bird[i] == P, loc[i] == 0))

# Given: third lecture is on sandpipers (position index 2)
solver.add(bird[2] == S)

# Now evaluate each option
found_options = []

# Option A: second lecture (index 1) on oystercatchers and in Gladwyn Hall
opt_a = And(bird[1] == O, loc[1] == 0)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: fifth lecture (index 4) on oystercatchers and in Howard Auditorium
opt_b = And(bird[4] == O, loc[4] == 1)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: second lecture (index 1) on rails and in Howard Auditorium
opt_c = And(bird[1] == R, loc[1] == 1)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: second lecture (index 1) on terns and in Gladwyn Hall
opt_d = And(bird[1] == T, loc[1] == 0)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: fourth lecture (index 3) on terns and in Howard Auditorium
opt_e = And(bird[3] == T, loc[3] == 1)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append("E")
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