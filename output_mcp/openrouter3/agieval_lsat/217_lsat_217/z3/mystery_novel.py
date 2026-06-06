from z3 import *

solver = Solver()

# Declare variables: chapter number for each clue (1-7)
R = Int('R')
S = Int('S')
T = Int('T')
U = Int('U')
W = Int('W')
X = Int('X')
Z = Int('Z')

clues = [R, S, T, U, W, X, Z]

# Each clue must be in a chapter 1-7
for clue in clues:
    solver.add(clue >= 1, clue <= 7)

# All clues must be in different chapters (permutation)
solver.add(Distinct(clues))

# Constraint 1: T cannot be in chapter 1
solver.add(T != 1)

# Constraint 2: T must be before W, and exactly two chapters separating them
# So W = T + 3 (since T before W, and exactly 2 chapters between means W is 3 chapters after T)
solver.add(W == T + 3)
solver.add(T < W)  # redundant but explicit

# Constraint 3: S and Z cannot be adjacent
solver.add(Or(Abs(S - Z) != 1))

# Constraint 4: W and X cannot be adjacent
solver.add(Or(Abs(W - X) != 1))

# Constraint 5: U and X must be adjacent
solver.add(Abs(U - X) == 1)

# Now test each answer choice using the exact skeleton
found_options = []

# Option A: R is mentioned in chapter 7
opt_a_constr = (R == 7)

# Option B: T is mentioned in chapter 5
opt_b_constr = (T == 5)

# Option C: U is mentioned in chapter 7
opt_c_constr = (U == 7)

# Option D: W is mentioned in chapter 3
opt_d_constr = (W == 3)

# Option E: X is mentioned in chapter 6
opt_e_constr = (X == 6)

for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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