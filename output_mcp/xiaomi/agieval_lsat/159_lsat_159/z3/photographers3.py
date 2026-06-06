from z3 import *

# Define photographers
photographers = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']

# For each photographer, define which ceremony they are assigned to
# 0 = not assigned, 1 = Silva University, 2 = Thorne University
assign = {p: Int(f'assign_{p}') for p in photographers}

# Base constraints
def add_base_constraints(solver):
    # Domain constraints
    for p in photographers:
        solver.add(Or(assign[p] == 0, assign[p] == 1, assign[p] == 2))
    
    # Exactly four photographers are assigned (not 0)
    solver.add(Sum([If(assign[p] != 0, 1, 0) for p in photographers]) == 4)
    
    # At least two photographers assigned to Silva University
    solver.add(Sum([If(assign[p] == 1, 1, 0) for p in photographers]) >= 2)
    
    # At least two photographers assigned to Thorne University
    solver.add(Sum([If(assign[p] == 2, 1, 0) for p in photographers]) >= 2)
    
    # Constraint 1: Frost must be assigned together with Heideck to one ceremony
    solver.add(Implies(assign['Frost'] != 0, And(assign['Heideck'] != 0, assign['Frost'] == assign['Heideck'])))
    solver.add(Implies(assign['Heideck'] != 0, And(assign['Frost'] != 0, assign['Frost'] == assign['Heideck'])))
    
    # Constraint 2: If Lai and Mays are both assigned, they must be to different ceremonies
    solver.add(Implies(And(assign['Lai'] != 0, assign['Mays'] != 0), assign['Lai'] != assign['Mays']))
    
    # Constraint 3: If Gonzalez is assigned to Silva (1), then Lai must be assigned to Thorne (2)
    solver.add(Implies(assign['Gonzalez'] == 1, assign['Lai'] == 2))
    
    # Constraint 4: If Knutson is not assigned to Thorne (2), then both Heideck and Mays must be assigned to Thorne (2)
    solver.add(Implies(assign['Knutson'] != 2, And(assign['Heideck'] == 2, assign['Mays'] == 2)))

# First, let's find all valid assignments to understand the problem
s1 = Solver()
add_base_constraints(s1)

print("=== Finding all valid assignments ===")
solutions = []
while s1.check() == sat:
    m = s1.model()
    sol = {p: m[assign[p]].as_long() for p in photographers}
    solutions.append(sol)
    # Block this solution
    s1.add(Or([assign[p] != m[assign[p]] for p in photographers]))

print(f"Total valid assignments: {len(solutions)}")
for i, sol in enumerate(solutions):
    silva = [p for p in photographers if sol[p] == 1]
    thorne = [p for p in photographers if sol[p] == 2]
    unassigned = [p for p in photographers if sol[p] == 0]
    print(f"Solution {i+1}: Silva={silva}, Thorne={thorne}, Unassigned={unassigned}")

# Now check which photographer MUST be assigned to Silva
print("\n=== Checking which photographer MUST be assigned to Silva ===")
must_be_silva = []
for p in photographers:
    s = Solver()
    add_base_constraints(s)
    # Negation: photographer is NOT assigned to Silva (either 0 or 2)
    s.add(Or(assign[p] == 0, assign[p] == 2))
    if s.check() == unsat:
        must_be_silva.append(p)
        print(f"{p} MUST be assigned to Silva (negation is UNSAT)")
    else:
        print(f"{p} does NOT have to be assigned to Silva")

print(f"\nMust be assigned to Silva: {must_be_silva}")

# Map to answer choices
answer_map = {'Frost': 'A', 'Gonzalez': 'B', 'Knutson': 'C', 'Lai': 'D', 'Mays': 'E'}
if len(must_be_silva) == 1:
    print(f"STATUS: sat")
    print(f"answer:{answer_map[must_be_silva[0]]}")
elif len(must_be_silva) > 1:
    print(f"STATUS: sat")
    print(f"Multiple must be assigned: {[answer_map[p] for p in must_be_silva]}")
else:
    print("STATUS: sat")
    print("No photographer must be assigned to Silva")