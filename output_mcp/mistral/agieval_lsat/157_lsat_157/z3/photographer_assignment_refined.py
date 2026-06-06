from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for each photographer's assignment
# 0 = not assigned, 1 = Silva University, 2 = Thorne University
photographers = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']
assign = {p: Int(f'assign_{p}') for p in photographers}

# Base constraints
solver = Solver()

# Each photographer is either not assigned (0), assigned to Silva (1), or assigned to Thorne (2)
for p in photographers:
    solver.add(Or(assign[p] == 0, assign[p] == 1, assign[p] == 2))

# At least two photographers must be assigned to each ceremony
silva_assigned = [assign[p] == 1 for p in photographers]
thorne_assigned = [assign[p] == 2 for p in photographers]
solver.add(Sum(silva_assigned) >= 2)
solver.add(Sum(thorne_assigned) >= 2)

# Constraint 1: Frost must be assigned together with Heideck to one of the ceremonies
solver.add(Or(
    And(assign['Frost'] == 1, assign['Heideck'] == 1),
    And(assign['Frost'] == 2, assign['Heideck'] == 2)
))

# Constraint 2: If Lai and Mays are both assigned, they must be assigned to different ceremonies
solver.add(Implies(
    And(assign['Lai'] != 0, assign['Mays'] != 0),
    Or(
        And(assign['Lai'] == 1, assign['Mays'] == 2),
        And(assign['Lai'] == 2, assign['Mays'] == 1)
    )
))

# Constraint 3: If Gonzalez is assigned to Silva University, then Lai must be assigned to Thorne University
solver.add(Implies(
    assign['Gonzalez'] == 1,
    assign['Lai'] == 2
))

# Constraint 4: If Knutson is not assigned to Thorne University, then both Heideck and Mays must be assigned to Thorne University
solver.add(Implies(
    assign['Knutson'] != 2,
    And(assign['Heideck'] == 2, assign['Mays'] == 2)
))

# Now evaluate each multiple-choice option
# Each option specifies the photographers assigned to Silva University
# We will encode the option as constraints and check for satisfiability

found_options = []

# Option A: Frost, Gonzalez, Heideck, Knutson assigned to Silva
solver.push()
solver.add(assign['Frost'] == 1)
solver.add(assign['Gonzalez'] == 1)
solver.add(assign['Heideck'] == 1)
solver.add(assign['Knutson'] == 1)
solver.add(assign['Lai'] == 0)  # Lai not assigned
solver.add(assign['Mays'] == 0)  # Mays not assigned

if solver.check() == sat:
    found_options.append("A")
    print("Option A is SAT")
else:
    print("Option A is UNSAT")
solver.pop()

# Option B: Frost, Gonzalez, Heideck assigned to Silva
solver.push()
solver.add(assign['Frost'] == 1)
solver.add(assign['Gonzalez'] == 1)
solver.add(assign['Heideck'] == 1)
solver.add(assign['Knutson'] == 0)  # Knutson not assigned
solver.add(assign['Lai'] == 0)  # Lai not assigned
solver.add(assign['Mays'] == 0)  # Mays not assigned

if solver.check() == sat:
    found_options.append("B")
    print("Option B is SAT")
else:
    print("Option B is UNSAT")
solver.pop()

# Option C: Gonzalez, Knutson assigned to Silva
solver.push()
solver.add(assign['Gonzalez'] == 1)
solver.add(assign['Knutson'] == 1)
solver.add(assign['Frost'] == 0)  # Frost not assigned
solver.add(assign['Heideck'] == 0)  # Heideck not assigned
solver.add(assign['Lai'] == 0)  # Lai not assigned
solver.add(assign['Mays'] == 0)  # Mays not assigned

if solver.check() == sat:
    found_options.append("C")
    print("Option C is SAT")
else:
    print("Option C is UNSAT")
solver.pop()

# Option D: Heideck, Lai assigned to Silva
solver.push()
solver.add(assign['Heideck'] == 1)
solver.add(assign['Lai'] == 1)
solver.add(assign['Frost'] == 0)  # Frost not assigned
solver.add(assign['Gonzalez'] == 0)  # Gonzalez not assigned
solver.add(assign['Knutson'] == 0)  # Knutson not assigned
solver.add(assign['Mays'] == 0)  # Mays not assigned

if solver.check() == sat:
    found_options.append("D")
    print("Option D is SAT")
else:
    print("Option D is UNSAT")
solver.pop()

# Option E: Knutson, Mays assigned to Silva
solver.push()
solver.add(assign['Knutson'] == 1)
solver.add(assign['Mays'] == 1)
solver.add(assign['Frost'] == 0)  # Frost not assigned
solver.add(assign['Gonzalez'] == 0)  # Gonzalez not assigned
solver.add(assign['Heideck'] == 0)  # Heideck not assigned
solver.add(assign['Lai'] == 0)  # Lai not assigned

if solver.check() == sat:
    found_options.append("E")
    print("Option E is SAT")
else:
    print("Option E is UNSAT")
solver.pop()

# Determine the result based on found_options
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")