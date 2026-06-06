from z3 import *

# We will evaluate each option in isolation and check if it fully determines the shelf assignments.
# To do this, we will:
# 1. Add the base constraints.
# 2. For each option, add the option's constraint and check if the shelf assignments are uniquely determined.
# 3. If exactly one option leads to a unique assignment, that is the correct answer.

books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']

found_options = []

# Helper function to check if a set of constraints fully determines the shelf assignments
def is_uniquely_determined(option_constraint):
    solver = Solver()
    book_to_shelf = {book: Int(f'{book}_shelf') for book in books}
    
    # Base constraints
    # 1. At least two books on each shelf
    for shelf in [0, 1, 2]:
        solver.add(Sum([If(book_to_shelf[book] == shelf, 1, 0) for book in books]) >= 2)
    
    # 2. More books on bottom shelf than top shelf
    solver.add(Sum([If(book_to_shelf[book] == 2, 1, 0) for book in books]) > 
               Sum([If(book_to_shelf[book] == 0, 1, 0) for book in books]))
    
    # 3. I is on the middle shelf
    solver.add(book_to_shelf['I'] == 1)
    
    # 4. K is on a higher shelf than F
    solver.add(book_to_shelf['K'] > book_to_shelf['F'])
    
    # 5. O is on a higher shelf than L
    solver.add(book_to_shelf['O'] > book_to_shelf['L'])
    
    # 6. F is on the same shelf as M
    solver.add(book_to_shelf['F'] == book_to_shelf['M'])
    
    # Add the option's constraint
    solver.add(option_constraint)
    
    # Check if the model is satisfiable
    if solver.check() == sat:
        # Now check if the solution is unique by blocking the current model and checking again
        model = solver.model()
        # Create a blocking clause to ensure at least one variable changes
        blocking_clause = []
        for book in books:
            blocking_clause.append(book_to_shelf[book] != model[book_to_shelf[book]])
        solver.add(Or(blocking_clause))
        
        # If the solver cannot find another model, the solution is unique
        if solver.check() == unsat:
            return True
    return False

# Option A: I and M are on the same shelf
solver_A = Solver()
book_to_shelf_A = {book: Int(f'{book}_shelf') for book in books}
solver_A.add(book_to_shelf_A['I'] == book_to_shelf_A['M'])
if is_uniquely_determined(book_to_shelf_A['I'] == book_to_shelf_A['M']):
    found_options.append("A")

# Option B: K and G are on the same shelf
solver_B = Solver()
book_to_shelf_B = {book: Int(f'{book}_shelf') for book in books}
solver_B.add(book_to_shelf_B['K'] == book_to_shelf_B['G'])
if is_uniquely_determined(book_to_shelf_B['K'] == book_to_shelf_B['G']):
    found_options.append("B")

# Option C: L and F are on the same shelf
solver_C = Solver()
book_to_shelf_C = {book: Int(f'{book}_shelf') for book in books}
solver_C.add(book_to_shelf_C['L'] == book_to_shelf_C['F'])
if is_uniquely_determined(book_to_shelf_C['L'] == book_to_shelf_C['F']):
    found_options.append("C")

# Option D: M and H are on the same shelf
solver_D = Solver()
book_to_shelf_D = {book: Int(f'{book}_shelf') for book in books}
solver_D.add(book_to_shelf_D['M'] == book_to_shelf_D['H'])
if is_uniquely_determined(book_to_shelf_D['M'] == book_to_shelf_D['H']):
    found_options.append("D")

# Option E: H and O are on the same shelf
solver_E = Solver()
book_to_shelf_E = {book: Int(f'{book}_shelf') for book in books}
solver_E.add(book_to_shelf_E['H'] == book_to_shelf_E['O'])
if is_uniquely_determined(book_to_shelf_E['H'] == book_to_shelf_E['O']):
    found_options.append("E")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")