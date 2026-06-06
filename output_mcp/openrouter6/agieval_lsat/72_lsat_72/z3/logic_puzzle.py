from z3 import *

# Define assistants
assistants = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]
# Session indices: 0: Wed AM, 1: Wed PM, 2: Thu AM, 3: Thu PM, 4: Fri AM, 5: Fri PM
session = {a: Int(f"session_{a}") for a in assistants}

solver = Solver()

# All sessions must be distinct (each session assigned to exactly one assistant)
solver.add(Distinct([session[a] for a in assistants]))

# Domain constraints: session indices between 0 and 5
for a in assistants:
    solver.add(session[a] >= 0)
    solver.add(session[a] <= 5)

# Constraint 1: Kevin and Rebecca same day
solver.add(session["Kevin"] / 2 == session["Rebecca"] / 2)

# Constraint 2: Lan and Olivia different days
solver.add(session["Lan"] / 2 != session["Olivia"] / 2)

# Constraint 3: Nessa afternoon
solver.add(session["Nessa"] % 2 == 1)

# Constraint 4: Julio earlier day than Olivia
solver.add(session["Julio"] / 2 < session["Olivia"] / 2)

# Additional condition: Lan does not lead a Wednesday session
# Wednesday is day 0 (session indices 0,1)
solver.add(session["Lan"] / 2 != 0)

# Now evaluate multiple choice options
# For each option, we add the constraint that the assistant leads a Thursday session (day 1)
# Thursday sessions are indices 2 and 3, so day = 1
opt_a_constr = (session["Rebecca"] / 2 == 1)
opt_b_constr = (session["Olivia"] / 2 == 1)
opt_c_constr = (session["Nessa"] / 2 == 1)
opt_d_constr = (session["Kevin"] / 2 == 1)
opt_e_constr = (session["Julio"] / 2 == 1)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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