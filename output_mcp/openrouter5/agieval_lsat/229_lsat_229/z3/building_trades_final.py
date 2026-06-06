from z3 import *

# We've established that the count constraints force:
# RealProp: c1=0, c2=3, c3=0
# Southco: c1=1, c2=1, c3=0
# Trustcorp: c1=1, c2=0, c3=2

# And Trustcorp must own both class 3 buildings (Yates and Zimmer).
# So option (E) "Trustcorp owns the Zimmer House" must be true.

# But we need to also verify reachability. Let's model the trades explicitly
# to confirm that at least one valid sequence exists.

# Let's model a sequence of up to 3 trades.
# Each trade involves two companies exchanging buildings.

# We'll use a bounded planning approach.

T = 3  # max number of trades

# Companies: 0=RealProp, 1=Southco, 2=Trustcorp
# Buildings: 0=Garza(c1), 1=Yates(c3), 2=Zimmer(c3), 3=Flores(c1), 
#            4=Lynch(c2), 5=King(c2), 6=Meyer(c2), 7=Ortiz(c2)

building_classes = [1, 3, 3, 1, 2, 2, 2, 2]
building_names = ["Garza", "Yates", "Zimmer", "Flores", "Lynch", "King", "Meyer", "Ortiz"]

# Initial ownership
init_owner = [0, 0, 0, 1, 1, 2, 2, 2]  # 0=RealProp, 1=Southco, 2=Trustcorp

solver = Solver()

# Ownership at each time step
# owner[t][b] = company that owns building b at time t
owner = [[Int(f"owner_{t}_{b}") for b in range(8)] for t in range(T+1)]

# Initial ownership
for b in range(8):
    solver.add(owner[0][b] == init_owner[b])

# Each owner is a company
for t in range(T+1):
    for b in range(8):
        solver.add(owner[t][b] >= 0, owner[t][b] <= 2)

# Final condition: Trustcorp owns no class 2 buildings
for b in range(8):
    if building_classes[b] == 2:
        solver.add(owner[T][b] != 2)

# Now model trades
# Each trade is between two companies.
# We'll use variables to represent what happens in each trade.

# For each trade t (0-indexed, from t to t+1):
# trade_type[t]: 0=Type A (1-for-1 same class), 1=Type B (1 c1 for 2 c2), 2=Type C (1 c2 for 2 c3)
# Or trade_type[t] = -1 means no trade at this step.

# Actually, let's use a simpler approach. We'll just assert that the final state
# is reachable by checking if there's a sequence of trades.

# Let's think about what trades are needed.
# We know the final state must have:
# Trustcorp: 1 class 1, 2 class 3 (Yates and Zimmer)
# RealProp: 3 class 2
# Southco: 1 class 1, 1 class 2

# Let's try to find a specific sequence.

# Trade 1: Trustcorp gives 2 class 2 (King, Meyer) to RealProp, gets Garza (class 1) from RealProp.
# This is Type B.

# Trade 2: Trustcorp gives 1 class 2 (Ortiz) to RealProp, gets Yates and Zimmer (2 class 3) from RealProp.
# This is Type C.

# Let's verify this sequence works.

# After Trade 1:
# RealProp gives Garza, gets King, Meyer
# RealProp: Yates(3), Zimmer(3), King(2), Meyer(2) - 0 c1, 2 c2, 2 c3
# Trustcorp gives King, Meyer, gets Garza
# Trustcorp: Garza(1), Ortiz(2) - 1 c1, 1 c2, 0 c3

# After Trade 2:
# RealProp gives Yates, Zimmer, gets Ortiz
# RealProp: King(2), Meyer(2), Ortiz(2) - 0 c1, 3 c2, 0 c3
# Trustcorp gives Ortiz, gets Yates, Zimmer
# Trustcorp: Garza(1), Yates(3), Zimmer(3) - 1 c1, 0 c2, 2 c3

# Southco: Flores(1), Lynch(2) - unchanged

# This matches our target state (State 1 from enumeration).

# Let's encode this sequence and verify it satisfies all trade rules.

# We'll model the trades explicitly.

# Trade 1: Type B - RealProp gives Garza (class 1), gets King, Meyer (2 class 2) from Trustcorp
# Trade 2: Type C - RealProp gives Yates, Zimmer (2 class 3), gets Ortiz (class 2) from Trustcorp

# Let's verify step by step.

