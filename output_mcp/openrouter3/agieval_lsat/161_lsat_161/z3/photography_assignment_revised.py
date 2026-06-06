from z3 import *

# Photographers: 0=not assigned, 1=Silva, 2=Thorne
F, G, H, K, L, M = Ints('F G H K L M')

# Define base constraints (without the original constraint)
def add_base_constraints(solver):
    # Domain constraints: each photographer can be 0, 1, or 2
    for var in [F, G, H, K, L, M]:
        solver.add(Or(var == 0, var == 1, var == 2))
    
    # Constraint 1: At least 2 photographers assigned to each ceremony
    silva_count = Sum([If(var == 1, 1, 0) for var in [F, G, H, K, L, M]])
    thorne_count = Sum([If(var == 2, 1, 0) for var in [F, G, H, K, L, M]])
    solver.add(silva_count >= 2)
    solver.add(thorne_count >= 2)
    
    # Constraint 3: Frost must be assigned together with Heideck to one ceremony
    solver.add(Or(
        And(F == 1, H == 1),  # Both to Silva
        And(F == 2, H == 2),  # Both to Thorne
        And(F == 0, H == 0)   # Both not assigned
    ))
    
    # Constraint 4: If Lai and Mays are both assigned, they must be to different ceremonies
    solver.add(Implies(
        And(L != 0, M != 0),
        L != M
    ))
    
    # Constraint 5: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
    solver.add(Implies(
        G == 1,
        L == 2
    ))

# Original constraint: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
original_constraint = Implies(
    K != 2,
    And(H == 2, M == 2)
)

# Define the options
opt_a = Implies(
    K == 1,  # Knutson assigned to Silva
    Not(And(H == 1, M == 1))  # Heideck and Mays cannot both be assigned to Silva
)

opt_b = Implies(
    K == 1,  # Knutson assigned to Silva
    L == 1   # Lai must also be assigned to Silva
)

opt_c = Implies(
    K != 2,  # Unless Knutson is assigned to Thorne (i.e., Knutson not assigned to Thorne)
    And(F == 2, M == 2)  # Both Frost and Mays must be assigned to Thorne
)

opt_d = Implies(
    K != 2,  # Unless Knutson is assigned to Thorne
    # Heideck cannot be assigned to the same ceremony as Lai
    # This means: if both are assigned, they must be different
    Or(H == 0, L == 0, H != L)
)

opt_e = Implies(
    And(H != 2, M != 2),  # Unless either Heideck or Mays is assigned to Thorne
    K == 2  # Knutson must be assigned to Thorne
)

# Test each option for equivalence with original constraint
found_options = []

for letter, option in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    # Check if (base+original) ⇒ (base+option) is valid
    # i.e., base+original ∧ ¬option is unsat
    s1 = Solver()
    add_base_constraints(s1)
    s1.add(original_constraint)
    s1.add(Not(option))
    res1 = s1.check()
    
    # Check if (base+option) ⇒ (base+original) is valid
    # i.e., base+option ∧ ¬original is unsat
    s2 = Solver()
    add_base_constraints(s2)
    s2.add(option)
    s2.add(Not(original_constraint))
    res2 = s2.check()
    
    # If both are unsat, then the option is equivalent to the original
    if res1 == unsat and res2 == unsat:
        found_options.append(letter)
        print(f"Option {letter} is equivalent to original constraint")

print(f"\nOptions equivalent to original constraint: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")