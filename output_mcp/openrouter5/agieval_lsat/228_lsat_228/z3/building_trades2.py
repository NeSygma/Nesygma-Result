from z3 import *

# Let me re-analyze the problem more carefully.
# 
# Initial buildings:
# RP: Garza Tower (c1), Yates House (c3), Zimmer House (c3)
# SC: Flores Tower (c1), Lynch Building (c2)
# TC: King Building (c2), Meyer Building (c2), Ortiz Building (c2)
#
# Trade types:
# A: 1-for-1 same class
# B: give 1 c1, receive 2 c2
# C: give 1 c2, receive 2 c3
#
# Goal: RP ends with ONLY class 2 buildings.
# RP starts with: 1 c1, 0 c2, 2 c3
# RP must end with: 0 c1, some c2, 0 c3
#
# So RP must get rid of its c1 and c3, and acquire c2.
#
# Let's think about what trades can happen.
#
# Type A: 1-for-1 same class. This doesn't change class counts, just ownership.
# Type B: give 1 c1, get 2 c2. Net: -1 c1, +2 c2 for giver; +1 c1, -2 c2 for receiver.
# Type C: give 1 c2, get 2 c3. Net: -1 c2, +2 c3 for giver; +1 c2, -2 c3 for receiver.
#
# RP needs to lose its c1 (Garza Tower) and its two c3 (Yates, Zimmer).
# To lose c1: RP can give Garza in type B (getting 2 c2) or type A (getting another c1, which it then must give away).
# To lose c3: RP can give c3 in type A (getting another c3, which it then must give away).
#   But type A doesn't change counts, so RP can only lose c3 by giving it away and getting nothing back.
#   Wait - type C gives c3 to the giver of c2. So RP could receive c3 in type C trades.
#   But RP needs to end with 0 c3. So RP must give away all c3 it has or receives.
#   RP can give c3 in type A trades (1-for-1 same class).
#
# Actually, the key insight: type A trades just swap buildings of the same class.
# They don't change the count distribution at all.
# So the count distribution is determined entirely by type B and C trades.
#
# Let me model this more carefully with specific buildings.

# Let's use a different approach: model each building's final owner.
# Buildings: 0=Garza(c1), 1=Yates(c3), 2=Zimmer(c3), 3=Flores(c1), 4=Lynch(c2),
#            5=King(c2), 6=Meyer(c2), 7=Ortiz(c2)
# Owners: 0=RP, 1=SC, 2=TC

solver = Solver()

# Initial owners
init_owner = [0, 0, 0, 1, 1, 2, 2, 2]
# Building classes
bldg_class = [1, 3, 3, 1, 2, 2, 2, 2]
# Building names
bldg_names = ["Garza", "Yates", "Zimmer", "Flores", "Lynch", "King", "Meyer", "Ortiz"]

# Final owner of each building
final_owner = [Int(f'fo_{i}') for i in range(8)]
for i in range(8):
    solver.add(final_owner[i] >= 0, final_owner[i] <= 2)

# RP ends with only class 2 buildings
# Count RP's buildings by class
rp_c1_count = Sum([If(And(final_owner[i] == 0, bldg_class[i] == 1), 1, 0) for i in range(8)])
rp_c2_count = Sum([If(And(final_owner[i] == 0, bldg_class[i] == 2), 1, 0) for i in range(8)])
rp_c3_count = Sum([If(And(final_owner[i] == 0, bldg_class[i] == 3), 1, 0) for i in range(8)])

solver.add(rp_c1_count == 0)
solver.add(rp_c3_count == 0)
# RP must have at least some c2 (since it ends with only c2 buildings)
solver.add(rp_c2_count >= 1)

# Now we need to model the trades. Trades are sequences of exchanges.
# Each trade is one of three types.
# 
# Let me think about this differently. The trades must be feasible.
# 
# Type B: give 1 c1, get 2 c2. The giver loses a c1 and gains 2 c2.
#          The receiver loses 2 c2 and gains 1 c1.
# Type C: give 1 c2, get 2 c3. The giver loses a c2 and gains 2 c3.
#          The receiver loses 2 c3 and gains 1 c2.
# Type A: swap 1-for-1 same class. No net change in counts.
#
# Let's model the net flow of buildings between companies.
# 
# Let x_ij = number of type B trades where i gives c1 to j (i gives 1 c1, gets 2 c2 from j)
# Let y_ij = number of type C trades where i gives c2 to j (i gives 1 c2, gets 2 c3 from j)
#
# For each company k, the net change in each class:
# delta_c1[k] = (sum of x_jk for j!=k) - (sum of x_kj for j!=k)
#   i.e., c1 received from others minus c1 given to others
# delta_c2[k] = 2*(sum of x_kj - sum of x_jk) + (sum of y_jk - sum of y_kj)
#   i.e., from type B: receive 2 c2 per trade where k gives c1, lose 2 c2 per trade where k receives c1
#   from type C: receive 1 c2 per trade where k gives c2... wait no.
#   Type C: give 1 c2, get 2 c3. So giver loses 1 c2, receiver gains 1 c2.
#   So delta_c2 from type C: (sum of y_jk) - (sum of y_kj)
#   Wait: y_ij means i gives c2 to j. So i loses 1 c2, j gains 1 c2.
#   So delta_c2[k] = 2*(sum of x_jk - sum of x_kj) + (sum of y_jk - sum of y_kj)
# delta_c3[k] = 2*(sum of y_kj - sum of y_jk)
#   i.e., from type C: giver gains 2 c3, receiver loses 2 c3

