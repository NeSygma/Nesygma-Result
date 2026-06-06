from z3 import *

# Define businesses
businesses = ['pharmacy', 'optometrist', 'restaurant1', 'restaurant2', 'shoe_store', 'toy_store', 'veterinarian']

# Create position variables for each business (1-7)
pos = {b: Int(f'pos_{b}') for b in businesses}

def get_solutions_with_constraint(constraint_func):
    """Get all solutions with a specific constraint function"""
    solver = Solver()
    
    # All positions must be between 1 and 7
    for b in businesses:
        solver.add(pos[b] >= 1, pos[b] <= 7)
    
    # All positions must be distinct
    solver.add(Distinct([pos[b] for b in businesses]))
    
    # Constraint 1: Pharmacy at one end, restaurant at other end
    solver.add(Or(pos['pharmacy'] == 1, pos['pharmacy'] == 7))
    solver.add(Or(pos['restaurant1'] == 1, pos['restaurant1'] == 7, 
                  pos['restaurant2'] == 1, pos['restaurant2'] == 7))
    solver.add(Or(
        And(pos['pharmacy'] == 1, Or(pos['restaurant1'] == 7, pos['restaurant2'] == 7)),
        And(pos['pharmacy'] == 7, Or(pos['restaurant1'] == 1, pos['restaurant2'] == 1))
    ))
    
    # Constraint 3: Pharmacy next to optometrist or veterinarian
    solver.add(Or(
        pos['pharmacy'] - pos['optometrist'] == 1,
        pos['optometrist'] - pos['pharmacy'] == 1,
        pos['pharmacy'] - pos['veterinarian'] == 1,
        pos['veterinarian'] - pos['pharmacy'] == 1
    ))
    
    # Constraint 4: Toy store not next to veterinarian
    solver.add(And(
        pos['toy_store'] - pos['veterinarian'] != 1,
        pos['veterinarian'] - pos['toy_store'] != 1
    ))
    
    # Add the specific constraint
    constraint_func(solver)
    
    # Collect all solutions
    solutions = []
    while solver.check() == sat:
        m = solver.model()
        sol = {b: m[pos[b]].as_long() for b in businesses}
        solutions.append(sol)
        
        # Block this solution
        solver.add(Or([pos[b] != sol[b] for b in businesses]))
    
    return solutions

# Define constraint functions
def original_constraint(solver):
    solver.add(Or(
        pos['restaurant1'] - pos['restaurant2'] >= 3,
        pos['restaurant2'] - pos['restaurant1'] >= 3
    ))

def option_a_constraint(solver):
    solver.add(Or(
        pos['restaurant1'] == 3, pos['restaurant1'] == 4, pos['restaurant1'] == 5,
        pos['restaurant2'] == 3, pos['restaurant2'] == 4, pos['restaurant2'] == 5
    ))

def option_b_constraint(solver):
    solver.add(Or(
        Or(pos['restaurant1'] - pos['optometrist'] == 1, pos['optometrist'] - pos['restaurant1'] == 1),
        Or(pos['restaurant1'] - pos['veterinarian'] == 1, pos['veterinarian'] - pos['restaurant1'] == 1),
        Or(pos['restaurant2'] - pos['optometrist'] == 1, pos['optometrist'] - pos['restaurant2'] == 1),
        Or(pos['restaurant2'] - pos['veterinarian'] == 1, pos['veterinarian'] - pos['restaurant2'] == 1)
    ))

def option_c_constraint(solver):
    solver.add(Or(
        And(pos['restaurant1'] < pos['toy_store'], pos['toy_store'] < pos['restaurant2']),
        And(pos['restaurant2'] < pos['toy_store'], pos['toy_store'] < pos['restaurant1']),
        And(pos['restaurant1'] < pos['veterinarian'], pos['veterinarian'] < pos['restaurant2']),
        And(pos['restaurant2'] < pos['veterinarian'], pos['veterinarian'] < pos['restaurant1'])
    ))

def option_d_constraint(solver):
    # No more than two businesses can separate the pharmacy and the restaurant nearest it
    # This means distance between pharmacy and nearest restaurant <= 3
    solver.add(Or(
        # Pharmacy at 1: nearest restaurant must be at 2, 3, or 4
        And(pos['pharmacy'] == 1, Or(
            And(pos['restaurant1'] <= 4, pos['restaurant1'] >= 2),
            And(pos['restaurant2'] <= 4, pos['restaurant2'] >= 2)
        )),
        # Pharmacy at 7: nearest restaurant must be at 4, 5, or 6
        And(pos['pharmacy'] == 7, Or(
            And(pos['restaurant1'] >= 4, pos['restaurant1'] <= 6),
            And(pos['restaurant2'] >= 4, pos['restaurant2'] <= 6)
        ))
    ))

def option_e_constraint(solver):
    solver.add(And(
        pos['optometrist'] - pos['shoe_store'] != 1,
        pos['shoe_store'] - pos['optometrist'] != 1
    ))

# Get solutions with original constraint
original_solutions = get_solutions_with_constraint(original_constraint)
print(f"Original constraint gives {len(original_solutions)} solutions")

# Test each option
options = [
    ("A", option_a_constraint),
    ("B", option_b_constraint),
    ("C", option_c_constraint),
    ("D", option_d_constraint),
    ("E", option_e_constraint)
]

matching_options = []
for letter, constraint_func in options:
    option_solutions = get_solutions_with_constraint(constraint_func)
    print(f"Option {letter} gives {len(option_solutions)} solutions")
    
    # Check if the sets of solutions are identical
    if len(option_solutions) == len(original_solutions):
        # Convert to sets of tuples for comparison
        orig_set = set(tuple(sorted(sol.items())) for sol in original_solutions)
        opt_set = set(tuple(sorted(sol.items())) for sol in option_solutions)
        if orig_set == opt_set:
            matching_options.append(letter)
            print(f"Option {letter} matches!")

print(f"\nMatching options: {matching_options}")

# Now use the exact skeleton for multiple choice evaluation
found_options = []
for letter, constr in [("A", option_a_constraint), ("B", option_b_constraint), 
                       ("C", option_c_constraint), ("D", option_d_constraint), 
                       ("E", option_e_constraint)]:
    solver = Solver()
    # Add base constraints
    for b in businesses:
        solver.add(pos[b] >= 1, pos[b] <= 7)
    solver.add(Distinct([pos[b] for b in businesses]))
    solver.add(Or(pos['pharmacy'] == 1, pos['pharmacy'] == 7))
    solver.add(Or(pos['restaurant1'] == 1, pos['restaurant1'] == 7, 
                  pos['restaurant2'] == 1, pos['restaurant2'] == 7))
    solver.add(Or(
        And(pos['pharmacy'] == 1, Or(pos['restaurant1'] == 7, pos['restaurant2'] == 7)),
        And(pos['pharmacy'] == 7, Or(pos['restaurant1'] == 1, pos['restaurant2'] == 1))
    ))
    solver.add(Or(
        pos['pharmacy'] - pos['optometrist'] == 1,
        pos['optometrist'] - pos['pharmacy'] == 1,
        pos['pharmacy'] - pos['veterinarian'] == 1,
        pos['veterinarian'] - pos['pharmacy'] == 1
    ))
    solver.add(And(
        pos['toy_store'] - pos['veterinarian'] != 1,
        pos['veterinarian'] - pos['toy_store'] != 1
    ))
    
    solver.push()
    constr(solver)
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