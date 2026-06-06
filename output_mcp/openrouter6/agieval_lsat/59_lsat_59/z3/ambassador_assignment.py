from z3 import *

# Candidate indices
JARAMILLO = 0
KAYNE = 1
LANDON = 2
NOVETZKE = 3
ONG = 4

# Country codes
NONE = 0
VENEZUELA = 1
YEMEN = 2
ZAMBIA = 3

def get_all_solutions(constraints):
    """Return a set of assignments (tuple of 5 country values) that satisfy constraints."""
    solver = Solver()
    # Declare variables
    c = [Int(f'c_{i}') for i in range(5)]
    
    # Base constraints: each variable in 0..3
    for ci in c:
        solver.add(ci >= 0, ci <= 3)
    
    # Add given constraints
    for constr in constraints:
        solver.add(constr)
    
    # Enumerate all solutions
    solutions = set()
    while solver.check() == sat:
        m = solver.model()
        # Get assignment as tuple
        assignment = tuple(m.eval(c[i], model_completion=True).as_long() for i in range(5))
        solutions.add(assignment)
        # Blocking clause: at least one variable differs
        solver.add(Or([c[i] != assignment[i] for i in range(5)]))
    return solutions

# Define base constraints (excluding the Jaramillo-Kayne constraint)
c = [Int(f'c_{i}') for i in range(5)]

# Exactly three assigned
base_constraints = [
    Sum([If(ci != 0, 1, 0) for ci in c]) == 3
]

# Each country assigned exactly once
for country in [VENEZUELA, YEMEN, ZAMBIA]:
    base_constraints.append(Sum([If(ci == country, 1, 0) for ci in c]) == 1)

# Exactly one of Kayne and Novetzke assigned
base_constraints.append( (c[KAYNE] != 0) != (c[NOVETZKE] != 0) )

# Ong to Venezuela constraint
base_constraints.append( Implies(c[ONG] == VENEZUELA, c[KAYNE] != YEMEN) )

# Landon to Zambia constraint
base_constraints.append( Implies(c[LANDON] != 0, c[LANDON] == ZAMBIA) )

# Original constraint: If Jaramillo assigned, then Kayne assigned
original_constraint = Implies(c[JARAMILLO] != 0, c[KAYNE] != 0)

# Candidate constraints
candidate_constraints = {
    'A': Implies(c[KAYNE] != 0, c[JARAMILLO] != 0),
    'B': Implies(And(c[LANDON] != 0, c[ONG] != 0), c[NOVETZKE] != 0),
    'C': Implies(c[ONG] == 0, c[KAYNE] != 0),
    'D': Not(And(c[JARAMILLO] != 0, c[NOVETZKE] != 0)),
    'E': Not(And(c[NOVETZKE] != 0, c[ONG] != 0))
}

# Get solutions with original constraint
original_solutions = get_all_solutions(base_constraints + [original_constraint])
print(f"Original solutions count: {len(original_solutions)}")

# For each candidate, get solutions with candidate constraint
found_options = []
for letter, cand_constr in candidate_constraints.items():
    cand_solutions = get_all_solutions(base_constraints + [cand_constr])
    print(f"Candidate {letter} solutions count: {len(cand_solutions)}")
    if original_solutions == cand_solutions:
        found_options.append(letter)

print(f"Found options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")