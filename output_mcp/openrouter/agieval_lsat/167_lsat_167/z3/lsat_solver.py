from z3 import *

solver = Solver()
# Declare variables for each person
Peters = Int('Peters')
Quinn = Int('Quinn')
Rovero = Int('Rovero')
Stanton = Int('Stanton')
Tao = Int('Tao')
Villas = Int('Villas')
White = Int('White')
people = [Peters, Quinn, Rovero, Stanton, Tao, Villas, White]
# Domain constraints: positions 1..7
for p in people:
    solver.add(p >= 1, p <= 7)
# All distinct positions
solver.add(Distinct(people))
# Given constraints
solver.add(Peters == 4)  # Peters was recruited fourth
solver.add(Villas + 1 == White)  # Villas immediately before White
solver.add(Quinn < Rovero)  # Quinn earlier than Rovero
solver.add(Abs(Stanton - Tao) != 1)  # Stanton not immediately before/after Tao
# Additional condition from the question
solver.add(White + 1 == Quinn)  # White immediately before Quinn

# Define option constraints: each option asserts that the named person is in position 6
option_constraints = {
    "A": Quinn == 6,
    "B": Rovero == 6,
    "C": Stanton == 6,
    "D": Villas == 6,
    "E": White == 6,
}

found_options = []
for letter, constr in [("A", option_constraints["A"]),
                       ("B", option_constraints["B"]),
                       ("C", option_constraints["C"]),
                       ("D", option_constraints["D"]),
                       ("E", option_constraints["E"])]:
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