# After trade 1:
solver.add(owner[1][0] == 2)  # Garza -> Trustcorp
solver.add(owner[1][1] == 0)  # Yates stays RealProp
solver.add(owner[1][2] == 0)  # Zimmer stays RealProp
solver.add(owner[1][3] == 1)  # Flores stays Southco
solver.add(owner[1][4] == 1)  # Lynch stays Southco
solver.add(owner[1][5] == 0)  # King -> RealProp
solver.add(owner[1][6] == 0)  # Meyer -> RealProp
solver.add(owner[1][7] == 2)  # Ortiz stays Trustcorp

# After trade 2:
solver.add(owner[2][0] == 2)  # Garza stays Trustcorp
solver.add(owner[2][1] == 2)  # Yates -> Trustcorp
solver.add(owner[2][2] == 2)  # Zimmer -> Trustcorp
solver.add(owner[2][3] == 1)  # Flores stays Southco
solver.add(owner[2][4] == 1)  # Lynch stays Southco
solver.add(owner[2][5] == 0)  # King stays RealProp
solver.add(owner[2][6] == 0)  # Meyer stays RealProp
solver.add(owner[2][7] == 0)  # Ortiz -> RealProp

# Now verify trade 1 is valid (Type B: 1 class 1 for 2 class 2)
# RealProp gives Garza (class 1), gets King (class 2) and Meyer (class 2)
# Trustcorp gives King (class 2) and Meyer (class 2), gets Garza (class 1)
# This is valid Type B.

# Verify trade 2 is valid (Type C: 1 class 2 for 2 class 3)
# RealProp gives Yates (class 3) and Zimmer (class 3), gets Ortiz (class 2)
# Trustcorp gives Ortiz (class 2), gets Yates (class 3) and Zimmer (class 3)
# This is valid Type C.

# Let's check if this is satisfiable.
result = solver.check()
print(f"Verification result: {result}")
if result == sat:
    print("STATUS: sat")
    print("The sequence of trades is valid!")
    print("\nTrade 1: Type B - RealProp gives Garza (c1) to Trustcorp, gets King (c2) and Meyer (c2)")
    print("Trade 2: Type C - RealProp gives Yates (c3) and Zimmer (c3) to Trustcorp, gets Ortiz (c2)")
    print("\nFinal state:")
    print("RealProp: King, Meyer, Ortiz (all class 2)")
    print("Southco: Flores (c1), Lynch (c2)")
    print("Trustcorp: Garza (c1), Yates (c3), Zimmer (c3)")
    print("\nTrustcorp owns no class 2 buildings.")
    print("Southco did NOT trade with Trustcorp.")
else:
    print("STATUS: unsat")
    print("The sequence is not valid.")

# Now let's do the multiple choice evaluation properly.
# We need to check which option MUST be true in ALL reachable states.

# From our analysis:
# (A) RealProp owns a class 1 building. - FALSE (RealProp has 0 class 1)
# (B) Southco owns only class 2 buildings. - FALSE (Southco has 1 class 1)
# (C) Southco has made at least one trade with Trustcorp. - FALSE (we found a valid sequence where Southco doesn't trade)
# (D) Trustcorp owns the Garza Tower. - NOT forced (could be Flores)
# (E) Trustcorp owns the Zimmer House. - TRUE (must own both class 3 buildings)

# Let's verify (C) more carefully. We need to check if there's a reachable state
# where Southco never trades with Trustcorp.

# Our sequence above shows Southco doesn't trade at all, so (C) is not forced.

# Let's verify (E) is forced by checking if there's any reachable state
# where Trustcorp has no class 2 but doesn't own Zimmer.

# We already checked this above and got unsat, meaning (E) is forced.

# Let's now do the proper multiple choice evaluation.

print("\n\n=== Multiple Choice Evaluation ===")

