from z3 import *

# Days: 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday
# Cookie types: O=Oatmeal, P=Peanut butter, S=Sugar
# Batches: 1,2,3 for each type

# Declare variables for each batch's day
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

# Base constraints
def add_base_constraints(solver):
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

# Define the options as constraints that must be true
# Option A: Exactly three batches of cookies are made on Tuesday (day 2)
def opt_a_constraint():
    all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]
    # Count batches on Tuesday (day 2)
    tuesday_count = Sum([If(batch == 2, 1, 0) for batch in all_batches])
    return tuesday_count == 3

# Option B: Exactly three batches of cookies are made on Friday (day 5)
def opt_b_constraint():
    all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]
    friday_count = Sum([If(batch == 5, 1, 0) for batch in all_batches])
    return friday_count == 3

# Option C: At least two batches of cookies are made on Monday (day 1)
def opt_c_constraint():
    all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]
    monday_count = Sum([If(batch == 1, 1, 0) for batch in all_batches])
    return monday_count >= 2

# Option D: At least two batches of cookies are made on Thursday (day 4)
def opt_d_constraint():
    all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]
    thursday_count = Sum([If(batch == 4, 1, 0) for batch in all_batches])
    return thursday_count >= 2

# Option E: Fewer batches of cookies are made on Monday than on Tuesday
def opt_e_constraint():
    all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]
    monday_count = Sum([If(batch == 1, 1, 0) for batch in all_batches])
    tuesday_count = Sum([If(batch == 2, 1, 0) for batch in all_batches])
    return monday_count < tuesday_count

# Now check which options must be true
found_options = []

# Check Option A
solver = Solver()
add_base_constraints(solver)
solver.add(Not(opt_a_constraint()))
result_a = solver.check()
if result_a == unsat:
    found_options.append("A")

# Check Option B
solver = Solver()
add_base_constraints(solver)
solver.add(Not(opt_b_constraint()))
result_b = solver.check()
if result_b == unsat:
    found_options.append("B")

# Check Option C
solver = Solver()
add_base_constraints(solver)
solver.add(Not(opt_c_constraint()))
result_c = solver.check()
if result_c == unsat:
    found_options.append("C")

# Check Option D
solver = Solver()
add_base_constraints(solver)
solver.add(Not(opt_d_constraint()))
result_d = solver.check()
if result_d == unsat:
    found_options.append("D")

# Check Option E
solver = Solver()
add_base_constraints(solver)
solver.add(Not(opt_e_constraint()))
result_e = solver.check()
if result_e == unsat:
    found_options.append("E")

print(f"Options that must be true: {found_options}")
print(f"Result A: {result_a}")
print(f"Result B: {result_b}")
print(f"Result C: {result_c}")
print(f"Result D: {result_d}")
print(f"Result E: {result_e}")

# Print the final answer using the required format
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")