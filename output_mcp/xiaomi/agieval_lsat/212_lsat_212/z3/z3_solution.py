from z3 import *

solver = Solver()

# Variables: team assignment (0 = green, 1 = red) and facilitator status
juana_team = Int('juana_team')
kelly_team = Int('kelly_team')
lateefah_team = Int('lateefah_team')
mei_team = Int('mei_team')
olga_team = Int('olga_team')

juana_fac = Bool('juana_fac')
kelly_fac = Bool('kelly_fac')
lateefah_fac = Bool('lateefah_fac')
mei_fac = Bool('mei_fac')
olga_fac = Bool('olga_fac')

teams = [juana_team, kelly_team, lateefah_team, mei_team, olga_team]
facs = [juana_fac, kelly_fac, lateefah_fac, mei_fac, olga_fac]

# Each student on exactly one team (0=green, 1=red)
for t in teams:
    solver.add(Or(t == 0, t == 1))

# One team has 2 members, the other has 3
green_count = Sum([If(t == 0, 1, 0) for t in teams])
solver.add(Or(green_count == 2, green_count == 3))

# Exactly one facilitator per team
green_fac = Sum([If(And(fac, t == 0), 1, 0) for fac, t in zip(facs, teams)])
red_fac = Sum([If(And(fac, t == 1), 1, 0) for fac, t in zip(facs, teams)])
solver.add(green_fac == 1)
solver.add(red_fac == 1)

# Conditions:
# 1. Juana is assigned to a different team than Olga
solver.add(juana_team != olga_team)

# 2. Lateefah is assigned to the green team
solver.add(lateefah_team == 0)

# 3. Kelly is not a facilitator
solver.add(kelly_fac == False)

# 4. Olga is a facilitator
solver.add(olga_fac == True)

# 5. Mei is assigned to the green team (given in the question)
solver.add(mei_team == 0)

# The question asks what MUST be true.
# We need to check: for each option, is it true in ALL valid models?
# An option MUST be true if its negation is unsatisfiable.

options = {
    "A": (juana_team == 0),        # Juana is assigned to the green team
    "B": (kelly_team == 1),         # Kelly is assigned to the red team
    "C": (olga_team == 0),          # Olga is assigned to the green team
    "D": (lateefah_fac == True),    # Lateefah is a facilitator
    "E": (mei_fac == True),         # Mei is a facilitator
}

must_be_true = []
for letter, constr in options.items():
    solver.push()
    solver.add(Not(constr))  # Try to find a model where the option is FALSE
    result = solver.check()
    if result == unsat:
        # Cannot find a model where option is false => MUST be true
        must_be_true.append(letter)
        print(f"Option {letter}: MUST be true (negation is unsat)")
    else:
        print(f"Option {letter}: NOT necessarily true (found counterexample)")
        m = solver.model()
        print(f"  Counterexample: juana={m[juana_team]}, kelly={m[kelly_team]}, lateefah={m[lateefah_team]}, mei={m[mei_team]}, olga={m[olga_team]}")
        print(f"  Facs: juana={m[juana_fac]}, kelly={m[kelly_fac]}, lateefah={m[lateefah_fac]}, mei={m[mei_fac]}, olga={m[olga_fac]}")
    solver.pop()

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")