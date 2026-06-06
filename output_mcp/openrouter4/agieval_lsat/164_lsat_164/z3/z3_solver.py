from z3 import *

solver = Solver()

# Create position variables for each person (1-indexed positions 1-7)
P, Q, R, S, T, V, W = Ints('P Q R S T V W')

# Domain constraints: positions 1 through 7
persons = [P, Q, R, S, T, V, W]
for p in persons:
    solver.add(p >= 1, p <= 7)

# All positions are distinct
solver.add(Distinct(persons))

# Constraint 1: Stanton was recruited neither immediately before nor immediately after Tao.
solver.add(Abs(S - T) != 1)

# Constraint 2: Quinn was recruited earlier than Rovero.
solver.add(Q < R)

# Constraint 3: Villas was recruited immediately before White.
solver.add(V + 1 == W)

# Constraint 4: Peters was recruited fourth.
solver.add(P == 4)

# Additional given: Tao was recruited second.
solver.add(T == 2)

# Now test each option
# Option A: Quinn was recruited third.
opt_a = (Q == 3)

# Option B: Rovero was recruited fifth.
opt_b = (R == 5)

# Option C: Stanton was recruited sixth.
opt_c = (S == 6)

# Option D: Villas was recruited sixth.
opt_d = (V == 6)

# Option E: White was recruited third.
opt_e = (W == 3)

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