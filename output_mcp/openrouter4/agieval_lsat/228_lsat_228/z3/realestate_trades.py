from z3 import *

# Buildings and their classes
# G = Garza Tower (class 1), owned by RealProp initially
# Y = Yates House (class 3), owned by RealProp initially
# Z = Zimmer House (class 3), owned by RealProp initially
# F = Flores Tower (class 1), owned by Southco initially
# L = Lynch Building (class 2), owned by Southco initially
# K = King Building (class 2), owned by Trustcorp initially
# M = Meyer Building (class 2), owned by Trustcorp initially
# O = Ortiz Building (class 2), owned by Trustcorp initially

# Building classes
building_class = {
    "G": 1, "Y": 3, "Z": 3, "F": 1, "L": 2, "K": 2, "M": 2, "O": 2
}

# Initial ownership: 0=RealProp, 1=Southco, 2=Trustcorp
initial_owner = {
    "G": 0, "Y": 0, "Z": 0, "F": 1, "L": 1, "K": 2, "M": 2, "O": 2
}

buildings = ["G", "Y", "Z", "F", "L", "K", "M", "O"]

# Total counts
total_class1 = 2  # G, F
total_class2 = 4  # L, K, M, O
total_class3 = 2  # Y, Z

# Invariant: each company's weighted sum (2*c1 + 1*c2 + 0.5*c3) is preserved
# Initial weighted sums:
# RealProp: 2*1 + 1*0 + 0.5*2 = 2 + 0 + 1 = 3
# Southco: 2*1 + 1*1 + 0.5*0 = 2 + 1 + 0 = 3
# Trustcorp: 2*0 + 1*3 + 0.5*0 = 0 + 3 + 0 = 3

# Since RealProp ends with only class 2 buildings, let k = number of class 2 buildings RealProp has.
# Weighted sum = 1*k = 3 (invariant), so k = 3. RealProp must have exactly 3 class 2 buildings.

# Let me model the final ownership and check each option.

solver = Solver()

# Variables: final owner of each building (0=R, 1=S, 2=T)
owner = {b: Int(f"owner_{b}") for b in buildings}

for b in buildings:
    solver.add(owner[b] >= 0, owner[b] <= 2)

# RealProp (owner 0) must own only class 2 buildings at the end
# So RealProp cannot own any class 1 or class 3 building
for b in buildings:
    if building_class[b] != 2:
        solver.add(owner[b] != 0)
    # RealProp must own all its class 2... no, RealProp just needs only class 2s,
    # we don't require RealProp to own any particular buildings.

# RealProp must own at least one building (otherwise "owns only class 2 buildings" is vacuous)
# Actually, let's count RealProp's class 2 buildings
realprop_class2_count = Sum([If(And(owner[b] == 0, building_class[b] == 2), 1, 0) for b in buildings])
# RealProp must have at least 1 class 2 building to "own only class 2 buildings"
solver.add(realprop_class2_count >= 1)

# RealProp has no class 1 or class 3
for b in buildings:
    if building_class[b] == 1:
        solver.add(owner[b] != 0)
    if building_class[b] == 3:
        solver.add(owner[b] != 0)

# Each building belongs to exactly one owner
# (already enforced by domain constraint)

# Now we need to encode that the final state is reachable through legal trades.
# With the weighted sum invariant, we know:
# Each company's weighted sum (2*c1 + 1*c2 + 0.5*c3) remains the same.
# Since RealProp starts with weight 3 and ends with only class 2, 
# RealProp must have exactly 3 class 2 buildings (weight = 1*3 = 3).

realprop_w = Sum([If(owner[b] == 0, 
                    2 if building_class[b] == 1 else (1 if building_class[b] == 2 else 0), 
                    0) for b in buildings])
# Actually, since RealProp has no class 1 or 3, this simplifies:
# But let me just count class 2 buildings for RealProp
solver.add(realprop_class2_count == 3)

# Now let's also enforce the weighted sum invariant for Southco and Trustcorp
# Southco initial weight = 3, Trustcorp initial weight = 3

# Southco's final weighted sum must be 3
southco_w = Sum([If(owner[b] == 1, 
                    2 if building_class[b] == 1 else (1 if building_class[b] == 2 else 0), 
                    0) for b in buildings])

# Wait, 0.5 weight for class 3. Use If to handle this.
southco_w = Sum([If(owner[b] == 1,
                    If(building_class[b] == 1, 2,
                       If(building_class[b] == 2, 1, 0)),
                    0) for b in buildings])
# Hmm, but 0.5 for class 3... Let me multiply everything by 2 to avoid fractions.
# Weight*2: class 1 = 4, class 2 = 2, class 3 = 1
# Initial: RealProp: 4*1 + 2*0 + 1*2 = 6, Southco: 4*1 + 2*1 + 1*0 = 6, Trustcorp: 4*0 + 2*3 + 1*0 = 6

southco_w_times2 = Sum([If(owner[b] == 1,
                           If(building_class[b] == 1, 4,
                              If(building_class[b] == 2, 2, 1)),
                           0) for b in buildings])

trustcorp_w_times2 = Sum([If(owner[b] == 2,
                             If(building_class[b] == 1, 4,
                                If(building_class[b] == 2, 2, 1)),
                             0) for b in buildings])

# For RealProp, all buildings are class 2, weight contribution = 2 each, and we have 3 of them
# So weight*2 = 3*2 = 6. Or compute directly.
realprop_w_times2 = Sum([If(owner[b] == 0,
                            If(building_class[b] == 1, 4,
                               If(building_class[b] == 2, 2, 1)),
                            0) for b in buildings])

solver.add(realprop_w_times2 == 6)
solver.add(southco_w_times2 == 6)
solver.add(trustcorp_w_times2 == 6)

