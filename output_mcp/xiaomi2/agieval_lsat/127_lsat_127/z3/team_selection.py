from z3 import *

solver = Solver()

# Boolean variables: True if employee is on the team
Myers = Bool('Myers')
Ortega = Bool('Ortega')
Paine = Bool('Paine')
Schmidt = Bool('Schmidt')
Thomson = Bool('Thomson')
Wong = Bool('Wong')
Yoder = Bool('Yoder')
Zayre = Bool('Zayre')

employees = [Myers, Ortega, Paine, Schmidt, Thomson, Wong, Yoder, Zayre]

# Constraint 1: If Myers is on the team, neither Ortega nor Paine can be
solver.add(Implies(Myers, And(Not(Ortega), Not(Paine))))

# Constraint 2: If Schmidt is on the team, both Paine and Thomson must be
solver.add(Implies(Schmidt, And(Paine, Thomson)))

# Constraint 3: If Wong is on the team, both Myers and Yoder must be
solver.add(Implies(Wong, And(Myers, Yoder)))

# Constraint 4: At least 4 employees on the team
solver.add(Sum([If(e, 1, 0) for e in employees]) >= 4)

# For each option, check if it's possible that NEITHER employee is on the team.
# If impossible (unsat), then at least one MUST be on the team.
options = {
    "A": And(Not(Ortega), Not(Schmidt)),
    "B": And(Not(Ortega), Not(Wong)),
    "C": And(Not(Paine), Not(Schmidt)),
    "D": And(Not(Thomson), Not(Yoder)),
    "E": And(Not(Yoder), Not(Zayre)),
}

found_options = []
for letter, neither_constraint in options.items():
    solver.push()
    solver.add(neither_constraint)
    result = solver.check()
    if result == unsat:
        # Cannot exclude both → at least one MUST be on the team
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