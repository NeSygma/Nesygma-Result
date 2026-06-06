from z3 import *

solver = Solver()

# Declare employees as boolean variables
employees = {
    "Myers": Bool("Myers"),
    "Ortega": Bool("Ortega"),
    "Paine": Bool("Paine"),
    "Schmidt": Bool("Schmidt"),
    "Thomson": Bool("Thomson"),
    "Wong": Bool("Wong"),
    "Yoder": Bool("Yoder"),
    "Zayre": Bool("Zayre")
}

# Base constraint: Team must include at least four employees
solver.add(Sum(list(employees.values())) >= 4)

# Constraints from the problem statement
# 1. If Myers is on the team, neither Ortega nor Paine can be.
solver.add(Implies(employees["Myers"], And(Not(employees["Ortega"]), Not(employees["Paine"]))))

# 2. If Schmidt is on the team, both Paine and Thomson must also be.
solver.add(Implies(employees["Schmidt"], And(employees["Paine"], employees["Thomson"])))

# 3. If Wong is on the team, both Myers and Yoder must also be.
solver.add(Implies(employees["Wong"], And(employees["Myers"], employees["Yoder"])))

# Define the options as constraints
# (A) Myers and Thomson cannot be on the team together
opt_a_constr = And(employees["Myers"], employees["Thomson"])

# (B) Ortega and Yoder cannot be on the team together
opt_b_constr = And(employees["Ortega"], employees["Yoder"])

# (C) Paine and Zayre cannot be on the team together
opt_c_constr = And(employees["Paine"], employees["Zayre"])

# (D) Schmidt and Wong cannot be on the team together
opt_d_constr = And(employees["Schmidt"], employees["Wong"])

# (E) Wong and Yoder cannot be on the team together
opt_e_constr = And(employees["Wong"], employees["Yoder"])

# Evaluate each option
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