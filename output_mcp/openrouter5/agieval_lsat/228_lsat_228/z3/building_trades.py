from z3 import *

# Three companies: 0=RealProp, 1=Southco, 2=Trustcorp
# Buildings with classes:
# RP: Garza Tower (c1), Yates House (c3), Zimmer House (c3)
# SC: Flores Tower (c1), Lynch Building (c2)
# TC: King Building (c2), Meyer Building (c2), Ortiz Building (c2)

# Total: c1=2, c2=4, c3=2

# Trade types:
# A: 1-for-1 same class (no net effect on counts)
# B: give 1 c1, receive 2 c2
# C: give 1 c2, receive 2 c3

solver = Solver()

# Trade count variables (non-negative integers)
# b_ij = number of type B trades where company i gives c1 to j, receives 2 c2 from j
b_01, b_02 = Int('b_01'), Int('b_02')
b_10, b_12 = Int('b_10'), Int('b_12')
b_20, b_21 = Int('b_20'), Int('b_21')

# c_ij = number of type C trades where company i gives c2 to j, receives 2 c3 from j
c_01, c_02 = Int('c_01'), Int('c_02')
c_10, c_12 = Int('c_10'), Int('c_12')
c_20, c_21 = Int('c_20'), Int('c_21')

for v in [b_01, b_02, b_10, b_12, b_20, b_21, c_01, c_02, c_10, c_12, c_20, c_21]:
    solver.add(v >= 0)

# Initial counts: (c1, c2, c3)
init = [(1, 0, 2), (1, 1, 0), (0, 3, 0)]

# Final counts
final_c1 = [Int(f'fc1_{i}') for i in range(3)]
final_c2 = [Int(f'fc2_{i}') for i in range(3)]
final_c3 = [Int(f'fc3_{i}') for i in range(3)]

for i in range(3):
    solver.add(final_c1[i] >= 0)
    solver.add(final_c2[i] >= 0)
    solver.add(final_c3[i] >= 0)

# Total conservation
solver.add(final_c1[0] + final_c1[1] + final_c1[2] == 2)
solver.add(final_c2[0] + final_c2[1] + final_c2[2] == 4)
solver.add(final_c3[0] + final_c3[1] + final_c3[2] == 2)

# RealProp owns only class 2
solver.add(final_c1[0] == 0)
solver.add(final_c3[0] == 0)

# Change equations for each company
# RP (k=0)
solver.add(final_c1[0] - init[0][0] == (b_10 + b_20) - (b_01 + b_02))
solver.add(final_c2[0] - init[0][1] == 2*((b_01 + b_02) - (b_10 + b_20)) + (c_10 + c_20) - (c_01 + c_02))
solver.add(final_c3[0] - init[0][2] == 2*((c_01 + c_02) - (c_10 + c_20)))

# SC (k=1)
solver.add(final_c1[1] - init[1][0] == (b_01 + b_21) - (b_10 + b_12))
solver.add(final_c2[1] - init[1][1] == 2*((b_10 + b_12) - (b_01 + b_21)) + (c_01 + c_21) - (c_10 + c_12))
solver.add(final_c3[1] - init[1][2] == 2*((c_10 + c_12) - (c_01 + c_21)))

# TC (k=2)
solver.add(final_c1[2] - init[2][0] == (b_02 + b_12) - (b_20 + b_21))
solver.add(final_c2[2] - init[2][1] == 2*((b_20 + b_21) - (b_02 + b_12)) + (c_02 + c_12) - (c_20 + c_21))
solver.add(final_c3[2] - init[2][2] == 2*((c_20 + c_21) - (c_02 + c_12)))

# Also need to ensure that a company can't give more of a class than it has available.
# This is a feasibility constraint on the trades themselves.
# For type B trades: company i gives c1 buildings. The total c1 it gives (sum of b_ij for j!=i)
# must be <= its initial c1 + c1 it receives from type B trades.
# Similarly for type C: company i gives c2 buildings. Total c2 it gives (sum of c_ij for j!=i)
# must be <= its initial c2 + c2 it receives.

# Actually, the net effect equations already capture the final state.
# But we need to ensure there exists some ordering of trades that respects
# intermediate availability. This is a more complex constraint.

# Let's add constraints that the total outflow of a class from a company
# doesn't exceed what it could have (initial + inflow).

