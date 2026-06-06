from z3 import *

# We have 7 accomplices: Peters, Quinn, Rovero, Stanton, Tao, Villas, White
# Positions 1 through 7 (1st through 7th recruited)
# We'll use integer variables for each person's position

P, Q, R, S, T, V, W = Ints('P Q R S T V W')

solver = Solver()

# Each position is between 1 and 7
persons = [P, Q, R, S, T, V, W]
for p in persons:
    solver.add(p >= 1, p <= 7)

# All positions are distinct
solver.add(Distinct(persons))

# Stanton was recruited neither immediately before nor immediately after Tao.
# |S - T| != 1
solver.add(Not(Or(S - T == 1, T - S == 1)))

# Quinn was recruited earlier than Rovero.
solver.add(Q < R)

# Villas was recruited immediately before White.
solver.add(V + 1 == W)

# Peters was recruited fourth.
solver.add(P == 4)

# Additional condition: White was recruited immediately before Quinn.
solver.add(W + 1 == Q)

# Now evaluate each option: which one must have been recruited sixth?
# We need to check if a given person being 6th is forced by the constraints.
# We'll test each option by adding the constraint that the person is NOT 6th.
# If adding "person != 6" makes the problem unsat, then that person MUST be 6th.

found_options = []

# Option A: Quinn is 6th
solver.push()
solver.add(Q != 6)
if solver.check() == unsat:
    found_options.append("A")
solver.pop()

# Option B: Rovero is 6th
solver.push()
solver.add(R != 6)
if solver.check() == unsat:
    found_options.append("B")
solver.pop()

# Option C: Stanton is 6th
solver.push()
solver.add(S != 6)
if solver.check() == unsat:
    found_options.append("C")
solver.pop()

# Option D: Villas is 6th
solver.push()
solver.add(V != 6)
if solver.check() == unsat:
    found_options.append("D")
solver.pop()

# Option E: White is 6th
solver.push()
solver.add(W != 6)
if solver.check() == unsat:
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