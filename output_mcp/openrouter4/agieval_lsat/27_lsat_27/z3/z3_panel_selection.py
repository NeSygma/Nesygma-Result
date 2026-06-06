from z3 import *

# Scientists
# Botanists: F, G, H -> indices 0,1,2
# Chemists: K, L, M -> indices 3,4,5
# Zoologists: P, Q, R -> indices 6,7,8

scientists = ["F", "G", "H", "K", "L", "M", "P", "Q", "R"]
N = 9

# Boolean variables for each scientist being selected
selected = [Bool(f"selected_{s}") for s in scientists]

solver = Solver()

# Exactly 5 scientists are selected
solver.add(Sum([If(s, 1, 0) for s in selected]) == 5)

# F, L, Q, and R are selected (given)
solver.add(selected[0] == True)  # F
solver.add(selected[4] == True)  # L
solver.add(selected[7] == True)  # Q
solver.add(selected[8] == True)  # R

# Condition 1: At least one of each type
# Botanists: F, G, H (indices 0,1,2)
solver.add(Or([selected[i] for i in [0,1,2]]))
# Chemists: K, L, M (indices 3,4,5)
solver.add(Or([selected[i] for i in [3,4,5]]))
# Zoologists: P, Q, R (indices 6,7,8)
solver.add(Or([selected[i] for i in [6,7,8]]))

# Condition 2: If more than one botanist, then at most one zoologist
# Count botanists selected
botanists_selected = Sum([If(selected[i], 1, 0) for i in [0,1,2]])
# Count zoologists selected
zoologists_selected = Sum([If(selected[i], 1, 0) for i in [6,7,8]])
solver.add(Implies(botanists_selected > 1, zoologists_selected <= 1))

# Condition 3: F and K cannot both be selected
solver.add(Not(And(selected[0], selected[3])))  # F and K

# Condition 4: K and M cannot both be selected
solver.add(Not(And(selected[3], selected[5])))  # K and M

# Condition 5: If M is selected, both P and R must be selected
solver.add(Implies(selected[5], And(selected[6], selected[8])))  # M -> P and R

# Now test each option
# Option A: G (index 1)
# Option B: H (index 2)
# Option C: K (index 3)
# Option D: M (index 5)
# Option E: P (index 6)

options = [
    ("A", selected[1]),  # G
    ("B", selected[2]),  # H
    ("C", selected[3]),  # K
    ("D", selected[5]),  # M
    ("E", selected[6])   # P
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
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