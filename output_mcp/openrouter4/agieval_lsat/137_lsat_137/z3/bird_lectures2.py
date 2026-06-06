from z3 import *

solver = Solver()

# Birds: Oystercatchers, Petrels, Rails, Sandpipers, Terns
O, P, R, S, T = 0, 1, 2, 3, 4
bird_names = ["O", "P", "R", "S", "T"]

# Each bird has a position 1-5
pos = [Int(f"pos_{bird_names[i]}") for i in range(5)]

# Use a Z3 Array for locations at positions 1..5 (index 1..5, we'll use 1-indexed)
loc = Array('loc', IntSort(), BoolSort())

# Domain constraints
for i in range(5):
    solver.add(pos[i] >= 1, pos[i] <= 5)

solver.add(Distinct(pos))

# Constraint 1: First lecture is in Gladwyn Hall
solver.add(Select(loc, 1) == True)

# Constraint 2: Fourth lecture is in Howard Auditorium
solver.add(Select(loc, 4) == False)

# Constraint 3: Exactly three lectures are in Gladwyn Hall
solver.add(Sum([If(Select(loc, i+1), 1, 0) for i in range(5)]) == 3)

# Constraint 4: Sandpipers is in Howard and earlier than oystercatchers
solver.add(Select(loc, pos[S]) == False)  # S is in H
solver.add(pos[S] < pos[O])

# Constraint 5: Terns earlier than petrels, petrels in Gladwyn
solver.add(pos[T] < pos[P])
solver.add(Select(loc, pos[P]) == True)  # P is in G

# Now evaluate each option for the fifth lecture
options = []

# (A) It is on oystercatchers and is in Gladwyn Hall.
opt_a = And(pos[O] == 5, Select(loc, 5) == True)
options.append(("A", opt_a))

# (B) It is on petrels and is in Howard Auditorium.
opt_b = And(pos[P] == 5, Select(loc, 5) == False)
options.append(("B", opt_b))

# (C) It is on rails and is in Howard Auditorium.
opt_c = And(pos[R] == 5, Select(loc, 5) == False)
options.append(("C", opt_c))

# (D) It is on sandpipers and is in Howard Auditorium.
opt_d = And(pos[S] == 5, Select(loc, 5) == False)
options.append(("D", opt_d))

# (E) It is on terns and is in Gladwyn Hall.
opt_e = And(pos[T] == 5, Select(loc, 5) == True)
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