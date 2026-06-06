from z3 import *

# Declare Boolean variables for each employee
My = Bool('My')   # Myers
Or = Bool('Or')   # Ortega
Pa = Bool('Pa')   # Paine
Sc = Bool('Sc')   # Schmidt
Th = Bool('Th')   # Thomson
Wo = Bool('Wo')   # Wong
Yo = Bool('Yo')   # Yoder
Za = Bool('Za')   # Zayre

solver = Solver()

# Base constraints
# At least four employees on the team
solver.add(Sum([If(My,1,0), If(Or,1,0), If(Pa,1,0), If(Sc,1,0),
                If(Th,1,0), If(Wo,1,0), If(Yo,1,0), If(Za,1,0)]) >= 4)

# Condition 1: If Myers is on the team, neither Ortega nor Paine can be.
solver.add(Implies(My, And(Not(Or), Not(Pa))))

# Condition 2: If Schmidt is on the team, both Paine and Thomson must also be.
solver.add(Implies(Sc, And(Pa, Th)))

# Condition 3: If Wong is on the team, both Myers and Yoder must also be.
solver.add(Implies(Wo, And(My, Yo)))

# Additional: Yoder is not on the team
solver.add(Yo == False)

# Now test each option
found_options = []
options = [("A", Za), ("B", Th), ("C", Pa), ("D", Or), ("E", My)]

for letter, var in options:
    solver.push()
    solver.add(var)  # the employee must be on the team
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