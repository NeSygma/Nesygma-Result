from z3 import *

solver = Solver()

# Birds: Oystercatchers, Petrels, Rails, Sandpipers, Terns
O, P, R, S, T = 0, 1, 2, 3, 4
bird_names = ["O", "P", "R", "S", "T"]

# Each bird has a position 1-5
pos = [Int(f"pos_{bird_names[i]}") for i in range(5)]

# Each position (1-indexed) has a location: True = Gladwyn, False = Howard
loc = [Bool(f"loc_{i+1}") for i in range(5)]

# Domain constraints
for i in range(5):
    solver.add(pos[i] >= 1, pos[i] <= 5)

solver.add(Distinct(pos))

# Constraint 1: First lecture is in Gladwyn Hall
solver.add(loc[0] == True)

# Constraint 2: Fourth lecture is in Howard Auditorium
solver.add(loc[3] == False)

# Constraint 3: Exactly three lectures are in Gladwyn Hall
solver.add(Sum([If(loc[i], 1, 0) for i in range(5)]) == 3)

# Constraint 4: Sandpipers is in Howard and earlier than oystercatchers
solver.add(loc[pos[S] - 1] == False)  # S is in H
solver.add(pos[S] < pos[O])

# Constraint 5: Terns earlier than petrels, petrels in Gladwyn
solver.add(pos[T] < pos[P])
solver.add(loc[pos[P] - 1] == True)  # P is in G

# Now evaluate each option for the fifth lecture
options = []

# (A) It is on oystercatchers and is in Gladwyn Hall.
opt_a = And(pos[O] == 5, loc[4] == True)
options.append(("A", opt_a))

# (B) It is on petrels and is in Howard Auditorium.
opt_b = And(pos[P] == 5, loc[4] == False)
options.append(("B", opt_b))

# (C) It is on rails and is in Howard Auditorium.
opt_c = And(pos[R] == 5, loc[4] == False)
options.append(("C", opt_c))

# (D) It is on sandpipers and is in Howard Auditorium.
opt_d = And(pos[S] == 5, loc[4] == False)
options.append(("D", opt_d))

# (E) It is on terns and is in Gladwyn Hall.
opt_e = And(pos[T] == 5, loc[4] == True)
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