from z3 import *

# Create solver
solver = Solver()

# Photographers: 0=Frost, 1=Gonzalez, 2=Heideck, 3=Knutson, 4=Lai, 5=Mays
photographers = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]
n = len(photographers)

# Variables: assignment[i] = 0 (not assigned), 1 (Silva), 2 (Thorne)
assignment = [Int(f"assign_{i}") for i in range(n)]

# Domain constraints: each photographer can be 0, 1, or 2
for i in range(n):
    solver.add(Or(assignment[i] == 0, assignment[i] == 1, assignment[i] == 2))

# No photographer assigned to both ceremonies (already enforced by domain)

# At least 2 photographers assigned to each ceremony
silva_count = Sum([If(assignment[i] == 1, 1, 0) for i in range(n)])
thorne_count = Sum([If(assignment[i] == 2, 1, 0) for i in range(n)])
solver.add(silva_count >= 2)
solver.add(thorne_count >= 2)

# Constraint 1: Frost must be assigned together with Heideck to one ceremony
solver.add(Or(
    And(assignment[0] == 0, assignment[2] == 0),  # both unassigned
    And(assignment[0] == 1, assignment[2] == 1),  # both to Silva
    And(assignment[0] == 2, assignment[2] == 2)   # both to Thorne
))

# Constraint 2: If Lai and Mays are both assigned, they must be to different ceremonies
solver.add(Implies(
    And(assignment[4] != 0, assignment[5] != 0),
    assignment[4] != assignment[5]
))

# Constraint 3: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(
    assignment[1] == 1,
    assignment[4] == 2
))

# Constraint 4: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
solver.add(Implies(
    assignment[3] != 2,
    And(assignment[2] == 2, assignment[5] == 2)
))

# Now test each answer choice for Thorne University ceremony
# We want to find which option CANNOT be the complete assignment to Thorne
# This means when we add the option constraints, the solver should return unsat

impossible_options = []

# Option A: Frost, Gonzalez, Heideck, Mays (indices 0, 1, 2, 5)
opt_a_constr = And(
    assignment[0] == 2,  # Frost to Thorne
    assignment[1] == 2,  # Gonzalez to Thorne
    assignment[2] == 2,  # Heideck to Thorne
    assignment[5] == 2,  # Mays to Thorne
    # Others not in Thorne (they could be Silva or unassigned)
    assignment[3] != 2,  # Knutson not in Thorne
    assignment[4] != 2   # Lai not in Thorne
)

# Option B: Frost, Heideck, Knutson, Mays (indices 0, 2, 3, 5)
opt_b_constr = And(
    assignment[0] == 2,  # Frost to Thorne
    assignment[2] == 2,  # Heideck to Thorne
    assignment[3] == 2,  # Knutson to Thorne
    assignment[5] == 2,  # Mays to Thorne
    # Others not in Thorne
    assignment[1] != 2,  # Gonzalez not in Thorne
    assignment[4] != 2   # Lai not in Thorne
)

# Option C: Gonzalez, Knutson, Lai (indices 1, 3, 4)
opt_c_constr = And(
    assignment[1] == 2,  # Gonzalez to Thorne
    assignment[3] == 2,  # Knutson to Thorne
    assignment[4] == 2,  # Lai to Thorne
    # Others not in Thorne
    assignment[0] != 2,  # Frost not in Thorne
    assignment[2] != 2,  # Heideck not in Thorne
    assignment[5] != 2   # Mays not in Thorne
)

# Option D: Gonzalez, Knutson, Mays (indices 1, 3, 5)
opt_d_constr = And(
    assignment[1] == 2,  # Gonzalez to Thorne
    assignment[3] == 2,  # Knutson to Thorne
    assignment[5] == 2,  # Mays to Thorne
    # Others not in Thorne
    assignment[0] != 2,  # Frost not in Thorne
    assignment[2] != 2,  # Heideck not in Thorne
    assignment[4] != 2   # Lai not in Thorne
)

# Option E: Knutson, Mays (indices 3, 5)
opt_e_constr = And(
    assignment[3] == 2,  # Knutson to Thorne
    assignment[5] == 2,  # Mays to Thorne
    # Others not in Thorne
    assignment[0] != 2,  # Frost not in Thorne
    assignment[1] != 2,  # Gonzalez not in Thorne
    assignment[2] != 2,  # Heideck not in Thorne
    assignment[4] != 2   # Lai not in Thorne
)

# Test each option - if adding it makes the problem unsat, then it CANNOT be the assignment
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        impossible_options.append(letter)
    solver.pop()

# Print results
if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")