# For RP: c1 outflow = b_01 + b_02, c1 inflow = b_10 + b_20
# RP starts with 1 c1. So b_01 + b_02 <= 1 + (b_10 + b_20)
solver.add(b_01 + b_02 <= 1 + b_10 + b_20)

# RP c2 outflow = c_01 + c_02, c2 inflow = 2*(b_01 + b_02) + (c_10 + c_20)
# RP starts with 0 c2.
solver.add(c_01 + c_02 <= 0 + 2*(b_01 + b_02) + (c_10 + c_20))

# RP c3 outflow = 0 (RP can't give c3 in any trade type), c3 inflow = 2*(c_01 + c_02)
# RP starts with 2 c3.
# RP can give c3 in type A trades (1-for-1 same class), but type A doesn't affect counts.
# Since type A doesn't change counts, we don't model it explicitly.
# But RP could give away c3 buildings in type A trades. However, the constraint is
# that RP ends with 0 c3. So RP must give away all its c3.
# In type C trades, RP receives c3. So RP's c3 can increase before being traded away.
# Actually, type A trades don't change counts, so they don't affect our equations.
# But they could be used to move buildings around without changing counts.

# Let's simplify: since type A trades don't change counts, they just permute ownership
# within the same class. So the count-based model is sufficient for determining
# what final count distributions are possible.

# However, we need to ensure that the specific buildings can be matched.
# For example, if RP ends with 0 c1, RP must have given away Garza Tower (its only c1).
# RP can give Garza Tower in a type B trade (getting 2 c2 in return) or in a type A trade
# (getting another c1 in return, which it would then need to give away again).

# Let's just check if the model is satisfiable first.

print("Checking model...")
result = solver.check()
print(f"Result: {result}")

if result == sat:
    m = solver.model()
    print("Final counts:")
    for i, name in enumerate(["RP", "SC", "TC"]):
        print(f"  {name}: c1={m[final_c1[i]]}, c2={m[final_c2[i]]}, c3={m[final_c3[i]]}")
    print()
    print("Trade counts:")
    for v in [b_01, b_02, b_10, b_12, b_20, b_21, c_01, c_02, c_10, c_12, c_20, c_21]:
        print(f"  {v}: {m[v]}")
    
    # Now let's enumerate all possible final states to find what MUST be true
    print("\n--- Enumerating all solutions ---")
    
    # Decision variables for enumeration
    decision_vars = final_c1 + final_c2 + final_c3
    
    solutions = []
    while solver.check() == sat:
        m = solver.model()
        sol = tuple(m.eval(v, model_completion=True).as_long() for v in decision_vars)
        solutions.append(sol)
        # Block this solution
        solver.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))
    
    print(f"Total distinct final states: {len(solutions)}")
    for sol in solutions:
        print(f"  RP(c1={sol[0]},c2={sol[1]},c3={sol[2]}) SC(c1={sol[3]},c2={sol[4]},c3={sol[5]}) TC(c1={sol[6]},c2={sol[7]},c3={sol[8]})")
    
    # Now check each option
    # We need to check what MUST be true in ALL solutions
    # Option A: Trustcorp owns a class 1 building -> TC_c1 > 0
    # Option B: Trustcorp owns the Meyer Building -> need specific building tracking
    # Option C: Southco owns a class 2 building -> SC_c2 > 0
    # Option D: Southco owns both of the class 3 buildings -> SC_c3 == 2
    # Option E: Southco owns the Flores Tower -> need specific building tracking
    
    # For options involving specific buildings (B, E), we need a more detailed model.
    # Let's first check what we can determine from counts alone.
    
    print("\nAnalyzing options from count data:")
    for sol in solutions:
        rp_c1, rp_c2, rp_c3 = sol[0], sol[1], sol[2]
        sc_c1, sc_c2, sc_c3 = sol[3], sol[4], sol[5]
        tc_c1, tc_c2, tc_c3 = sol[6], sol[7], sol[8]
        
        a_val = (tc_c1 > 0)
        c_val = (sc_c2 > 0)
        d_val = (sc_c3 == 2)
        
        print(f"  A(TC has c1)={a_val}, C(SC has c2)={c_val}, D(SC has both c3)={d_val}")
    
else:
    print("UNSAT - need to refine model")