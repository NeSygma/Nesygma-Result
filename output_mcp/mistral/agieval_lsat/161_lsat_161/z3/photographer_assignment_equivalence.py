from z3 import *

# Declare boolean variables for each photographer's assignment to each ceremony
frost_S = Bool('frost_S')
frost_T = Bool('frost_T')
gonzalez_S = Bool('gonzalez_S')
gonzalez_T = Bool('gonzalez_T')
heideck_S = Bool('heideck_S')
heideck_T = Bool('heideck_T')
knutson_S = Bool('knutson_S')
knutson_T = Bool('knutson_T')
lai_S = Bool('lai_S')
lai_T = Bool('lai_T')
mays_S = Bool('mays_S')
mays_T = Bool('mays_T')

# Base constraints (all constraints except the original constraint)
base_constraints = [
    # No photographer is assigned to both ceremonies
    Not(And(frost_S, frost_T)),
    Not(And(gonzalez_S, gonzalez_T)),
    Not(And(heideck_S, heideck_T)),
    Not(And(knutson_S, knutson_T)),
    Not(And(lai_S, lai_T)),
    Not(And(mays_S, mays_T)),
    
    # Each ceremony must have at least two photographers
    Sum([frost_S, gonzalez_S, heideck_S, knutson_S, lai_S, mays_S]) >= 2,
    Sum([frost_T, gonzalez_T, heideck_T, knutson_T, lai_T, mays_T]) >= 2,
    
    # Frost must be assigned together with Heideck to one of the ceremonies
    Or(And(frost_S, heideck_S), And(frost_T, heideck_T)),
    
    # If Lai and Mays are both assigned, they must be at different ceremonies
    Not(And(lai_S, mays_S)),
    Not(And(lai_T, mays_T)),
    
    # If Gonzalez is assigned to Silva University, then Lai must be assigned to Thorne University
    Implies(gonzalez_S, lai_T),
]

# Original constraint: If Knutson is not assigned to Thorne University, then both Heideck and Mays must be assigned to Thorne University
original_constraint = Implies(Not(knutson_T), And(heideck_T, mays_T))

# Define the answer choices as constraints replacing the original constraint
# (A) If Knutson is assigned to Silva, then Heideck and Mays cannot both be assigned to Silva.
opt_A = Implies(knutson_S, Not(And(heideck_S, mays_S)))

# (B) If Knutson is assigned to Silva, then Lai must also be assigned to Silva.
opt_B = Implies(knutson_S, lai_S)

# (C) Unless Knutson is assigned to Thorne, both Frost and Mays must be assigned to Thorne.
# This is equivalent to: If Knutson is not assigned to Thorne, then both Frost and Mays must be assigned to Thorne.
opt_C = Implies(Not(knutson_T), And(frost_T, mays_T))

# (D) Unless Knutson is assigned to Thorne, Heideck cannot be assigned to the same ceremony as Lai.
# This is equivalent to: If Knutson is not assigned to Thorne, then Heideck and Lai cannot be in the same ceremony.
opt_D = Implies(Not(knutson_T), Not(Or(And(heideck_S, lai_S), And(heideck_T, lai_T))))

# (E) Unless either Heideck or Mays is assigned to Thorne, Knutson must be assigned to Thorne.
# This is equivalent to: If neither Heideck nor Mays is assigned to Thorne, then Knutson must be assigned to Thorne.
opt_E = Implies(And(Not(heideck_T), Not(mays_T)), knutson_T)

# Function to check equivalence: (base + option) => original and (base + original) => option
def is_equivalent(option):
    # Check if (base + option) => original
    s1 = Solver()
    s1.add(base_constraints)
    s1.add(option)
    s1.add(Not(original_constraint))
    implies_original = (s1.check() == unsat)
    
    # Check if (base + original) => option
    s2 = Solver()
    s2.add(base_constraints)
    s2.add(original_constraint)
    s2.add(Not(option))
    implies_option = (s2.check() == unsat)
    
    return implies_original and implies_option

# Evaluate each option for equivalence
found_options = []

if is_equivalent(opt_A):
    found_options.append("A")

if is_equivalent(opt_B):
    found_options.append("B")

if is_equivalent(opt_C):
    found_options.append("C")

if is_equivalent(opt_D):
    found_options.append("D")

if is_equivalent(opt_E):
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