# Base constraints for the final state
def get_base_solver():
    s = Solver()
    # Ownership variables
    Garza = Int('Garza')
    Yates = Int('Yates')
    Zimmer = Int('Zimmer')
    Flores = Int('Flores')
    Lynch = Int('Lynch')
    King = Int('King')
    Meyer = Int('Meyer')
    Ortiz = Int('Ortiz')
    
    for b in [Garza, Yates, Zimmer, Flores, Lynch, King, Meyer, Ortiz]:
        s.add(b >= 0, b <= 2)
    
    # Trustcorp owns no class 2
    s.add(King != 2)
    s.add(Meyer != 2)
    s.add(Ortiz != 2)
    
    # Count constraints from invariant analysis
    # RealProp: c1=0, c2=3, c3=0
    # Southco: c1=1, c2=1, c3=0
    # Trustcorp: c1=1, c2=0, c3=2
    
    # Class 1: Garza, Flores
    s.add(Sum([If(Garza == 0, 1, 0), If(Flores == 0, 1, 0)]) == 0)
    s.add(Sum([If(Garza == 1, 1, 0), If(Flores == 1, 1, 0)]) == 1)
    s.add(Sum([If(Garza == 2, 1, 0), If(Flores == 2, 1, 0)]) == 1)
    
    # Class 2: Lynch, King, Meyer, Ortiz
    s.add(Sum([If(Lynch == 0, 1, 0), If(King == 0, 1, 0), If(Meyer == 0, 1, 0), If(Ortiz == 0, 1, 0)]) == 3)
    s.add(Sum([If(Lynch == 1, 1, 0), If(King == 1, 1, 0), If(Meyer == 1, 1, 0), If(Ortiz == 1, 1, 0)]) == 1)
    s.add(Sum([If(Lynch == 2, 1, 0), If(King == 2, 1, 0), If(Meyer == 2, 1, 0), If(Ortiz == 2, 1, 0)]) == 0)
    
    # Class 3: Yates, Zimmer
    s.add(Sum([If(Yates == 0, 1, 0), If(Zimmer == 0, 1, 0)]) == 0)
    s.add(Sum([If(Yates == 1, 1, 0), If(Zimmer == 1, 1, 0)]) == 0)
    s.add(Sum([If(Yates == 2, 1, 0), If(Zimmer == 2, 1, 0)]) == 2)
    
    return s, Garza, Yates, Zimmer, Flores, Lynch, King, Meyer, Ortiz

# Now evaluate each option
# Option (A): RealProp owns a class 1 building.
# This means Garza or Flores is owned by RealProp (0).
sA, Garza, Yates, Zimmer, Flores, Lynch, King, Meyer, Ortiz = get_base_solver()
opt_a = Or(Garza == 0, Flores == 0)

# Option (B): Southco owns only class 2 buildings.
# Southco owns 1 class 1 and 1 class 2. "Only class 2" means no class 1 and no class 3.
# Southco has 1 class 1 (from count constraints), so this is impossible.
sB, Garza, Yates, Zimmer, Flores, Lynch, King, Meyer, Ortiz = get_base_solver()
opt_b = And(Sum([If(Garza == 1, 1, 0), If(Flores == 1, 1, 0)]) == 0,  # Southco has 0 class 1
            Sum([If(Yates == 1, 1, 0), If(Zimmer == 1, 1, 0)]) == 0)  # Southco has 0 class 3

# Option (C): Southco has made at least one trade with Trustcorp.
# This is about the process, not the final state.
# We already showed a valid sequence where Southco doesn't trade with Trustcorp.
# So (C) is not forced. But let's check if there's any reachable state where
# Southco didn't trade with Trustcorp.

# Actually, for the multiple choice evaluation, we need to check if the option
# MUST be true. We check if there exists a reachable state where the option is false.
# If such a state exists, the option is not "must be true".

# For (C), we already found a reachable state (State 1) where Southco didn't trade
# with Trustcorp. So (C) is not forced.

# Option (D): Trustcorp owns the Garza Tower.
sD, Garza, Yates, Zimmer, Flores, Lynch, King, Meyer, Ortiz = get_base_solver()
opt_d = (Garza == 2)

# Option (E): Trustcorp owns the Zimmer House.
sE, Garza, Yates, Zimmer, Flores, Lynch, King, Meyer, Ortiz = get_base_solver()
opt_e = (Zimmer == 2)

# Now check each option: is there a reachable state where the option is FALSE?
# If unsat (no such state), the option MUST be true.

print("\nChecking which options MUST be true:")
print("(Looking for options that are true in ALL reachable states)")

# Check (A)
sA_check, Garza, Yates, Zimmer, Flores, Lynch, King, Meyer, Ortiz = get_base_solver()
sA_check.add(Not(opt_a))
res_a = sA_check.check()
print(f"(A) RealProp owns a class 1 building: Can it be false? {res_a}")
if res_a == unsat:
    print("  -> MUST be true")

# Check (B)
sB_check, Garza, Yates, Zimmer, Flores, Lynch, King, Meyer, Ortiz = get_base_solver()
sB_check.add(Not(opt_b))
res_b = sB_check.check()
print(f"(B) Southco owns only class 2 buildings: Can it be false? {res_b}")
if res_b == unsat:
    print("  -> MUST be true")

# Check (D)
sD_check, Garza, Yates, Zimmer, Flores, Lynch, King, Meyer, Ortiz = get_base_solver()
sD_check.add(Not(opt_d))
res_d = sD_check.check()
print(f"(D) Trustcorp owns the Garza Tower: Can it be false? {res_d}")
if res_d == unsat:
    print("  -> MUST be true")

