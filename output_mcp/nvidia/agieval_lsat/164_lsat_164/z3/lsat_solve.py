from z3 import *

solver = Solver()

# Declare position variables for each person
peters = Int('peters')
quinn = Int('quinn')
rovero = Int('rovero')
stanton = Int('stanton')
tao = Int('tao')
villas = Int('villas')
white = Int('white')

# Base constraints
solver.add(Distinct([peters, quinn, rovero, stanton, tao, villas, white]))
solver.add(peters == 4)
solver.add(tao == 2)
# Stanton not adjacent to Tao
solver.add(Not(Or(stanton == tao - 1, stanton == tao + 1)))
# Quinn earlier than Rovero
solver.add(quinn < rovero)
# Villas immediately before White
solver.add(villas + 1 == white)

found_options = []

# Option A: Quinn was recruited third
solver.push()
solver.add(quinn == 3)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Rovero was recruited fifth
solver.push()
solver.add(rovero == 5)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Stanton was recruited sixth
solver.push()
solver.add(stanton == 6)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Villas was recruited sixth
solver.push()
solver.add(villas == 6)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: White was recruited third
solver.push()
solver.add(white == 3)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Evaluate results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")