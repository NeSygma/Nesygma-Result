from z3 import *

solver = Solver()

# Seven accomplices, positions 1-7
P, Q, R, S, T, V, W = Ints('P Q R S T V W')
names = {'P': 'Peters', 'Q': 'Quinn', 'R': 'Rovero', 'S': 'Stanton', 'T': 'Tao', 'V': 'Villas', 'W': 'White'}
positions = [P, Q, R, S, T, V, W]

# All positions are between 1 and 7
for pos in positions:
    solver.add(pos >= 1, pos <= 7)

# All distinct
solver.add(Distinct(positions))

# Base constraints from the problem:
# 1. Stanton was recruited neither immediately before nor immediately after Tao
solver.add(S != T + 1)
solver.add(S != T - 1)

# 2. Quinn was recruited earlier than Rovero
solver.add(Q < R)

# 3. Villas was recruited immediately before White
solver.add(V + 1 == W)

# 4. Peters was recruited fourth
solver.add(P == 4)

# Additional constraints from the question:
# White was recruited earlier than Rovero
solver.add(W < R)

# Rovero was recruited earlier than Tao
solver.add(R < T)

# Now test each option
found_options = []

# (A) Quinn was recruited first
solver.push()
solver.add(Q == 1)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# (B) Rovero was recruited third
solver.push()
solver.add(R == 3)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# (C) Stanton was recruited second
solver.push()
solver.add(S == 2)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# (D) Tao was recruited sixth
solver.push()
solver.add(T == 6)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# (E) Villas was recruited sixth
solver.push()
solver.add(V == 6)
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