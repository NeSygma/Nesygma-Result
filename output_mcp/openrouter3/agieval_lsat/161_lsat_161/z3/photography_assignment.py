from z3 import *

# Photographers: 0=not assigned, 1=Silva, 2=Thorne
F, G, H, K, L, M = Ints('F G H K L M')

solver = Solver()

# Domain constraints: each photographer can be 0, 1, or 2
for var in [F, G, H, K, L, M]:
    solver.add(Or(var == 0, var == 1, var == 2))

# Constraint 1: At least 2 photographers assigned to each ceremony
# Count photographers assigned to Silva (value 1) and Thorne (value 2)
silva_count = Sum([If(var == 1, 1, 0) for var in [F, G, H, K, L, M]])
thorne_count = Sum([If(var == 2, 1, 0) for var in [F, G, H, K, L, M]])
solver.add(silva_count >= 2)
solver.add(thorne_count >= 2)

# Constraint 2: No photographer assigned to both ceremonies (handled by single assignment)

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
solver.add(original_constraint)

# Check if base problem is satisfiable
print("Checking base problem with original constraint...")
result = solver.check()
if result == sat:
    print("Base problem is satisfiable")
    m = solver.model()
    print("Example assignment:")
    print(f"Frost: {m[F]} (0=none, 1=Silva, 2=Thorne)")
    print(f"Gonzalez: {m[G]}")
    print(f"Heideck: {m[H]}")
    print(f"Knutson: {m[K]}")
    print(f"Lai: {m[L]}")
    print(f"Mays: {m[M]}")
    print(f"Silva count: {m.eval(silva_count)}")
    print(f"Thorne count: {m.eval(thorne_count)}")
else:
    print("Base problem is unsatisfiable")
    print("STATUS: unsat")
    exit()

# Now test each answer choice
# We need to replace the original constraint with each option and see which gives the same solution space

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
    Not(And(H == L, H != 0))  # Heideck cannot be assigned to the same ceremony as Lai
    # Note: "cannot be assigned to the same ceremony" means if both assigned, they must be different
    # So: If K != 2, then (H == 0 or L == 0 or H != L)
)

opt_e = Implies(
    And(H != 2, M != 2),  # Unless either Heideck or Mays is assigned to Thorne
    K == 2  # Knutson must be assigned to Thorne
)

# Test each option
found_options = []

# Test option A
solver.push()
solver.remove(original_constraint)
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Test option B
solver.push()
solver.remove(original_constraint)
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Test option C
solver.push()
solver.remove(original_constraint)
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Test option D
solver.push()
solver.remove(original_constraint)
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Test option E
solver.push()
solver.remove(original_constraint)
solver.add(opt_e)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

print(f"\nOptions that result in satisfiable problem: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")