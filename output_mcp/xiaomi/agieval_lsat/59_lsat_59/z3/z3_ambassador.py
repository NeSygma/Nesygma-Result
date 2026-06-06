from z3 import *

# Countries: 0=Venezuela, 1=Yemen, 2=Zambia
# Candidates: 0=Jaramillo, 1=Kayne, 2=Landon, 3=Novetzke, 4=Ong
# assigned[c] = candidate assigned to country c, or -1 if unassigned
# But since exactly 3 ambassadors are assigned to 3 countries, we use:
# assigned[c] in {0,1,2,3,4} for each country c

solver = Solver()

# Variables: which candidate is assigned to each country
venezuela = Int('venezuela')
yemen = Int('yemen')
zambia = Int('zambia')

# Each country gets exactly one ambassador from {0,1,2,3,4}
solver.add(venezuela >= 0, venezuela <= 4)
solver.add(yemen >= 0, yemen <= 4)
solver.add(zambia >= 0, zambia <= 4)

# No ambassador assigned to more than one country
solver.add(Distinct(venezuela, yemen, zambia))

# Helper: candidate c is assigned to some country
def is_assigned(c):
    return Or(venezuela == c, yemen == c, zambia == c)

# Constraint 1: Exactly one of Kayne(1) or Novetzke(3) is assigned
solver.add(Xor(is_assigned(1), is_assigned(3)))

# Constraint 2 (original): If Jaramillo(0) is assigned, then Kayne(1) is assigned
# This is the constraint we will REPLACE with each option
# We'll test each option by removing this constraint and adding the option instead

# Constraint 3: If Ong(4) is assigned to Venezuela, then Kayne(1) is NOT assigned to Yemen
solver.add(Implies(venezuela == 4, yemen != 1))

# Constraint 4: If Landon(2) is assigned, it is to Zambia
solver.add(Implies(is_assigned(2), zambia == 2))

# Now we need to find which option, when substituted for Constraint 2,
# yields the SAME set of valid assignments as the original.

# First, find all valid assignments with the ORIGINAL constraint 2
original_solver = Solver()
original_solver.add(venezuela >= 0, venezuela <= 4)
original_solver.add(yemen >= 0, yemen <= 4)
original_solver.add(zambia >= 0, zambia <= 4)
original_solver.add(Distinct(venezuela, yemen, zambia))
original_solver.add(Xor(is_assigned(1), is_assigned(3)))
original_solver.add(Implies(is_assigned(0), is_assigned(1)))  # Original constraint 2
original_solver.add(Implies(venezuela == 4, yemen != 1))
original_solver.add(Implies(is_assigned(2), zambia == 2))

# Enumerate all solutions with original constraints
original_solutions = []
decision_vars = [venezuela, yemen, zambia]
while original_solver.check() == sat:
    m = original_solver.model()
    sol = tuple(m.eval(v).as_long() for v in decision_vars)
    original_solutions.append(sol)
    original_solver.add(Or([v != m.eval(v) for v in decision_vars]))

print(f"Original solutions count: {len(original_solutions)}")
for s in original_solutions:
    print(f"  V={s[0]}, Y={s[1]}, Z={s[2]}")

# Define the option constraints (replacing constraint 2)
# Option A: If Kayne is assigned, then Jaramillo is assigned
opt_a = Implies(is_assigned(1), is_assigned(0))
# Option B: If Landon and Ong are both assigned, then Novetzke is assigned
opt_b = Implies(And(is_assigned(2), is_assigned(4)), is_assigned(3))
# Option C: If Ong is not assigned, then Kayne is assigned
opt_c = Implies(Not(is_assigned(4)), is_assigned(1))
# Option D: Jaramillo and Novetzke are not both assigned
opt_d = Not(And(is_assigned(0), is_assigned(3)))
# Option E: Novetzke and Ong are not both assigned
opt_e = Not(And(is_assigned(3), is_assigned(4)))

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

# For each option, enumerate solutions and compare to original
found_options = []
for letter, opt_constr in options:
    test_solver = Solver()
    test_solver.add(venezuela >= 0, venezuela <= 4)
    test_solver.add(yemen >= 0, yemen <= 4)
    test_solver.add(zambia >= 0, zambia <= 4)
    test_solver.add(Distinct(venezuela, yemen, zambia))
    test_solver.add(Xor(is_assigned(1), is_assigned(3)))
    test_solver.add(opt_constr)  # Substitute constraint
    test_solver.add(Implies(venezuela == 4, yemen != 1))
    test_solver.add(Implies(is_assigned(2), zambia == 2))
    
    test_solutions = []
    while test_solver.check() == sat:
        m = test_solver.model()
        sol = tuple(m.eval(v).as_long() for v in decision_vars)
        test_solutions.append(sol)
        test_solver.add(Or([v != m.eval(v) for v in decision_vars]))
    
    print(f"\nOption {letter}: solutions count = {len(test_solutions)}")
    for s in test_solutions:
        print(f"  V={s[0]}, Y={s[1]}, Z={s[2]}")
    
    # Check if solution sets are identical
    if set(test_solutions) == set(original_solutions):
        found_options.append(letter)
        print(f"  -> MATCHES original!")
    else:
        print(f"  -> Does NOT match original")

if len(found_options) == 1:
    print("\nSTATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print(f"\nSTATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print(f"\nSTATUS: unsat")
    print("Refine: No options found")