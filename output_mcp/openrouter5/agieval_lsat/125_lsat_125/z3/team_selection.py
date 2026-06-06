from z3 import *

# Variables: True if the employee is on the team
Myers, Ortega, Paine, Schmidt, Thomson, Wong, Yoder, Zayre = Bools('Myers Ortega Paine Schmidt Thomson Wong Yoder Zayre')

solver = Solver()

# At least four employees on the team
solver.add(Sum([Myers, Ortega, Paine, Schmidt, Thomson, Wong, Yoder, Zayre]) >= 4)

# Condition 1: If Myers is on the team, neither Ortega nor Paine can be.
solver.add(Implies(Myers, And(Not(Ortega), Not(Paine))))

# Condition 2: If Schmidt is on the team, both Paine and Thomson must also be.
solver.add(Implies(Schmidt, And(Paine, Thomson)))

# Condition 3: If Wong is on the team, both Myers and Yoder must also be.
solver.add(Implies(Wong, And(Myers, Yoder)))

# Given: Yoder is not on the team
solver.add(Not(Yoder))

# Now evaluate each option: "could be on the team" means it's possible for that person to be on the team
# under the given constraints (including Yoder not being on the team).
# We need to find which one CANNOT be on the team (i.e., is impossible).

found_options = []

# Option A: Zayre could be on the team
opt_a = Zayre
# Option B: Thomson could be on the team
opt_b = Thomson
# Option C: Paine could be on the team
opt_c = Paine
# Option D: Ortega could be on the team
opt_d = Ortega
# Option E: Myers could be on the team
opt_e = Myers

for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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