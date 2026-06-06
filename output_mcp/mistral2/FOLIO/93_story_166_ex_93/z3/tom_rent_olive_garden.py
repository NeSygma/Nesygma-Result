from z3 import *

# Create a solver
solver = Solver()

# Predicates and variables
ManagedBuilding = Bool("ManagedBuilding")
AllowsPets = Bool("AllowsPets")
RequiresDeposit = Bool("RequiresDeposit")
MonthlyRent = Int("MonthlyRent")
SecurityDeposit = Int("SecurityDeposit")
CanMoveInWithPet = Bool("CanMoveInWithPet")
WillRent = Bool("WillRent")

# Premises
# 1. The Olive Garden is a managed building.
solver.add(ManagedBuilding == True)

# 2. A deposit is required to rent an apartment in a managed building.
solver.add(RequiresDeposit == True)

# 3. The security deposit can be either equal to the monthly rent at a managed building or more.
solver.add(SecurityDeposit >= MonthlyRent)

# 4. The monthly rent at the Olive Garden is $2000.
solver.add(MonthlyRent == 2000)

# 5. $2000 is more than $1500 (for clarity, though not directly used in constraints)
solver.add(IntVal(2000) > IntVal(1500))

# 6. If a managed building allows pets, then people are allowed to move in with a pet.
solver.add(Implies(AllowsPets, CanMoveInWithPet))

# 7. Tom will rent an apartment in a managed building if he is allowed to move in with Fluffy, and the security deposit is no more than $1500.
solver.add(WillRent == And(CanMoveInWithPet, SecurityDeposit <= 1500))

# Additional premises:
# - Fluffy is Tom's cat (modeled as Fluffy being a pet, but not directly used here)
# - Cats are pets (Fluffy is a pet)
# Since Fluffy is a pet, and if AllowsPets is true, then CanMoveInWithPet is true.

# Now, we want to check the conclusion: Tom will rent an apartment in The Olive Garden.
# This is WillRent.

# To determine if the conclusion is True, False, or Uncertain, we check:
# 1. If premises imply WillRent is True
# 2. If premises imply WillRent is False
# 3. Otherwise, it's Uncertain

# We will check both possibilities:
# A. premises + WillRent is satisfiable
# B. premises + not(WillRent) is satisfiable

# Check A: premises + WillRent
solver_A = Solver()
solver_A.add(solver.assertions())
solver_A.add(WillRent)
result_A = solver_A.check()

# Check B: premises + not(WillRent)
solver_B = Solver()
solver_B.add(solver.assertions())
solver_B.add(Not(WillRent))
result_B = solver_B.check()

# Interpret results
BENCHMARK_MODE = True

if result_A == unsat and result_B == sat:
    print("STATUS: proved")
    print("CONCLUSION: False")
elif result_A == sat and result_B == unsat:
    print("STATUS: proved")
    print("CONCLUSION: True")
elif result_A == sat and result_B == sat:
    print("STATUS: proved")
    print("CONCLUSION: Uncertain")
elif result_A == unsat and result_B == unsat:
    print("STATUS: unknown")
    print("CONCLUSION: Inconsistent premises")
else:
    print("STATUS: unknown")
    print("CONCLUSION: Inconclusive")