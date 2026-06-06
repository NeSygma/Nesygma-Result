from z3 import *

# Create solver
solver = Solver()

# Define chapter positions for each clue
chapters = [Int(f'ch_{clue}') for clue in ['R', 'S', 'T', 'U', 'W', 'X', 'Z']]
R, S, T, U, W, X, Z = chapters

# Each clue must be in a distinct chapter from 1 to 7
for i, clue in enumerate(chapters):
    solver.add(clue >= 1, clue <= 7)
solver.add(Distinct(chapters))

# Constraint 1: T cannot be mentioned in chapter 1
solver.add(T != 1)

# Constraint 2: T must be mentioned before W, and exactly 2 chapters between them
# So W = T + 3
solver.add(W == T + 3)
solver.add(T >= 1, W <= 7)  # Ensure within bounds

# Constraint 3: S and Z not adjacent
# Adjacent means |S - Z| = 1
solver.add(Or(S == Z - 1, S == Z + 1))

# Constraint 4: W and X not adjacent
solver.add(Or(W == X - 1, W == X + 1))

# Constraint 5: U and X adjacent
solver.add(Or(U == X - 1, U == X + 1))

# Given: Z is in chapter 7
solver.add(Z == 7)

# Now evaluate each answer choice
found_options = []

# Option A: R is mentioned in chapter 3
opt_a = (R == 3)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: S is mentioned in chapter 3
opt_b = (S == 3)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: T is mentioned in chapter 4
opt_c = (T == 4)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: U is mentioned in chapter 1
opt_d = (U == 1)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: X is mentioned in chapter 5
opt_e = (X == 5)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")