# Let's use variables for the trade counts
x = [[Int(f'x_{i}_{j}') for j in range(3)] for i in range(3)]
y = [[Int(f'y_{i}_{j}') for j in range(3)] for i in range(3)]

for i in range(3):
    for j in range(3):
        solver.add(x[i][j] >= 0)
        solver.add(y[i][j] >= 0)
        if i == j:
            solver.add(x[i][j] == 0)
            solver.add(y[i][j] == 0)

# Initial counts
init_c1 = [1, 1, 0]
init_c2 = [0, 1, 3]
init_c3 = [2, 0, 0]

# Final counts (derived from final_owner)
final_c1 = [Sum([If(And(final_owner[i] == k, bldg_class[i] == 1), 1, 0) for i in range(8)]) for k in range(3)]
final_c2 = [Sum([If(And(final_owner[i] == k, bldg_class[i] == 2), 1, 0) for i in range(8)]) for k in range(3)]
final_c3 = [Sum([If(And(final_owner[i] == k, bldg_class[i] == 3), 1, 0) for i in range(8)]) for k in range(3)]

# Net change equations
for k in range(3):
    # delta_c1 = c1 received - c1 given
    c1_received = Sum([x[j][k] for j in range(3) if j != k])
    c1_given = Sum([x[k][j] for j in range(3) if j != k])
    solver.add(final_c1[k] - init_c1[k] == c1_received - c1_given)
    
    # delta_c2 = 2*(c1_given - c1_received) + (c2_received - c2_given)
    # where c2_received from type C = sum of y[j][k], c2_given in type C = sum of y[k][j]
    c2_from_B = 2 * (c1_given - c1_received)
    c2_from_C_received = Sum([y[j][k] for j in range(3) if j != k])
    c2_from_C_given = Sum([y[k][j] for j in range(3) if j != k])
    solver.add(final_c2[k] - init_c2[k] == c2_from_B + c2_from_C_received - c2_from_C_given)
    
    # delta_c3 = 2*(c3_received - c3_given) where c3 comes from type C
    # giver of c2 gets 2 c3, receiver of c2 loses 2 c3
    c3_from_C = 2 * (c2_from_C_given - c2_from_C_received)
    solver.add(final_c3[k] - init_c3[k] == c3_from_C)

# Also need to ensure that during the process, companies have enough buildings to trade.
# This is a feasibility constraint.
# For type B: company k must have enough c1 to give. The total c1 it gives in type B
# is sum(x[k][j]). It starts with init_c1[k] c1 and can receive c1 from type B trades.
# So: sum(x[k][j]) <= init_c1[k] + sum(x[j][k])
for k in range(3):
    solver.add(Sum([x[k][j] for j in range(3) if j != k]) <= init_c1[k] + Sum([x[j][k] for j in range(3) if j != k]))

# For type C: company k must have enough c2 to give.
# sum(y[k][j]) <= init_c2[k] + 2*(sum(x[k][j]) - sum(x[j][k])) + sum(y[j][k])
# The c2 available to give is: initial c2 + c2 gained from type B + c2 gained from type C
for k in range(3):
    c2_from_B_given = 2 * Sum([x[k][j] for j in range(3) if j != k])
    c2_from_B_received = 2 * Sum([x[j][k] for j in range(3) if j != k])
    c2_from_C_received = Sum([y[j][k] for j in range(3) if j != k])
    solver.add(Sum([y[k][j] for j in range(3) if j != k]) <= init_c2[k] + c2_from_B_received - c2_from_B_given + c2_from_C_received)

print("Checking model...")
result = solver.check()
print(f"Result: {result}")

