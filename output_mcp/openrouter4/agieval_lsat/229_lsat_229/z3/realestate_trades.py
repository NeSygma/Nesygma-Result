from z3 import *

solver = Solver()

# We model the final state of the problem.
# Initial state:
# RealProp: Garza (c1), Yates (c3), Zimmer (c3)  -> (1, 0, 2)
# Southco: Flores (c1), Lynch (c2)               -> (1, 1, 0)
# Trustcorp: King (c2), Meyer (c2), Ortiz (c2)   -> (0, 3, 0)

# Total counts are invariant across trades:
# Class 1: 2 buildings (Garza, Flores)
# Class 2: 4 buildings (Lynch, King, Meyer, Ortiz)
# Class 3: 2 buildings (Yates, Zimmer)

# After trades, we know Trustcorp has 0 class 2 buildings.
# Let the final state be:
# RealProp: (r1, r2, r3)
# Southco: (s1, s2, s3)
# Trustcorp: (t1, t2=0, t3)

# Total class counts are invariant
r1, r2, r3 = Ints('r1 r2 r3')
s1, s2, s3 = Ints('s1 s2 s3')
t1, t3 = Ints('t1 t3')

# Non-negative
for v in [r1, r2, r3, s1, s2, s3, t1, t3]:
    solver.add(v >= 0)

# Trustcorp has 0 class 2 (already enforced by not having t2)

# Conservation of class totals
solver.add(r1 + s1 + t1 == 2)  # total class 1
solver.add(r2 + s2 + 0 == 4)   # total class 2
solver.add(r3 + s3 + t3 == 2)  # total class 3

# Weight conservation: total weight = 18, each company has weight 6
# Weight: class 1 = 4, class 2 = 2, class 3 = 1
solver.add(4*r1 + 2*r2 + r3 == 6)  # RealProp weight
solver.add(4*s1 + 2*s2 + s3 == 6)  # Southco weight
solver.add(4*t1 + 2*0 + t3 == 6)   # Trustcorp weight

print("=== Checking final state constraints ===")
result = solver.check()
if result == sat:
    m = solver.model()
    print(f"RealProp: r1={m[r1]}, r2={m[r2]}, r3={m[r3]}")
    print(f"Southco: s1={m[s1]}, s2={m[s2]}, s3={m[s3]}")
    print(f"Trustcorp: t1={m[t1]}, t3={m[t3]}")
    print()
    
    # Trustcorp owns t1 class 1 buildings and t3 class 3 buildings.
    # Class 3 buildings are Yates House and Zimmer House (both owned by RealProp initially)
    # Class 1 buildings are Garza Tower (RealProp) and Flores Tower (Southco)
    
    # Option (A): RealProp owns a class 1 building → r1 > 0
    solver.push()
    solver.add(r1 == 0)  # Check if RealProp could own NO class 1
    resA = solver.check()
    solver.pop()
    
    # Option (B): Southco owns only class 2 buildings → s1 == 0 and s3 == 0
    solver.push()
    solver.add(Not(And(s1 == 0, s3 == 0)))  # Check if Southco could own non-class-2
    resB = solver.check()
    solver.pop()
    
    # Option (C): Southco has made at least one trade with Trustcorp.
    # We can't directly model this from final state alone.
    # But we can check if it's possible that Southco never traded with Trustcorp.
    # If Southco's initial buildings (Flores c1, Lynch c2) are still with Southco,
    # and Southco has no buildings from Trustcorp, then no trade happened.
    # Actually, Southco could have traded with RealProp only. Let me think...
    # We need to check if a scenario exists where Southco and Trustcorp didn't trade.
    # For this, we need to check reachability more carefully.
    print("Checking options with final state constraints...")
    
    # Option (D): Trustcorp owns the Garza Tower → Trustcorp must own Garza (c1)
    # Garza is one specific building. If Trustcorp has 1 class 1 building, it could be
    # Garza OR Flores. So we check if Trustcorp could own Garza specifically.
    # We need a more detailed model for this. Let me check if t1 >= 1 at minimum
    # From weight: 4*t1 + t3 = 6, so t1 can be 0 or 1.
    # If t1=0, t3=6: but total class 3 is only 2! So this is impossible.
    # Wait, let's solve: 4t1 + t3 = 6, t3 <= 2 (conservation of class 3)
    # If t1=0: t3=6 > 2. Impossible.
    # If t1=1: t3=2. Possible (t3=2 <= 2).
    # So t1 MUST be 1. Trustcorp MUST own exactly 1 class 1 building.
    # And t3 MUST be 2. Trustcorp MUST own both class 3 buildings.
    
    # So Trustcorp owns both class 3 buildings (Yates and Zimmer) → Option (E) is true
    # and Trustcorp owns exactly 1 class 1 building (either Garza or Flores) → Option (D) is unsure
    
    print(f"\nFrom weight equation 4*t1 + t3 = 6 and t3 <= 2:")
    print(f"t1=1, t3=2 is forced.")
    print(f"So Trustcorp MUST own 1 class 1 and 2 class 3 buildings.")
    print(f"The only class 3 buildings are Yates and Zimmer.")
    print(f"Therefore Trustcorp MUST own Zimmer House. Option (E) must be true.")
    
else:
    print("UNSAT - no valid final state")