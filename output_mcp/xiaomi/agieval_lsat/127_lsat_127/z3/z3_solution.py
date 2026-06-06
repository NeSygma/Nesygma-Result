from z3 import *

solver = Solver()

# Boolean variables for each employee
Myers = Bool('Myers')
Ortega = Bool('Ortega')
Paine = Bool('Paine')
Schmidt = Bool('Schmidt')
Thomson = Bool('Thomson')
Wong = Bool('Wong')
Yoder = Bool('Yoder')
Zayre = Bool('Zayre')

employees = [Myers, Ortega, Paine, Schmidt, Thomson, Wong, Yoder, Zayre]

# At least four employees on the team
solver.add(Sum([If(e, 1, 0) for e in employees]) >= 4)

# Condition 1: If Myers is on the team, neither Ortega nor Paine can be
solver.add(Implies(Myers, And(Not(Ortega), Not(Paine))))

# Condition 2: If Schmidt is on the team, both Paine and Thomson must also be
solver.add(Implies(Schmidt, And(Paine, Thomson)))

# Condition 3: If Wong is on the team, both Myers and Yoder must also be
solver.add(Implies(Wong, And(Myers, Yoder)))

# Now test each option: "at least one of whom must be on the team"
# This means: for every valid team, at least one of the pair is on it.
# Equivalently: it is UNSATISFIABLE that NEITHER is on the team.
# So we check: can we find a valid team where NEITHER of the pair is on it?
# If NOT satisfiable (unsat), then at least one MUST be on the team.

def must_be_on_team(emp1, emp2):
    """Returns True if at least one of emp1, emp2 must be on every valid team."""
    s = Solver()
    # Copy all base constraints
    s.add(Sum([If(e, 1, 0) for e in employees]) >= 4)
    s.add(Implies(Myers, And(Not(Ortega), Not(Paine))))
    s.add(Implies(Schmidt, And(Paine, Thomson)))
    s.add(Implies(Wong, And(Myers, Yoder)))
    # Add: NEITHER emp1 nor emp2 is on the team
    s.add(Not(emp1))
    s.add(Not(emp2))
    return s.check() == unsat

# Option A: Ortega and Schmidt
opt_a = must_be_on_team(Ortega, Schmidt)
# Option B: Ortega and Wong
opt_b = must_be_on_team(Ortega, Wong)
# Option C: Paine and Schmidt
opt_c = must_be_on_team(Paine, Schmidt)
# Option D: Thomson and Yoder
opt_d = must_be_on_team(Thomson, Yoder)
# Option E: Yoder and Zayre
opt_e = must_be_on_team(Yoder, Zayre)

found_options = []
if opt_a:
    found_options.append("A")
if opt_b:
    found_options.append("B")
if opt_c:
    found_options.append("C")
if opt_d:
    found_options.append("D")
if opt_e:
    found_options.append("E")

print(f"Option A (Ortega and Schmidt): {'must be' if opt_a else 'not required'}")
print(f"Option B (Ortega and Wong): {'must be' if opt_b else 'not required'}")
print(f"Option C (Paine and Schmidt): {'must be' if opt_c else 'not required'}")
print(f"Option D (Thomson and Yoder): {'must be' if opt_d else 'not required'}")
print(f"Option E (Yoder and Zayre): {'must be' if opt_e else 'not required'}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")