if result == sat:
    m = solver.model()
    print("\nFinal owners:")
    for i in range(8):
        owner = m[final_owner[i]].as_long()
        owner_name = ["RP", "SC", "TC"][owner]
        print(f"  {bldg_names[i]} (c{bldg_class[i]}): {owner_name}")
    
    print("\nFinal counts:")
    for k, name in enumerate(["RP", "SC", "TC"]):
        print(f"  {name}: c1={m[final_c1[k]]}, c2={m[final_c2[k]]}, c3={m[final_c3[k]]}")
    
    print("\nTrade counts:")
    for i in range(3):
        for j in range(3):
            if i != j:
                xi = m[x[i][j]].as_long()
                yi = m[y[i][j]].as_long()
                if xi > 0 or yi > 0:
                    print(f"  x[{i}][{j}]={xi}, y[{i}][{j}]={yi}")
    
    # Now enumerate all solutions to find what MUST be true
    print("\n--- Enumerating all solutions ---")
    
    # Decision variables for enumeration: final_owner for each building
    decision_vars = final_owner
    
    solutions = []
    while solver.check() == sat:
        m = solver.model()
        sol = tuple(m.eval(v, model_completion=True).as_long() for v in decision_vars)
        solutions.append(sol)
        # Block this solution
        solver.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))
    
    print(f"Total distinct solutions: {len(solutions)}")
    
    # Check each option across all solutions
    # Option A: Trustcorp owns a class 1 building
    # Option B: Trustcorp owns the Meyer Building
    # Option C: Southco owns a class 2 building
    # Option D: Southco owns both of the class 3 buildings
    # Option E: Southco owns the Flores Tower
    
    # For each option, check if it's true in ALL solutions (must be true)
    a_true_all = True
    b_true_all = True
    c_true_all = True
    d_true_all = True
    e_true_all = True
    
    for sol in solutions:
        # sol[i] = owner of building i
        # TC owns a c1 building: building 0 (Garza, c1) or 3 (Flores, c1) owned by TC (2)
        a_here = (sol[0] == 2 or sol[3] == 2)
        if not a_here:
            a_true_all = False
        
        # TC owns Meyer (building 6)
        b_here = (sol[6] == 2)
        if not b_here:
            b_true_all = False
        
        # SC owns a c2 building: buildings 4(Lynch,c2),5(King,c2),6(Meyer,c2),7(Ortiz,c2) owned by SC(1)
        c_here = (sol[4] == 1 or sol[5] == 1 or sol[6] == 1 or sol[7] == 1)
        if not c_here:
            c_true_all = False
        
        # SC owns both c3 buildings: buildings 1(Yates,c3) and 2(Zimmer,c3) both owned by SC(1)
        d_here = (sol[1] == 1 and sol[2] == 1)
        if not d_here:
            d_true_all = False
        
        # SC owns Flores Tower (building 3, c1)
        e_here = (sol[3] == 1)
        if not e_here:
            e_true_all = False
    
    print(f"\nOption A (TC owns a c1 building) must be true: {a_true_all}")
    print(f"Option B (TC owns Meyer) must be true: {b_true_all}")
    print(f"Option C (SC owns a c2 building) must be true: {c_true_all}")
    print(f"Option D (SC owns both c3 buildings) must be true: {d_true_all}")
    print(f"Option E (SC owns Flores Tower) must be true: {e_true_all}")
    
    # Now use the multiple choice skeleton
    # Re-create solver with base constraints
    solver2 = Solver()
    
    for i in range(8):
        solver2.add(final_owner[i] >= 0, final_owner[i] <= 2)
    
    solver2.add(rp_c1_count == 0)
    solver2.add(rp_c3_count == 0)
    solver2.add(rp_c2_count >= 1)
    
    for i in range(3):
        for j in range(3):
            solver2.add(x[i][j] >= 0)
            solver2.add(y[i][j] >= 0)
            if i == j:
                solver2.add(x[i][j] == 0)
                solver2.add(y[i][j] == 0)
    
    for k in range(3):
        c1_received = Sum([x[j][k] for j in range(3) if j != k])
        c1_given = Sum([x[k][j] for j in range(3) if j != k])
        solver2.add(final_c1[k] - init_c1[k] == c1_received - c1_given)
        
        c2_from_B = 2 * (c1_given - c1_received)
        c2_from_C_received = Sum([y[j][k] for j in range(3) if j != k])
        c2_from_C_given = Sum([y[k][j] for j in range(3) if j != k])
        solver2.add(final_c2[k] - init_c2[k] == c2_from_B + c2_from_C_received - c2_from_C_given)
        
        c3_from_C = 2 * (c2_from_C_given - c2_from_C_received)
        solver2.add(final_c3[k] - init_c3[k] == c3_from_C)
    
    for k in range(3):
        solver2.add(Sum([x[k][j] for j in range(3) if j != k]) <= init_c1[k] + Sum([x[j][k] for j in range(3) if j != k]))
    
    for k in range(3):
        c2_from_B_given = 2 * Sum([x[k][j] for j in range(3) if j != k])
        c2_from_B_received = 2 * Sum([x[j][k] for j in range(3) if j != k])
        c2_from_C_received = Sum([y[j][k] for j in range(3) if j != k])
        solver2.add(Sum([y[k][j] for j in range(3) if j != k]) <= init_c2[k] + c2_from_B_received - c2_from_B_given + c2_from_C_received)
    
    # Option constraints
    opt_a = Or([final_owner[0] == 2, final_owner[3] == 2])  # TC owns a c1 building
    opt_b = (final_owner[6] == 2)  # TC owns Meyer
    opt_c = Or([final_owner[4] == 1, final_owner[5] == 1, final_owner[6] == 1, final_owner[7] == 1])  # SC owns a c2
    opt_d = And(final_owner[1] == 1, final_owner[2] == 1)  # SC owns both c3
    opt_e = (final_owner[3] == 1)  # SC owns Flores
    
    found_options = []
    for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
        solver2.push()
        solver2.add(constr)
        if solver2.check() == sat:
            found_options.append(letter)
        solver2.pop()
    
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
else:
    print("UNSAT")