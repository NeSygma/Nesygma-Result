from z3 import *

solver = Solver()

# Declare symbolic variables for each employee (True if selected, False otherwise)
employees = {
    "Myers": Bool("Myers"),
    "Ortega": Bool("Ortega"),
    "Paine": Bool("Paine"),
    "Schmidt": Bool("Schmidt"),
    "Thomson": Bool("Thomson"),
    "Wong": Bool("Wong"),
    "Yoder": Bool("Yoder"),
    "Zayre": Bool("Zayre"),
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
option_constraints = {
    "A": And(
        employees["Myers"],
        employees["Paine"],
        employees["Schmidt"],
        employees["Thomson"],
        Not(employees["Ortega"]),
        Not(employees["Wong"]),
        Not(employees["Yoder"]),
        Not(employees["Zayre"])
    ),
    "B": And(
        employees["Ortega"],
        employees["Paine"],
        employees["Thomson"],
        employees["Zayre"],
        Not(employees["Myers"]),
        Not(employees["Schmidt"]),
        Not(employees["Wong"]),
        Not(employees["Yoder"])
    ),
    "C": And(
        employees["Paine"],
        employees["Schmidt"],
        employees["Yoder"],
        employees["Zayre"],
        Not(employees["Myers"]),
        Not(employees["Ortega"]),
        Not(employees["Thomson"]),
        Not(employees["Wong"])
    ),
    "D": And(
        employees["Schmidt"],
        employees["Thomson"],
        employees["Yoder"],
        employees["Zayre"],
        Not(employees["Myers"]),
        Not(employees["Ortega"]),
        Not(employees["Paine"]),
        Not(employees["Wong"])
    ),
    "E": And(
        employees["Thomson"],
        employees["Wong"],
        employees["Yoder"],
        employees["Zayre"],
        Not(employees["Myers"]),
        Not(employees["Ortega"]),
        Not(employees["Paine"]),
        Not(employees["Schmidt"])
    ),
}

# Evaluate each option
found_options = []
for letter, constr in option_constraints.items():
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