# Also enforce counts: total class 1 = 2, total class 2 = 4, total class 3 = 2
total_c1 = Sum([If(building_class[b] == 1, 1, 0) for b in buildings])
total_c2 = Sum([If(building_class[b] == 2, 1, 0) for b in buildings])
total_c3 = Sum([If(building_class[b] == 3, 1, 0) for b in buildings])
# These are constants, so no need to add as constraints.

print("Base constraints added. Checking satisfiability...")
result = solver.check()
print(f"Result: {result}")

if result == sat:
    m = solver.model()
    print("\nFinal ownership:")
    for b in buildings:
        owners = {0: "RealProp", 1: "Southco", 2: "Trustcorp"}
        print(f"  {b} (class {building_class[b]}): {owners[m[owner[b]].as_long()]}")
    
    # Count by class for each company
    for comp_name, comp_val in [("RealProp", 0), ("Southco", 1), ("Trustcorp", 2)]:
        c1 = sum(1 for b in buildings if building_class[b] == 1 and m[owner[b]].as_long() == comp_val)
        c2 = sum(1 for b in buildings if building_class[b] == 2 and m[owner[b]].as_long() == comp_val)
        c3 = sum(1 for b in buildings if building_class[b] == 3 and m[owner[b]].as_long() == comp_val)
        print(f"  {comp_name}: c1={c1}, c2={c2}, c3={c3}")
    
    # Check each option
    print("\n--- Checking options ---")
    
    # A: Trustcorp owns a class 1 building
    s_a = Solver()
    # Add same base constraints
    for b in buildings:
        s_a.add(owner[b] >= 0, owner[b] <= 2)
    for b in buildings:
        if building_class[b] != 2:
            s_a.add(owner[b] != 0)
    s_a.add(realprop_class2_count >= 1)
    s_a.add(realprop_class2_count == 3)
    s_a.add(realprop_w_times2 == 6)
    s_a.add(southco_w_times2 == 6)
    s_a.add(trustcorp_w_times2 == 6)
    
    # Option A: Trustcorp does NOT own a class 1 building (negation)
    trustcorp_has_c1 = Or([And(owner[b] == 2, building_class[b] == 1) for b in buildings])
    s_a.add(Not(trustcorp_has_c1))
    result_a = s_a.check()
    print(f"Option A (Trustcorp has no class 1 - negation check): {result_a}")
    # If unsat, then Trustcorp must have a class 1 -> A is true
    # If sat, then it's possible that Trustcorp has no class 1 -> A is not necessarily true
    
    # B: Trustcorp owns the Meyer Building
    s_b = Solver()
    for b in buildings:
        s_b.add(owner[b] >= 0, owner[b] <= 2)
    for b in buildings:
        if building_class[b] != 2:
            s_b.add(owner[b] != 0)
    s_b.add(realprop_class2_count >= 1)
    s_b.add(realprop_class2_count == 3)
    s_b.add(realprop_w_times2 == 6)
    s_b.add(southco_w_times2 == 6)
    s_b.add(trustcorp_w_times2 == 6)
    # B: Trustcorp does NOT own Meyer Building (negation)
    s_b.add(owner["M"] != 2)
    result_b = s_b.check()
    print(f"Option B (Trustcorp doesn't own Meyer - negation check): {result_b}")
    
    # C: Southco owns a class 2 building
    s_c = Solver()
    for b in buildings:
        s_c.add(owner[b] >= 0, owner[b] <= 2)
    for b in buildings:
        if building_class[b] != 2:
            s_c.add(owner[b] != 0)
    s_c.add(realprop_class2_count >= 1)
    s_c.add(realprop_class2_count == 3)
    s_c.add(realprop_w_times2 == 6)
    s_c.add(southco_w_times2 == 6)
    s_c.add(trustcorp_w_times2 == 6)
    # C: Southco has NO class 2 buildings (negation)
    southco_has_c2 = Or([And(owner[b] == 1, building_class[b] == 2) for b in buildings])
    s_c.add(Not(southco_has_c2))
    result_c = s_c.check()
    print(f"Option C (Southco has no class 2 - negation check): {result_c}")
    
    # D: Southco owns both class 3 buildings
    s_d = Solver()
    for b in buildings:
        s_d.add(owner[b] >= 0, owner[b] <= 2)
    for b in buildings:
        if building_class[b] != 2:
            s_d.add(owner[b] != 0)
    s_d.add(realprop_class2_count >= 1)
    s_d.add(realprop_class2_count == 3)
    s_d.add(realprop_w_times2 == 6)
    s_d.add(southco_w_times2 == 6)
    s_d.add(trustcorp_w_times2 == 6)
    # D: Southco does NOT own both class 3 buildings (negation)
    # Either Southco doesn't own Y or doesn't own Z
    s_d.add(Or(owner["Y"] != 1, owner["Z"] != 1))
    result_d = s_d.check()
    print(f"Option D (Southco doesn't own both class 3 - negation check): {result_d}")
    
    # E: Southco owns the Flores Tower
    s_e = Solver()
    for b in buildings:
        s_e.add(owner[b] >= 0, owner[b] <= 2)
    for b in buildings:
        if building_class[b] != 2:
            s_e.add(owner[b] != 0)
    s_e.add(realprop_class2_count >= 1)
    s_e.add(realprop_class2_count == 3)
    s_e.add(realprop_w_times2 == 6)
    s_e.add(southco_w_times2 == 6)
    s_e.add(trustcorp_w_times2 == 6)
    # E: Southco does NOT own Flores Tower (negation)
    s_e.add(owner["F"] != 1)
    result_e = s_e.check()
    print(f"Option E (Southco doesn't own Flores - negation check): {result_e}")

else:
    print("No solution found!")