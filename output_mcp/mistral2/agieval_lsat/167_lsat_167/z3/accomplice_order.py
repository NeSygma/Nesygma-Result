from z3 import *

# Declare symbolic variables for each accomplice's recruitment position
peters = Int('peters')
quinn = Int('quinn')
rovero = Int('rovero')
stanton = Int('stanton')
tao = Int('tao')
villas = Int('villas')
white = Int('white')

# Create a solver instance
solver = Solver()

# All positions are between 1 and 7 and distinct
positions = [peters, quinn, rovero, stanton, tao, villas, white]
for pos in positions:
    solver.add(pos >= 1, pos <= 7)
solver.add(Distinct(positions))

# Peters was recruited fourth
solver.add(peters == 4)

# Villas was recruited immediately before White
solver.add(villas == white - 1)

# White was recruited immediately before Quinn
solver.add(white == quinn - 1)

# Quinn was recruited earlier than Rovero
solver.add(quinn < rovero)

# Stanton was recruited neither immediately before nor immediately after Tao
solver.add(Not(stanton == tao - 1))
solver.add(Not(stanton == tao + 1))

# Now, test each option to see if it must be the sixth position
found_options = []

# Option A: Quinn is sixth
solver.push()
solver.add(quinn == 6)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Rovero is sixth
solver.push()
solver.add(rovero == 6)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Stanton is sixth
solver.push()
solver.add(stanton == 6)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Villas is sixth
solver.push()
solver.add(villas == 6)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: White is sixth
solver.push()
solver.add(white == 6)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")