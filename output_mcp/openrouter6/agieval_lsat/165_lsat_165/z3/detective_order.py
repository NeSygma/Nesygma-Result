from z3 import *

solver = Solver()

# Declare variables for positions (1 to 7)
peters = Int('peters')
quinn = Int('quinn')
rovero = Int('rovero')
stanton = Int('stanton')
tao = Int('tao')
villas = Int('villas')
white = Int('white')

# Base constraints
# All positions distinct and within 1..7
solver.add(Distinct([peters, quinn, rovero, stanton, tao, villas, white]))
solver.add(peters >= 1, peters <= 7)
solver.add(quinn >= 1, quinn <= 7)
solver.add(rovero >= 1, rovero <= 7)
solver.add(stanton >= 1, stanton <= 7)
solver.add(tao >= 1, tao <= 7)
solver.add(villas >= 1, villas <= 7)
solver.add(white >= 1, white <= 7)

# Stanton was recruited neither immediately before nor immediately after Tao
solver.add(Not(Or(stanton == tao + 1, stanton == tao - 1)))

# Quinn was recruited earlier than Rovero
solver.add(quinn < rovero)

# Villas was recruited immediately before White
solver.add(white == villas + 1)

# Peters was recruited fourth
solver.add(peters == 4)

# Extra condition: Quinn was recruited immediately before Rovero
solver.add(quinn + 1 == rovero)

# Now evaluate each option: Stanton's position
# We want to find which position is impossible (unsat)
found_options = []
options = [
    ("A", stanton == 1),
    ("B", stanton == 2),
    ("C", stanton == 3),
    ("D", stanton == 5),
    ("E", stanton == 7)
]

for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
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