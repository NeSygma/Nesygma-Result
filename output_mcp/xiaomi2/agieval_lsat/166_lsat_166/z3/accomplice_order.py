from z3 import *

solver = Solver()

# Positions 1-7 for each accomplice
P = Int('P')  # Peters
Q = Int('Q')  # Quinn
R = Int('R')  # Rovero
S = Int('S')  # Stanton
T = Int('T')  # Tao
V = Int('V')  # Villas
W = Int('W')  # White

people = [P, Q, R, S, T, V, W]

# All positions are between 1 and 7
for p in people:
    solver.add(p >= 1, p <= 7)

# All different positions
solver.add(Distinct(people))

# Base constraints from the problem
# 1. Stanton neither immediately before nor immediately after Tao
solver.add(Abs(S - T) != 1)

# 2. Quinn recruited earlier than Rovero
solver.add(Q < R)

# 3. Villas recruited immediately before White
solver.add(V + 1 == W)

# 4. Peters recruited fourth
solver.add(P == 4)

# Additional constraints from the conditional in the question
# 5. White recruited earlier than Rovero
solver.add(W < R)

# 6. Rovero recruited earlier than Tao
solver.add(R < T)

# Now check each option to see which "could be true"
found_options = []

# (A) Quinn was recruited first
opt_a = (Q == 1)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# (B) Rovero was recruited third
opt_b = (R == 3)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# (C) Stanton was recruited second
opt_c = (S == 2)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# (D) Tao was recruited sixth
opt_d = (T == 6)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# (E) Villas was recruited sixth
opt_e = (V == 6)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append('E')
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

# Print a sample model for verification
solver.push()
if solver.check() == sat:
    m = solver.model()
    print("\nSample model:")
    for name, var in [("Peters", P), ("Quinn", Q), ("Rovero", R), ("Stanton", S), ("Tao", T), ("Villas", V), ("White", W)]:
        print(f"  {name}: position {m[var]}")
solver.pop()