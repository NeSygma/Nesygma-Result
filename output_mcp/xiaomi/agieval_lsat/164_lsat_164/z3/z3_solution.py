from z3 import *

solver = Solver()

# Seven accomplices: Peters, Quinn, Rovero, Stanton, Tao, Villas, White
# Positions 1-7 (one at a time)
P, Q, R, S, T, V, W = Ints('P Q R S T V W')
positions = [P, Q, R, S, T, V, W]
names = ['Peters', 'Quinn', 'Rovero', 'Stanton', 'Tao', 'Villas', 'White']

# Each position is 1-7, all distinct
for pos in positions:
    solver.add(pos >= 1, pos <= 7)
solver.add(Distinct(positions))

# Constraint 1: Stanton was recruited neither immediately before nor immediately after Tao
solver.add(S != T + 1)
solver.add(S != T - 1)

# Constraint 2: Quinn was recruited earlier than Rovero
solver.add(Q < R)

# Constraint 3: Villas was recruited immediately before White
solver.add(W == V + 1)

# Constraint 4: Peters was recruited fourth
solver.add(P == 4)

# Constraint 5: Tao was recruited second
solver.add(T == 2)

# Now test each option
found_options = []

# (A) Quinn was recruited third
solver.push()
solver.add(Q == 3)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# (B) Rovero was recruited fifth
solver.push()
solver.add(R == 5)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# (C) Stanton was recruited sixth
solver.push()
solver.add(S == 6)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# (D) Villas was recruited sixth
solver.push()
solver.add(V == 6)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# (E) White was recruited third
solver.push()
solver.add(W == 3)
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