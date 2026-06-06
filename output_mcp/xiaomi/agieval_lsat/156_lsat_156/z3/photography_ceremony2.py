from z3 import *

# Define photographers
photographers = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']

# For each photographer: 0 = unassigned, 1 = Silva, 2 = Thorne
assignment = {p: Int(f'assign_{p}') for p in photographers}

# Base constraints
def add_base_constraints(solver):
    for p in photographers:
        solver.add(Or(assignment[p] == 0, assignment[p] == 1, assignment[p] == 2))

    # At least 2 photographers at Silva
    solver.add(Sum([If(assignment[p] == 1, 1, 0) for p in photographers]) >= 2)

    # At least 2 photographers at Thorne
    solver.add(Sum([If(assignment[p] == 2, 1, 0) for p in photographers]) >= 2)

    # Constraint 1: Frost and Heideck must be assigned together to the same ceremony
    solver.add(Implies(assignment['Frost'] != 0, assignment['Frost'] == assignment['Heideck']))
    solver.add(Implies(assignment['Heideck'] != 0, assignment['Frost'] == assignment['Heideck']))

    # Constraint 2: If Lai and Mays are both assigned, they must be at different ceremonies
    solver.add(Implies(And(assignment['Lai'] != 0, assignment['Mays'] != 0), assignment['Lai'] != assignment['Mays']))

    # Constraint 3: If Gonzalez is at Silva, then Lai must be at Thorne
    solver.add(Implies(assignment['Gonzalez'] == 1, assignment['Lai'] == 2))

    # Constraint 4: If Knutson is NOT at Thorne, then both Heideck and Mays must be at Thorne
    solver.add(Implies(assignment['Knutson'] != 2, And(assignment['Heideck'] == 2, assignment['Mays'] == 2)))

    # Additional condition: Heideck is assigned to the same ceremony as Lai
    solver.add(assignment['Heideck'] == assignment['Lai'])
    solver.add(assignment['Heideck'] != 0)
    solver.add(assignment['Lai'] != 0)

# Answer choices
options = {
    "A": (assignment['Frost'] == 2),
    "B": (assignment['Gonzalez'] == 1),
    "C": (assignment['Gonzalez'] == 0),
    "D": (assignment['Knutson'] == 2),
    "E": (assignment['Lai'] == 2),
}

# To find what MUST be true, check if negation of each option is UNSAT
must_be_true = []
for letter, constr in options.items():
    s = Solver()
    add_base_constraints(s)
    s.add(Not(constr))  # Try to find a model where the option is FALSE
    result = s.check()
    if result == unsat:
        # The negation is unsatisfiable, so the option MUST be true
        must_be_true.append(letter)
    elif result == sat:
        m = s.model()
        print(f"Option {letter} can be FALSE. Counterexample:")
        for p in photographers:
            val = m[assignment[p]]
            if val == 0:
                print(f"  {p}: unassigned")
            elif val == 1:
                print(f"  {p}: Silva")
            elif val == 2:
                print(f"  {p}: Thorne")
    else:
        print(f"Option {letter}: unknown")

print()
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: sat")
    print(f"Multiple must-be-true: {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No option must be true")