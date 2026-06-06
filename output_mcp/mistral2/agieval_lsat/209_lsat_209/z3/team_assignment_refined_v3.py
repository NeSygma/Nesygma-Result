from z3 import *

solver = Solver()

# Declare symbolic variables for team assignments
# 0: green team, 1: red team
Juana_team = Int('Juana_team')
Kelly_team = Int('Kelly_team')
Lateefah_team = Int('Lateefah_team')
Mei_team = Int('Mei_team')
Olga_team = Int('Olga_team')

# Declare symbolic variables for facilitator roles
Juana_facilitator = Bool('Juana_facilitator')
Kelly_facilitator = Bool('Kelly_facilitator')
Lateefah_facilitator = Bool('Lateefah_facilitator')
Mei_facilitator = Bool('Mei_facilitator')
Olga_facilitator = Bool('Olga_facilitator')

# Base constraints
# Each student is assigned to exactly one team (0 or 1)
solver.add(Juana_team >= 0, Juana_team <= 1)
solver.add(Kelly_team >= 0, Kelly_team <= 1)
solver.add(Lateefah_team >= 0, Lateefah_team <= 1)
solver.add(Mei_team >= 0, Mei_team <= 1)
solver.add(Olga_team >= 0, Olga_team <= 1)

# Lateefah is assigned to the green team
solver.add(Lateefah_team == 0)

# Each team has exactly one facilitator
solver.add(Or(Juana_facilitator, Kelly_facilitator, Lateefah_facilitator, Mei_facilitator, Olga_facilitator))
solver.add(Not(And(Juana_facilitator, Kelly_facilitator)))
solver.add(Not(And(Juana_facilitator, Lateefah_facilitator)))
solver.add(Not(And(Juana_facilitator, Mei_facilitator)))
solver.add(Not(And(Juana_facilitator, Olga_facilitator)))
solver.add(Not(And(Kelly_facilitator, Lateefah_facilitator)))
solver.add(Not(And(Kelly_facilitator, Mei_facilitator)))
solver.add(Not(And(Kelly_facilitator, Olga_facilitator)))
solver.add(Not(And(Lateefah_facilitator, Mei_facilitator)))
solver.add(Not(And(Lateefah_facilitator, Olga_facilitator)))
solver.add(Not(And(Mei_facilitator, Olga_facilitator)))

# Facilitator must be on the same team as the student
solver.add(Implies(Juana_facilitator, Juana_team == 0))
solver.add(Implies(Kelly_facilitator, Kelly_team == 0))
solver.add(Implies(Lateefah_facilitator, Lateefah_team == 0))
solver.add(Implies(Mei_facilitator, Mei_team == 0))
solver.add(Implies(Olga_facilitator, Olga_team == 0))

# Additional constraints from the problem
# Juana is assigned to a different team than Olga
solver.add(Juana_team != Olga_team)

# Kelly is not a facilitator
solver.add(Not(Kelly_facilitator))

# Olga is a facilitator
solver.add(Olga_facilitator)

# Team sizes: one team has 2 members, the other has 3
# Lateefah is on the green team, so green team has at least 1 member
# Olga is a facilitator and must be on a team

# If Olga is on the green team (0), then green team has Lateefah, Olga, and one more member (total 3)
# If Olga is on the red team (1), then red team has Olga and two more members (total 3), and green team has Lateefah and one more member (total 2)

# Enforce team sizes based on Olga's team
solver.add(If(Olga_team == 0, 
              # Olga is on green team: green team has 3 members (Lateefah, Olga, and one more)
              Sum([If(Lateefah_team == 0, 1, 0),
                   If(Olga_team == 0, 1, 0),
                   If(Juana_team == 0, 1, 0),
                   If(Kelly_team == 0, 1, 0),
                   If(Mei_team == 0, 1, 0)]) == 3,
              # Olga is on red team: red team has 3 members (Olga and two more), green team has 2 members (Lateefah and one more)
              Sum([If(Lateefah_team == 0, 1, 0),
                   If(Olga_team == 0, 1, 0),
                   If(Juana_team == 0, 1, 0),
                   If(Kelly_team == 0, 1, 0),
                   If(Mei_team == 0, 1, 0)]) == 2))

# Now evaluate the multiple choice options
found_options = []

# Option A: Juana is assigned to the red team
solver.push()
solver.add(Juana_team == 1)
if solver.check() == sat:
    found_options.append("A")
    # Print model for Option A to verify
    model = solver.model()
    print("Model for Option A:")
    print(f"Juana_team = {model[Juana_team]}")
    print(f"Olga_team = {model[Olga_team]}")
    print(f"Juana_facilitator = {model[Juana_facilitator]}")
    print(f"Mei_facilitator = {model[Mei_facilitator]}")
    print(f"Lateefah_facilitator = {model[Lateefah_facilitator]}")
    print()
solver.pop()

# Option B: Lateefah is a facilitator
solver.push()
solver.add(Lateefah_facilitator)
if solver.check() == sat:
    found_options.append("B")
    # Print model for Option B to verify
    model = solver.model()
    print("Model for Option B:")
    print(f"Lateefah_facilitator = {model[Lateefah_facilitator]}")
    print()
solver.pop()

# Option C: Olga is assigned to the green team
solver.push()
solver.add(Olga_team == 0)
if solver.check() == sat:
    found_options.append("C")
    # Print model for Option C to verify
    model = solver.model()
    print("Model for Option C:")
    print(f"Olga_team = {model[Olga_team]}")
    print(f"Olga_facilitator = {model[Olga_facilitator]}")
    print()
solver.pop()

# Option D: Juana and Mei are not both facilitators
solver.push()
solver.add(Not(And(Juana_facilitator, Mei_facilitator)))
if solver.check() == sat:
    found_options.append("D")
    # Print model for Option D to verify
    model = solver.model()
    print("Model for Option D:")
    print(f"Juana_facilitator = {model[Juana_facilitator]}")
    print(f"Mei_facilitator = {model[Mei_facilitator]}")
    print()
solver.pop()

# Option E: Neither Juana nor Kelly is a facilitator
solver.push()
solver.add(Not(Juana_facilitator))
solver.add(Not(Kelly_facilitator))
if solver.check() == sat:
    found_options.append("E")
    # Print model for Option E to verify
    model = solver.model()
    print("Model for Option E:")
    print(f"Juana_facilitator = {model[Juana_facilitator]}")
    print(f"Kelly_facilitator = {model[Kelly_facilitator]}")
    print()
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