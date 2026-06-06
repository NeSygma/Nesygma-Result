from z3 import *

# Students: Juana, Kelly, Lateefah, Mei, Olga
# Teams: 0 = green, 1 = red

solver = Solver()

# Variables: team assignment (0=green, 1=red)
juana = Int('juana')
kelly = Int('kelly')
lateefah = Int('lateefah')
mei = Int('mei')
olga = Int('olga')

# Facilitator variables
juana_fac = Bool('juana_fac')
kelly_fac = Bool('kelly_fac')
lateefah_fac = Bool('lateefah_fac')
mei_fac = Bool('mei_fac')
olga_fac = Bool('olga_fac')

students = [juana, kelly, lateefah, mei, olga]
facilitators = [juana_fac, kelly_fac, lateefah_fac, mei_fac, olga_fac]

# Domain: each student assigned to team 0 (green) or 1 (red)
for s in students:
    solver.add(Or(s == 0, s == 1))

# One team has 2 members, the other has 3 members
green_count = Sum([If(s == 0, 1, 0) for s in students])
solver.add(Or(green_count == 2, green_count == 3))

# Exactly one facilitator per team
green_fac_count = Sum([If(And(s == 0, fac), 1, 0) for s, fac in zip(students, facilitators)])
solver.add(green_fac_count == 1)

red_fac_count = Sum([If(And(s == 1, fac), 1, 0) for s, fac in zip(students, facilitators)])
solver.add(red_fac_count == 1)

# Condition: Juana is assigned to a different team than Olga
solver.add(juana != olga)

# Condition: Lateefah is assigned to the green team
solver.add(lateefah == 0)

# Condition: Kelly is not a facilitator
solver.add(kelly_fac == False)

# Condition: Olga is a facilitator
solver.add(olga_fac == True)

# Additional condition from the question: Mei is assigned to the green team
solver.add(mei == 0)

# For "must be true", we check if the negation is impossible.
# If Not(option) is unsat, then the option must be true.

found_options = []
for letter, constr in [("A", juana == 0), ("B", kelly == 1), ("C", olga == 0), ("D", lateefah_fac == True), ("E", mei_fac == True)]:
    solver.push()
    solver.add(Not(constr))
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