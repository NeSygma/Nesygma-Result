from z3 import *

# Employees as Boolean variables
Myers, Ortega, Paine, Schmidt, Thomson, Wong, Yoder, Zayre = Bools('Myers Ortega Paine Schmidt Thomson Wong Yoder Zayre')

solver = Solver()

# At least four employees on the team
solver.add(Sum([Myers, Ortega, Paine, Schmidt, Thomson, Wong, Yoder, Zayre]) >= 4)

# If Myers is on the team, then neither Ortega nor Paine can be
solver.add(Implies(Myers, Not(Ortega)))
solver.add(Implies(Myers, Not(Paine)))

# If Schmidt is on the team, both Paine and Thomson must also be
solver.add(Implies(Schmidt, Paine))
solver.add(Implies(Schmidt, Thomson))

# If Wong is on the team, both Myers and Yoder must also be
solver.add(Implies(Wong, Myers))
solver.add(Implies(Wong, Yoder))

# Evaluate each option: which pair CANNOT be together?
# We'll test whether the pair can be together (both on team). If unsat, they cannot be together.
found_options = []
options = [
    ("A", Myers, Thomson),
    ("B", Ortega, Yoder),
    ("C", Paine, Zayre),
    ("D", Schmidt, Wong),
    ("E", Wong, Yoder)
]

for letter, emp1, emp2 in options:
    solver.push()
    # Try to see if both can be on the team
    solver.add(And(emp1, emp2))
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