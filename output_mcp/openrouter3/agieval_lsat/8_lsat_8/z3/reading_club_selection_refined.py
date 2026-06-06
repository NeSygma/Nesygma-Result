from z3 import *

# Variables for counts:
FN = Int('FN')  # French novels (0-3)
RN = Int('RN')  # Russian novels (0-3)
FP = Int('FP')  # French plays (0-2)
RP = Int('RP')  # Russian play (0-1)

solver = Solver()

# Domain constraints
solver.add(FN >= 0, FN <= 3)
solver.add(RN >= 0, RN <= 3)
solver.add(FP >= 0, FP <= 2)
solver.add(RP >= 0, RP <= 1)

# Total selection constraint: 5-6 works
total = FN + RN + FP + RP
solver.add(total >= 5, total <= 6)

# Constraint 1: No more than 4 French works (French novels + French plays)
solver.add(FN + FP <= 4)

# Constraint 2: At least 3 but no more than 4 novels selected
novels = FN + RN
solver.add(novels >= 3, novels <= 4)

# Constraint 3: At least as many French novels as Russian novels
solver.add(FN >= RN)

# Constraint 4: If both French plays are selected, then Russian play is not selected
solver.add(Implies(FP == 2, RP == 0))

# Let's first check what models satisfy all constraints
print("Checking base constraints...")
if solver.check() == sat:
    m = solver.model()
    print(f"Base model: FN={m[FN]}, RN={m[RN]}, FP={m[FP]}, RP={m[RP]}, Total={m[FN]+m[RN]+m[FP]+m[RP]}")
else:
    print("No base model found - constraints might be inconsistent")

# Now evaluate each option with detailed checking
found_options = []

# Option A: No Russian novels are selected
print("\nTesting Option A: No Russian novels selected")
solver.push()
solver.add(RN == 0)
result_a = solver.check()
if result_a == sat:
    m = solver.model()
    print(f"  Model: FN={m[FN]}, RN={m[RN]}, FP={m[FP]}, RP={m[RP]}, Total={m[FN]+m[RN]+m[FP]+m[RP]}")
    found_options.append("A")
else:
    print("  UNSAT")
solver.pop()

# Option B: Exactly one French novel is selected
print("\nTesting Option B: Exactly one French novel selected")
solver.push()
solver.add(FN == 1)
result_b = solver.check()
if result_b == sat:
    m = solver.model()
    print(f"  Model: FN={m[FN]}, RN={m[RN]}, FP={m[FP]}, RP={m[RP]}, Total={m[FN]+m[RN]+m[FP]+m[RP]}")
    found_options.append("B")
else:
    print("  UNSAT")
solver.pop()

# Option C: All three plays are selected
print("\nTesting Option C: All three plays selected")
solver.push()
solver.add(FP == 2)
solver.add(RP == 1)
result_c = solver.check()
if result_c == sat:
    m = solver.model()
    print(f"  Model: FN={m[FN]}, RN={m[RN]}, FP={m[FP]}, RP={m[RP]}, Total={m[FN]+m[RN]+m[FP]+m[RP]}")
    found_options.append("C")
else:
    print("  UNSAT")
solver.pop()

# Option D: All three Russian novels are selected
print("\nTesting Option D: All three Russian novels selected")
solver.push()
solver.add(RN == 3)
result_d = solver.check()
if result_d == sat:
    m = solver.model()
    print(f"  Model: FN={m[FN]}, RN={m[RN]}, FP={m[FP]}, RP={m[RP]}, Total={m[FN]+m[RN]+m[FP]+m[RP]}")
    found_options.append("D")
else:
    print("  UNSAT")
solver.pop()

# Option E: All five French works are selected
print("\nTesting Option E: All five French works selected")
solver.push()
solver.add(FN + FP == 5)
result_e = solver.check()
if result_e == sat:
    m = solver.model()
    print(f"  Model: FN={m[FN]}, RN={m[RN]}, FP={m[FP]}, RP={m[RP]}, Total={m[FN]+m[RN]+m[FP]+m[RP]}")
    found_options.append("E")
else:
    print("  UNSAT")
solver.pop()

# Output results
print(f"\nFound options: {found_options}")
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")