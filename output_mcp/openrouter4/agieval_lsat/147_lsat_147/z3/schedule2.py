from z3 import *

solver = Solver()

# Positions: 0 = earliest, 3 = latest
# Historians: 0=Farley, 1=Garcia, 2=Holden, 3=Jiang
pos_h = [Int(f"pos_h_{i}") for i in range(4)]
# Topics: 0=Lithographs, 1=Oil paintings, 2=Sculptures, 3=Watercolors
pos_t = [Int(f"pos_t_{i}") for i in range(4)]

# All positions are 0-3
for i in range(4):
    solver.add(pos_h[i] >= 0, pos_h[i] <= 3)
    solver.add(pos_t[i] >= 0, pos_t[i] <= 3)

# Positions are distinct among historians and among topics
solver.add(Distinct(pos_h))
solver.add(Distinct(pos_t))

# Constraint 1: Oil paintings (1) and Watercolors (3) must both be earlier than Lithographs (0)
solver.add(pos_t[1] < pos_t[0])  # O < L
solver.add(pos_t[3] < pos_t[0])  # W < L

# Constraint 2: Farley's lecture (pos_h[0]) must be earlier than the Oil paintings lecture (pos_t[1])
solver.add(pos_h[0] < pos_t[1])  # F < O

# Constraint 3: Holden's lecture (pos_h[2]) must be earlier than both Garcia's (pos_h[1]) and Jiang's (pos_h[3])
solver.add(pos_h[2] < pos_h[1])  # H < G
solver.add(pos_h[2] < pos_h[3])  # H < J

# Evaluate each option
# Option A: Farley gives Lithographs -> pos_h[0] == pos_t[0]
# Option B: Garcia gives Sculptures -> pos_h[1] == pos_t[2]
# Option C: Garcia gives Watercolors -> pos_h[1] == pos_t[3]
# Option D: Holden gives Oil paintings -> pos_h[2] == pos_t[1]
# Option E: Jiang gives Watercolors -> pos_h[3] == pos_t[3]

options = [
    ("A", pos_h[0] == pos_t[0]),
    ("B", pos_h[1] == pos_t[2]),
    ("C", pos_h[1] == pos_t[3]),
    ("D", pos_h[2] == pos_t[1]),
    ("E", pos_h[3] == pos_t[3])
]

# For "Which CANNOT be true?" we find the option that is UNSAT
unsat_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        unsat_options.append(letter)
    solver.pop()

if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options cannot be true {unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: All options can be true")