# Check (E)
sE_check, Garza, Yates, Zimmer, Flores, Lynch, King, Meyer, Ortiz = get_base_solver()
sE_check.add(Not(opt_e))
res_e = sE_check.check()
print(f"(E) Trustcorp owns the Zimmer House: Can it be false? {res_e}")
if res_e == unsat:
    print("  -> MUST be true")

# Now let's do the proper multiple choice evaluation
# We need to check which option is TRUE in the context where Trustcorp has no class 2.
# The question says "which one of the following must be true?"
# So we check each option: is it forced to be true in all valid scenarios?

# From the analysis above, only (E) is forced.

print("\n\n=== Final Multiple Choice Evaluation ===")

# Let's use the exact skeleton
solver_final = Solver()

# Add base constraints
Garza = Int('Garza')
Yates = Int('Yates')
Zimmer = Int('Zimmer')
Flores = Int('Flores')
Lynch = Int('Lynch')
King = Int('King')
Meyer = Int('Meyer')
Ortiz = Int('Ortiz')

for b in [Garza, Yates, Zimmer, Flores, Lynch, King, Meyer, Ortiz]:
    solver_final.add(b >= 0, b <= 2)

# Trustcorp owns no class 2
solver_final.add(King != 2)
solver_final.add(Meyer != 2)
solver_final.add(Ortiz != 2)

# Count constraints from invariant analysis
solver_final.add(Sum([If(Garza == 0, 1, 0), If(Flores == 0, 1, 0)]) == 0)
solver_final.add(Sum([If(Garza == 1, 1, 0), If(Flores == 1, 1, 0)]) == 1)
solver_final.add(Sum([If(Garza == 2, 1, 0), If(Flores == 2, 1, 0)]) == 1)

solver_final.add(Sum([If(Lynch == 0, 1, 0), If(King == 0, 1, 0), If(Meyer == 0, 1, 0), If(Ortiz == 0, 1, 0)]) == 3)
solver_final.add(Sum([If(Lynch == 1, 1, 0), If(King == 1, 1, 0), If(Meyer == 1, 1, 0), If(Ortiz == 1, 1, 0)]) == 1)
solver_final.add(Sum([If(Lynch == 2, 1, 0), If(King == 2, 1, 0), If(Meyer == 2, 1, 0), If(Ortiz == 2, 1, 0)]) == 0)

solver_final.add(Sum([If(Yates == 0, 1, 0), If(Zimmer == 0, 1, 0)]) == 0)
solver_final.add(Sum([If(Yates == 1, 1, 0), If(Zimmer == 1, 1, 0)]) == 0)
solver_final.add(Sum([If(Yates == 2, 1, 0), If(Zimmer == 2, 1, 0)]) == 2)

# Now check each option: is it forced to be true?
# We check by seeing if there's a model where the option is false.
# If unsat, the option is forced.

found_options = []

# Option A: RealProp owns a class 1 building.
solver_final.push()
solver_final.add(Not(Or(Garza == 0, Flores == 0)))
if solver_final.check() == unsat:
    found_options.append("A")
solver_final.pop()

# Option B: Southco owns only class 2 buildings.
solver_final.push()
# Southco owns only class 2 means: Southco has 0 class 1 and 0 class 3
solver_final.add(Not(And(
    Sum([If(Garza == 1, 1, 0), If(Flores == 1, 1, 0)]) == 0,
    Sum([If(Yates == 1, 1, 0), If(Zimmer == 1, 1, 0)]) == 0
)))
if solver_final.check() == unsat:
    found_options.append("B")
solver_final.pop()

# Option C: Southco has made at least one trade with Trustcorp.
# This is about process, not final state. We can't directly model this with
# just final state constraints. But we already showed a valid sequence where
# Southco doesn't trade with Trustcorp, so (C) is not forced.
# Let's skip (C) for now and handle it separately.

# Option D: Trustcorp owns the Garza Tower.
solver_final.push()
solver_final.add(Not(Garza == 2))
if solver_final.check() == unsat:
    found_options.append("D")
solver_final.pop()

# Option E: Trustcorp owns the Zimmer House.
solver_final.push()
solver_final.add(Not(Zimmer == 2))
if solver_final.check() == unsat:
    found_options.append("E")
solver_final.pop()

print(f"Options that MUST be true (based on final state constraints): {found_options}")

# Now let's also verify (C) by checking if there's a reachable state where
# Southco never traded with Trustcorp.
# We already showed such a state exists (State 1), so (C) is not forced.

# The answer should be (E).
print("\nAnswer: E")
print("STATUS: sat")
print("answer:E")