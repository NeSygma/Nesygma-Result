from z3 import *

# Countries: Venezuela (0), Yemen (1), Zambia (2)
# Candidates: Jaramillo (0), Kayne (1), Landon (2), Novetzke (3), Ong (4)

# Assignment variables: assignment[c] = country assigned to candidate c, or -1 if not assigned
assignment = [Int(f'assignment_{i}') for i in range(5)]

# Each country must be assigned exactly one candidate
country_assigned = [Int(f'country_{i}') for i in range(3)]

# Initialize country assignments to -1 (unassigned)
solver = Solver()
for i in range(5):
    solver.add(assignment[i] >= -1, assignment[i] < 3)
for i in range(3):
    solver.add(country_assigned[i] >= -1, country_assigned[i] < 5)

# Each country is assigned exactly one candidate
for i in range(3):
    solver.add(Or([country_assigned[i] == j for j in range(5)]))
    solver.add(Distinct([country_assigned[i] for i in range(3)]))

# Each candidate is assigned to at most one country
for i in range(5):
    solver.add(Or([assignment[i] == j for j in range(3)] + [assignment[i] == -1]))
    for j in range(i+1, 5):
        solver.add(Not(And(assignment[i] >= 0, assignment[j] >= 0, assignment[i] == assignment[j])))

# Constraint 1: Either Kayne (1) or Novetzke (3), but not both, is assigned
solver.add(Or(And(assignment[1] >= 0, assignment[3] == -1),
              And(assignment[3] >= 0, assignment[1] == -1)))

# Constraint 2: If Jaramillo (0) is assigned, then Kayne (1) is also assigned
solver.add(Implies(assignment[0] >= 0, assignment[1] >= 0))

# Constraint 3: If Ong (4) is assigned to Venezuela (0), then Kayne (1) is not assigned to Yemen (1)
solver.add(Implies(assignment[4] == 0, assignment[1] != 1))

# Constraint 4: If Landon (2) is assigned, it is to Zambia (2)
solver.add(Implies(assignment[2] >= 0, assignment[2] == 2))

# Link assignment variables to country assignments
for c in range(3):
    for cand in range(5):
        solver.add(Implies(country_assigned[c] == cand, assignment[cand] == c))

# For each option, check if the pair of candidates are not assigned
found_options = []

# Option A: Jaramillo (0) and Novetzke (3) are not assigned
solver.push()
solver.add(assignment[0] == -1)
solver.add(assignment[3] == -1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Jaramillo (0) and Ong (4) are not assigned
solver.push()
solver.add(assignment[0] == -1)
solver.add(assignment[4] == -1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Kayne (1) and Landon (2) are not assigned
solver.push()
solver.add(assignment[1] == -1)
solver.add(assignment[2] == -1)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Kayne (1) and Novetzke (3) are not assigned
solver.push()
solver.add(assignment[1] == -1)
solver.add(assignment[3] == -1)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Landon (2) and Ong (4) are not assigned
solver.push()
solver.add(assignment[2] == -1)
solver.add(assignment[4] == -1)
if solver.check() == sat:
    found_options.append("E")
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