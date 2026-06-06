from z3 import *

solver = Solver()

# Declare position variables for each accomplice
p_peters = Int('p_peters')
p_quinn = Int('p_quinn')
p_rovero = Int('p_rovero')
p_stanton = Int('p_stanton')
p_tao = Int('p_tao')
p_villas = Int('p_villas')
p_white = Int('p_white')

# All positions are between 1 and 7 and distinct
positions = [p_peters, p_quinn, p_rovero, p_stanton, p_tao, p_villas, p_white]
for pos in positions:
    solver.add(pos >= 1, pos <= 7)
solver.add(Distinct(positions))

# Base constraints
solver.add(p_peters == 4)  # Peters was recruited fourth
solver.add(p_tao == 2)     # Tao was recruited second

# Stanton was recruited neither immediately before nor immediately after Tao
solver.add(Not(Or(p_stanton == p_tao - 1, p_stanton == p_tao + 1)))

# Quinn was recruited earlier than Rovero
solver.add(p_quinn < p_rovero)

# Villas was recruited immediately before White
solver.add(p_villas + 1 == p_white)

# Multiple choice options
found_options = []

# Option A: Quinn was recruited third
solver.push()
solver.add(p_quinn == 3)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Rovero was recruited fifth
solver.push()
solver.add(p_rovero == 5)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Stanton was recruited sixth
solver.push()
solver.add(p_stanton == 6)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Villas was recruited sixth
solver.push()
solver.add(p_villas == 6)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: White was recruited third
solver.push()
solver.add(p_white == 3)
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