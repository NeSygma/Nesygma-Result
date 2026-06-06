from z3 import *

# Days: 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday
# Cookie types: O=Oatmeal, P=Peanut butter, S=Sugar
# Batches: 1,2,3 for each type

# Declare variables for each batch's day
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

solver = Solver()

# Domain constraints: each batch is made on a day 1-5
all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]
for batch in all_batches:
    solver.add(batch >= 1, batch <= 5)

# Constraint 3: No two batches of the same kind on the same day
solver.add(Distinct([O1, O2, O3]))  # Oatmeal batches on different days
solver.add(Distinct([P1, P2, P3]))  # Peanut butter batches on different days
solver.add(Distinct([S1, S2, S3]))  # Sugar batches on different days

# Constraint 4: At least one batch on Monday
solver.add(Or([batch == 1 for batch in all_batches]))

# Constraint 5: O2 made on same day as P1
solver.add(O2 == P1)

# Constraint 6: S2 made on Thursday (day 4)
solver.add(S2 == 4)

# Constraint 7: No batch on Wednesday (day 3)
solver.add(And([batch != 3 for batch in all_batches]))

# Now test each answer choice for necessity
# Answer choices:
# (A) Exactly three batches of cookies are made on Tuesday.
# (B) Exactly three batches of cookies are made on Friday.
# (C) At least two batches of cookies are made on Monday.
# (D) At least two batches of cookies are made on Thursday.
# (E) Fewer batches of cookies are made on Monday than on Tuesday.

# Define constraints for each option
opt_a = Sum([If(batch == 2, 1, 0) for batch in all_batches]) == 3
opt_b = Sum([If(batch == 5, 1, 0) for batch in all_batches]) == 3
opt_c = Sum([If(batch == 1, 1, 0) for batch in all_batches]) >= 2
opt_d = Sum([If(batch == 4, 1, 0) for batch in all_batches]) >= 2
opt_e = Sum([If(batch == 1, 1, 0) for batch in all_batches]) < Sum([If(batch == 2, 1, 0) for batch in all_batches])

# For each option, check if its negation is unsatisfiable
# If negation is unsat, then the option must be true in all models
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    # Create a new solver for this test
    test_solver = Solver()
    # Add all base constraints
    for batch in all_batches:
        test_solver.add(batch >= 1, batch <= 5)
    test_solver.add(Distinct([O1, O2, O3]))
    test_solver.add(Distinct([P1, P2, P3]))
    test_solver.add(Distinct([S1, S2, S3]))
    test_solver.add(Or([batch == 1 for batch in all_batches]))
    test_solver.add(O2 == P1)
    test_solver.add(S2 == 4)
    test_solver.add(And([batch != 3 for batch in all_batches]))
    
    # Add the negation of the option
    test_solver.add(Not(constr))
    
    # Check if negation is unsatisfiable
    if test_solver.check() == unsat:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")