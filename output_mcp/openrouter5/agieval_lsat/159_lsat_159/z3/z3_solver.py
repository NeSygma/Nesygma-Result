from z3 import *

solver = Solver()

# Photographers
photographers = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']
P = len(photographers)

# Each photographer is assigned to either Silva (0), Thorne (1), or not assigned (2)
assign = [Int(f'assign_{p}') for p in photographers]

# Domain: 0 = Silva, 1 = Thorne, 2 = Not assigned
for a in assign:
    solver.add(Or(a == 0, a == 1, a == 2))

# Exactly four photographers are assigned (i.e., exactly two are not assigned)
solver.add(Sum([If(a != 2, 1, 0) for a in assign]) == 4)

# At least two photographers at each ceremony
solver.add(Sum([If(a == 0, 1, 0) for a in assign]) >= 2)
solver.add(Sum([If(a == 1, 1, 0) for a in assign]) >= 2)

# Constraint 1: Frost must be assigned together with Heideck to one ceremony
# They must be assigned to the same ceremony (both 0 or both 1), and both assigned (not 2)
solver.add(assign[0] == assign[2])  # Frost and Heideck same assignment
solver.add(assign[0] != 2)          # Frost assigned
solver.add(assign[2] != 2)          # Heideck assigned

# Constraint 2: If Lai and Mays are both assigned, they must be to different ceremonies
# Lai = index 4, Mays = index 5
# If both are assigned (not 2), then they must be different
solver.add(Implies(
    And(assign[4] != 2, assign[5] != 2),
    assign[4] != assign[5]
))

# Constraint 3: If Gonzalez is assigned to Silva (0), then Lai must be assigned to Thorne (1)
# Gonzalez = index 1, Lai = index 4
solver.add(Implies(assign[1] == 0, assign[4] == 1))

# Constraint 4: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
# Knutson = index 3, Heideck = index 2, Mays = index 5
# "not assigned to Thorne" means either assigned to Silva or not assigned at all
solver.add(Implies(
    assign[3] != 1,
    And(assign[2] == 1, assign[5] == 1)
))

# Now evaluate each option: which photographer MUST be assigned to Silva?
# We test each option as "this photographer is assigned to Silva"
# If an option is possible (sat), it's a candidate.
# We need the one that MUST be true, so we also need to check that the negation is unsat.
# But the skeleton tests each option individually. Let's think...
# The question asks "which one of the following MUST be assigned to Silva?"
# So we need to find the photographer who is assigned to Silva in ALL valid assignments.
# Approach: For each photographer, check if there exists a valid assignment where they are NOT assigned to Silva.
# If no such assignment exists, they MUST be assigned to Silva.

# Let's use the skeleton approach: test each option as "this photographer is assigned to Silva"
# and see which one is always true.

# Actually, the skeleton tests each option as a constraint and checks if it's satisfiable.
# For "must be true", we need the option that is true in ALL models.
# So we check: is there a model where this photographer is NOT assigned to Silva?
# If unsat, then they MUST be assigned to Silva.

# Let's do it properly:
# For each photographer, check if there's a valid assignment where they are NOT at Silva.
# If unsat, they must be at Silva.

found_options = []
option_letters = ["A", "B", "C", "D", "E"]
option_indices = [0, 1, 3, 4, 5]  # Frost, Gonzalez, Knutson, Lai, Mays

for letter, idx in zip(option_letters, option_indices):
    solver.push()
    # Check if this photographer can NOT be assigned to Silva
    solver.add(assign[idx] != 0)
    result = solver.check()
    if result == unsat:
        # They MUST be assigned to Silva
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