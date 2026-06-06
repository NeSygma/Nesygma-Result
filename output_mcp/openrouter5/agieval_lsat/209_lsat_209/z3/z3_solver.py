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

# Domain: team is 0 or 1
for v in [juana, kelly, lateefah, mei, olga]:
    solver.add(Or(v == 0, v == 1))

# Exactly one team has 2 members, the other has 3 members
# Count members on green team (team 0)
green_count = Sum([If(juana == 0, 1, 0),
                   If(kelly == 0, 1, 0),
                   If(lateefah == 0, 1, 0),
                   If(mei == 0, 1, 0),
                   If(olga == 0, 1, 0)])
solver.add(Or(green_count == 2, green_count == 3))

# One member of each team is designated as facilitator
# For each team, exactly one facilitator
# Green team (team 0): exactly one facilitator
green_fac_count = Sum([If(And(juana == 0, juana_fac), 1, 0),
                       If(And(kelly == 0, kelly_fac), 1, 0),
                       If(And(lateefah == 0, lateefah_fac), 1, 0),
                       If(And(mei == 0, mei_fac), 1, 0),
                       If(And(olga == 0, olga_fac), 1, 0)])
solver.add(green_fac_count == 1)

# Red team (team 1): exactly one facilitator
red_fac_count = Sum([If(And(juana == 1, juana_fac), 1, 0),
                     If(And(kelly == 1, kelly_fac), 1, 0),
                     If(And(lateefah == 1, lateefah_fac), 1, 0),
                     If(And(mei == 1, mei_fac), 1, 0),
                     If(And(olga == 1, olga_fac), 1, 0)])
solver.add(red_fac_count == 1)

# Condition: Juana is assigned to a different team than Olga
solver.add(juana != olga)

# Condition: Lateefah is assigned to the green team
solver.add(lateefah == 0)

# Condition: Kelly is not a facilitator
solver.add(Not(kelly_fac))

# Condition: Olga is a facilitator
solver.add(olga_fac)

# Let's first check if the base constraints are satisfiable
print("Base check:", solver.check())
if solver.check() == sat:
    m = solver.model()
    print("Juana team:", m[juana])
    print("Kelly team:", m[kelly])
    print("Lateefah team:", m[lateefah])
    print("Mei team:", m[mei])
    print("Olga team:", m[olga])
    print("Juana fac:", m[juana_fac])
    print("Kelly fac:", m[kelly_fac])
    print("Lateefah fac:", m[lateefah_fac])
    print("Mei fac:", m[mei_fac])
    print("Olga fac:", m[olga_fac])
    print("Green count:", m.eval(green_count))
else:
    print("Base constraints are UNSAT")
    exit()

# The question asks "which one of the following MUST be true?"
# This is a validity/entailment question: which option is entailed by the premises?
# For each option, we check if NOT(option) is consistent with premises.
# If NOT(option) is UNSAT, then option MUST be true.

found_options = []
for letter, constr in [("A", juana == 1), 
                       ("B", lateefah_fac), 
                       ("C", olga == 0), 
                       ("D", Not(And(juana_fac, mei_fac))), 
                       ("E", And(Not(juana_fac), Not(kelly_fac)))]:
    solver.push()
    # To check if constr MUST be true, add NOT(constr) and see if unsat
    solver.add(Not(constr))
    result = solver.check()
    print(f"Option {letter} (NOT): {result}")
    if result == unsat:
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