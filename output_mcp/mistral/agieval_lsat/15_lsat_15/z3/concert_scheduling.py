from z3 import *

# Define composition constants
F, H, L, O, P, R, S, T = 0, 1, 2, 3, 4, 5, 6, 7

# Create a solver
solver = Solver()

# Declare the sequence: positions 0 to 7
positions = [Int(f'pos_{i}') for i in range(8)]

# Helper: All compositions are distinct and in the set {F, H, L, O, P, R, S, T}
compositions_set = [F, H, L, O, P, R, S, T]
solver.add(Distinct(positions))
for p in positions:
    solver.add(Or([p == c for c in compositions_set]))

# Constraint 1: T is performed either immediately before F or immediately after R
# This means there exists an index i such that (positions[i] == T and positions[i+1] == F) or (positions[i] == R and positions[i+1] == T)
solver.add(Or(
    Or([And(positions[i] == T, positions[i+1] == F) for i in range(7)]),
    Or([And(positions[i] == R, positions[i+1] == T) for i in range(7)])
))

# Constraint 2: At least two compositions are performed either after F and before R, or after R and before F
# This means the distance between F and R is at least 3 (positions differ by at least 3)
# Find positions of F and R using Or-loop pattern
f_pos = Int('f_pos')
r_pos = Int('r_pos')
solver.add(And(f_pos >= 0, f_pos < 8))
solver.add(And(r_pos >= 0, r_pos < 8))
# Ensure F and R are in the sequence
solver.add(Or([p == F for p in positions]))
solver.add(Or([p == R for p in positions]))
# Constraint: distance between F and R is at least 3
solver.add(Or(
    And(Or([And(positions[i] == F, f_pos == i) for i in range(8)]),
        Or([And(positions[j] == R, r_pos == j) for j in range(8)]),
        f_pos - r_pos >= 3),
    And(Or([And(positions[i] == R, r_pos == i) for i in range(8)]),
        Or([And(positions[j] == F, f_pos == j) for j in range(8)]),
        r_pos - f_pos >= 3)
))

# Constraint 3: O is performed either first or fifth
solver.add(Or(positions[0] == O, positions[4] == O))

# Constraint 4: The eighth composition performed is either L or H
solver.add(Or(positions[7] == L, positions[7] == H))

# Constraint 5: P is performed at some time before S
# Find positions of P and S
p_pos = Int('p_pos')
s_pos = Int('s_pos')
solver.add(And(p_pos >= 0, p_pos < 8))
solver.add(And(s_pos >= 0, s_pos < 8))
# Ensure P and S are in the sequence
solver.add(Or([p == P for p in positions]))
solver.add(Or([p == S for p in positions]))
# Constraint: P is before S
solver.add(Or([And(positions[i] == P, positions[j] == S, i < j) for i in range(8) for j in range(8)]))

# Constraint 6: At least one composition is performed either after O and before S, or after S and before O
# This means O and S are not adjacent; there is at least one composition between them
# Find position of O
o_pos = Int('o_pos')
solver.add(And(o_pos >= 0, o_pos < 8))
solver.add(Or([And(positions[i] == O, o_pos == i) for i in range(8)]))
# We already have s_pos from constraint 5
solver.add(Or([And(positions[i] == S, s_pos == i) for i in range(8)]))
solver.add(abs(o_pos - s_pos) >= 2)

# Additional condition for the question: O is performed immediately after T
# This means T is immediately before O: there exists i such that positions[i] == T and positions[i+1] == O
solver.add(Or([And(positions[i] == T, positions[i+1] == O) for i in range(7)]))

# Now, evaluate the answer choices for F's position
# Answer choices are about the 1-indexed position of F
# (A) first or second -> 0 or 1 (0-indexed)
# (B) second or third -> 1 or 2
# (C) fourth or sixth -> 3 or 5
# (D) fourth or seventh -> 3 or 6
# (E) sixth or seventh -> 5 or 6

found_options = []

# Option A: F is at position 0 or 1
solver.push()
solver.add(Or(positions[0] == F, positions[1] == F))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: F is at position 1 or 2
solver.push()
solver.add(Or(positions[1] == F, positions[2] == F))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: F is at position 3 or 5
solver.push()
solver.add(Or(positions[3] == F, positions[5] == F))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: F is at position 3 or 6
solver.push()
solver.add(Or(positions[3] == F, positions[6] == F))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: F is at position 5 or 6
solver.push()
solver.add(Or(positions[5] == F, positions[6] == F))
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