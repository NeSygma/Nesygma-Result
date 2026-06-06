from z3 import *

# Let me rethink the model. The issue might be with the trade feasibility constraints.
# 
# Initial buildings:
# RP: Garza Tower (c1), Yates House (c3), Zimmer House (c3)
# SC: Flores Tower (c1), Lynch Building (c2)
# TC: King Building (c2), Meyer Building (c2), Ortiz Building (c2)
#
# Trade types:
# A: 1-for-1 same class (swap)
# B: give 1 c1, receive 2 c2
# C: give 1 c2, receive 2 c3
#
# Goal: RP ends with ONLY class 2 buildings.
# RP starts with: 1 c1, 0 c2, 2 c3
# RP must end with: 0 c1, some c2, 0 c3
#
# Let me think about what's possible.
# 
# RP needs to get rid of its c1 (Garza) and its two c3 (Yates, Zimmer).
# 
# Option 1: RP gives Garza (c1) in a type B trade, receiving 2 c2 from someone.
#   Now RP has: 0 c1, 2 c2, 2 c3. Still needs to get rid of c3.
#   RP can give c3 in type A trades (swap for other c3). But that doesn't reduce c3 count.
#   Hmm, RP can't get rid of c3 unless someone wants c3.
#   Type C: someone gives c2 and gets 2 c3. So RP could give c3 to someone doing type C.
#   But RP gives c3 and gets... nothing? No, type C gives c3 to the giver of c2.
#   So if SC gives RP a c2 (type C), RP gets 2 c3. That's worse.
#   
#   Actually wait - type A is a swap. RP gives a c3 and gets a c3 from someone else.
#   That doesn't help RP reduce c3 count.
#   
#   So how does RP get rid of c3? 
#   RP could give c3 to someone who needs c3 for a type C trade.
#   In type C: giver gives 1 c2, receives 2 c3.
#   So if RP is the receiver in type C, RP gives 2 c3 and gets 1 c2.
#   Wait no: the giver gives 1 c2 and receives 2 c3. The receiver gives 2 c3 and receives 1 c2.
#   
#   So RP could receive c2 in a type C trade by giving 2 c3.
#   But RP only has 2 c3 initially. So RP could give both c3 to someone and get 1 c2.
#   
#   Let me trace:
#   Initial RP: 1 c1, 0 c2, 2 c3
#   Step 1: RP gives Garza (c1) to SC in type B. RP gets 2 c2 from SC.
#     RP: 0 c1, 2 c2, 2 c3
#     SC: 2 c1, -1 c2... wait SC only has 1 c2 (Lynch). SC can't give 2 c2.
#   
#   Hmm, SC has 1 c2 (Lynch). TC has 3 c2 (King, Meyer, Ortiz).
#   So RP could trade with TC.
#   
#   Step 1: RP gives Garza (c1) to TC in type B. RP gets 2 c2 from TC.
#     RP: 0 c1, 2 c2, 2 c3
#     TC: 1 c1, 1 c2, 0 c3
#   Step 2: RP gives Yates and Zimmer (2 c3) to TC in type C. RP gets 1 c2 from TC.
#     RP: 0 c1, 3 c2, 0 c3
#     TC: 1 c1, 2 c2, 2 c3
#   
#   This works! RP ends with only c2.
#   
#   Let me check what must be true.
#   After these trades:
#   RP: Garza->TC, Yates->TC, Zimmer->TC. RP has 3 c2 (from TC).
#   SC: Flores (c1), Lynch (c2) - unchanged.
#   TC: Garza (c1), King (c2), Meyer (c2), Ortiz (c2), Yates (c3), Zimmer (c3)
#   
#   Option A: TC owns a c1 building. YES (Garza).
#   Option B: TC owns Meyer. YES (Meyer stayed with TC).
#   Option C: SC owns a c2 building. YES (Lynch).
#   Option D: SC owns both c3 buildings. NO.
#   Option E: SC owns Flores. YES (Flores stayed with SC).
#   
#   So A, B, C, E are all true in this scenario. That can't be right for "must be true".
#   
#   Let me think of another scenario.
#   
#   What if RP gives Garza to SC in type B?
#   SC has 1 c2 (Lynch). SC needs 2 c2 to give. SC only has 1 c2.
#   So SC can't do type B with RP unless SC first acquires another c2.
#   
#   What if RP gives Garza to TC in type B, getting 2 c2 from TC?
#   Then RP has 2 c2, 2 c3.
#   RP gives 2 c3 to SC in type C, getting 1 c2 from SC.
#   RP: 0 c1, 3 c2, 0 c3. Done!
#   SC: Flores (c1), Lynch (c2)... wait SC gave Lynch to RP. SC has: Flores (c1), Yates (c3), Zimmer (c3).
#   TC: Garza (c1), King (c2), Meyer (c2), Ortiz (c2).
#   
#   In this scenario:
#   A: TC owns Garza (c1). YES.
#   B: TC owns Meyer. YES.
#   C: SC owns a c2. NO (SC has Flores c1, Yates c3, Zimmer c3).
#   D: SC owns both c3. YES.
#   E: SC owns Flores. YES.
#   
#   So A, B, D, E are true. C is false.
#   
#   What if RP gives Garza to TC in type B, getting 2 c2 from TC.
#   Then RP gives 2 c3 to TC in type C, getting 1 c2 from TC.
#   RP: 0 c1, 3 c2, 0 c3.
#   TC: Garza (c1), King (c2), Meyer (c2), Ortiz (c2), Yates (c3), Zimmer (c3).
#   SC: Flores (c1), Lynch (c2).
#   
#   A: TC owns Garza (c1). YES.
#   B: TC owns Meyer. YES.
#   C: SC owns Lynch (c2). YES.
#   D: SC owns both c3. NO.
#   E: SC owns Flores. YES.
#   
#   So A, B, C, E are true.
#   
#   What if RP gives Garza to SC in type B? SC needs 2 c2. SC only has 1 c2.
#   SC could first get a c2 from TC via type A (swap Lynch for... something).
#   Or SC could get c2 from TC via type C (SC gives 2 c3... but SC has no c3).
#   
#   Actually, type A is 1-for-1 same class. SC has Lynch (c2). TC has King, Meyer, Ortiz (all c2).
#   SC could swap Lynch for King (type A). Now SC has King (c2), TC has Lynch (c2).
#   Still SC has only 1 c2.
#   
#   SC could get c2 from TC via type B: SC gives Flores (c1) to TC, gets 2 c2 from TC.
#   Now SC has 2 c2 (from TC) and Lynch (c2)... wait SC gave Flores to TC.
#   SC: 0 c1, 3 c2 (Lynch + 2 from TC). TC: 1 c1 (Flores), 1 c2 (remaining).
#   
#   Then RP gives Garza to SC in type B. SC gives 2 c2 to RP.
#   RP: 0 c1, 2 c2, 2 c3.
#   SC: 0 c1, 1 c2, 0 c3.
#   TC: 2 c1 (Flores, Garza), 1 c2.
#   
#   Then RP gives 2 c3 to... who needs c3? SC has no c2 to give. TC has 1 c2.
#   RP gives 2 c3 to TC in type C, getting 1 c2 from TC.
#   RP: 0 c1, 3 c2, 0 c3.
#   TC: 2 c1 (Flores, Garza), 0 c2, 2 c3 (Yates, Zimmer).
#   SC: 0 c1, 1 c2 (Lynch), 0 c3.
#   
#   A: TC owns Flores and Garza (c1). YES.
#   B: TC owns Meyer? TC gave away all c2. Meyer went to SC or RP. NO.
#   C: SC owns Lynch (c2). YES.
#   D: SC owns both c3. NO.
#   E: SC owns Flores. NO (TC owns Flores).
#   
#   So A and C are true.
#   
#   Hmm, so different scenarios give different sets of true options.
#   Let me find what's ALWAYS true.
#   
#   Actually, let me think about this more systematically.
#   
#   RP starts with 1 c1, 0 c2, 2 c3. Must end with 0 c1, some c2, 0 c3.
#   
#   To lose c1: RP must give Garza in type B (getting 2 c2) or type A (getting another c1).
#   If type A, RP swaps Garza for another c1. Then RP still has a c1. So RP must eventually give it in type B.
#   So RP must do at least one type B trade where RP gives a c1.
#   
#   To lose c3: RP has 2 c3. RP can give c3 in type A (swap for other c3) - doesn't reduce count.
#   RP can give c3 in type C as the receiver: RP gives 2 c3, gets 1 c2.
#   So RP must receive at least one type C trade (giving 2 c3, getting 1 c2).
#   
#   So RP does: 1 type B (give c1, get 2 c2) + 1 type C (give 2 c3, get 1 c2) = net +3 c2.
#   RP ends with 3 c2.
#   
#   Now, who gives RP the c2?
#   In type B: someone gives RP 2 c2. That someone must have 2 c2 to give.
#   In type C: someone gives RP 1 c2. That someone must have 1 c2 to give.
#   
#   Initial c2: SC has 1, TC has 3.
#   
#   Case 1: TC gives RP 2 c2 in type B, SC gives RP 1 c2 in type C.
#     TC loses 2 c2, gains 1 c1 (Garza).
#     SC loses 1 c2, gains 2 c3 (Yates, Zimmer).
#     Final: RP has 3 c2. TC has Garza(c1), King/Meyer/Ortiz minus 2 = 1 c2. SC has Flores(c1), Lynch minus 1 = 0 c2, Yates(c3), Zimmer(c3).
#     Wait, SC gives Lynch to RP. SC has: Flores(c1), Yates(c3), Zimmer(c3).
#     TC has: Garza(c1), 1 remaining c2.
#     A: TC owns Garza (c1). YES.
#     B: TC owns Meyer? TC has 1 c2, could be any of King/Meyer/Ortiz. Not necessarily Meyer. NO.
#     C: SC owns a c2? SC has 0 c2. NO.
#     D: SC owns both c3. YES.
#     E: SC owns Flores. YES.
#   
#   Case 2: SC gives RP 2 c2 in type B, TC gives RP 1 c2 in type C.
#     But SC only has 1 c2 initially. SC needs 2 c2.
#     SC could get c2 from TC first.
#     Subcase 2a: SC gets 2 c2 from TC via type B (SC gives Flores c1 to TC).
#       Now SC has 3 c2 (Lynch + 2 from TC). TC has Flores(c1), 1 c2.
#       Then SC gives RP 2 c2 in type B. RP gives Garza to SC.
#       RP: 0 c1, 2 c2, 2 c3. SC: 1 c1 (Garza), 1 c2 (Lynch). TC: 1 c1 (Flores), 1 c2.
#       Then RP gives 2 c3 to TC in type C. TC gives RP 1 c2.
#       RP: 0 c1, 3 c2, 0 c3. TC: 1 c1 (Flores), 0 c2, 2 c3. SC: 1 c1 (Garza), 1 c2 (Lynch).
#       A: TC owns Flores (c1). YES.
#       B: TC owns Meyer? TC has 0 c2. NO.
#       C: SC owns Lynch (c2). YES.
#       D: SC owns both c3. NO.
#       E: SC owns Flores? NO, TC owns Flores. SC owns Garza.
#     
#     Subcase 2b: SC gets 1 c2 from TC via type A (swap Lynch for King).
#       SC has King(c2). TC has Lynch(c2).
#       Still SC has only 1 c2. Can't give 2 c2.
#     
#     Subcase 2c: SC gets c2 from TC via type C (SC gives 2 c3... SC has no c3).
#       Not possible.
#     
#     So subcase 2a is the only way.
#   
#   Case 3: TC gives RP 2 c2 in type B, TC gives RP 1 c2 in type C.
#     TC gives RP 3 c2 total. TC has 3 c2 initially. TC ends with 0 c2.
#     TC gets Garza(c1) and Yates+Zimmer(c3).
#     TC: Garza(c1), Yates(c3), Zimmer(c3). SC: Flores(c1), Lynch(c2).
#     A: TC owns Garza (c1). YES.
#     B: TC owns Meyer? TC has 0 c2. NO.
#     C: SC owns Lynch (c2). YES.
#     D: SC owns both c3. NO.
#     E: SC owns Flores. YES.
#   
#   Case 4: SC gives RP 2 c2 in type B, SC gives RP 1 c2 in type C.
#     SC needs 3 c2. SC has 1 c2 initially. SC needs 2 more c2.
#     SC could get 2 c2 from TC via type B (SC gives Flores to TC).
#     Then SC has 3 c2. SC gives RP 2 c2 in type B (gets Garza). SC gives RP 1 c2 in type C (gets 2 c3).
#     SC: Garza(c1), 0 c2, Yates(c3), Zimmer(c3). TC: Flores(c1), 3 c2. RP: 3 c2.
#     A: TC owns Flores (c1). YES.
#     B: TC owns Meyer? TC has 3 c2 (King, Meyer, Ortiz). YES.
#     C: SC owns a c2? SC has 0 c2. NO.
#     D: SC owns both c3. YES.
#     E: SC owns Flores? NO.
#   
#   Let me check what's common across all cases.
#   
#   Case 1: A=YES, B=NO, C=NO, D=YES, E=YES
#   Case 2a: A=YES, B=NO, C=YES, D=NO, E=NO
#   Case 3: A=YES, B=NO, C=YES, D=NO, E=YES
#   Case 4: A=YES, B=YES, C=NO, D=YES, E=NO
#   
#   Only A is true in ALL cases! TC always ends up with a c1 building.
#   Because RP must give away Garza (c1) in a type B trade, and the receiver gets Garza.
#   
#   Let me verify with Z3.

solver = Solver()

# Buildings: 0=Garza(c1), 1=Yates(c3), 2=Zimmer(c3), 3=Flores(c1), 4=Lynch(c2),
#             5=King(c2), 6=Meyer(c2), 7=Ortiz(c2)
# Owners: 0=RP, 1=SC, 2=TC

init_owner = [0, 0, 0, 1, 1, 2, 2, 2]
bldg_class = [1, 3, 3, 1, 2, 2, 2, 2]
bldg_names = ["Garza", "Yates", "Zimmer", "Flores", "Lynch", "King", "Meyer", "Ortiz"]

# Final owner of each building
final_owner = [Int(f'fo_{i}') for i in range(8)]
for i in range(8):
    solver.add(final_owner[i] >= 0, final_owner[i] <= 2)

# RP ends with only class 2 buildings
rp_c1_count = Sum([If(And(final_owner[i] == 0, bldg_class[i] == 1), 1, 0) for i in range(8)])
rp_c2_count = Sum([If(And(final_owner[i] == 0, bldg_class[i] == 2), 1, 0) for i in range(8)])
rp_c3_count = Sum([If(And(final_owner[i] == 0, bldg_class[i] == 3), 1, 0) for i in range(8)])

solver.add(rp_c1_count == 0)
solver.add(rp_c3_count == 0)
solver.add(rp_c2_count >= 1)

# Trade variables
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

# Final counts
final_c1 = [Sum([If(And(final_owner[i] == k, bldg_class[i] == 1), 1, 0) for i in range(8)]) for k in range(3)]
final_c2 = [Sum([If(And(final_owner[i] == k, bldg_class[i] == 2), 1, 0) for i in range(8)]) for k in range(3)]
final_c3 = [Sum([If(And(final_owner[i] == k, bldg_class[i] == 3), 1, 0) for i in range(8)]) for k in range(3)]

# Net change equations
for k in range(3):
    c1_received = Sum([x[j][k] for j in range(3) if j != k])
    c1_given = Sum([x[k][j] for j in range(3) if j != k])
    solver.add(final_c1[k] - init_c1[k] == c1_received - c1_given)
    
    c2_from_B = 2 * (c1_given - c1_received)
    c2_from_C_received = Sum([y[j][k] for j in range(3) if j != k])
    c2_from_C_given = Sum([y[k][j] for j in range(3) if j != k])
    solver.add(final_c2[k] - init_c2[k] == c2_from_B + c2_from_C_received - c2_from_C_given)
    
    c3_from_C = 2 * (c2_from_C_given - c2_from_C_received)
    solver.add(final_c3[k] - init_c3[k] == c3_from_C)

# Feasibility: a company can only give c1 in type B if it has enough c1
for k in range(3):
    solver.add(Sum([x[k][j] for j in range(3) if j != k]) <= init_c1[k] + Sum([x[j][k] for j in range(3) if j != k]))

# Feasibility: a company can only give c2 in type C if it has enough c2
# c2 available = init_c2 + 2*(c1_given - c1_received) + c2_received_from_C
for k in range(3):
    c2_available = init_c2[k] + 2*(Sum([x[k][j] for j in range(3) if j != k]) - Sum([x[j][k] for j in range(3) if j != k])) + Sum([y[j][k] for j in range(3) if j != k])
    solver.add(Sum([y[k][j] for j in range(3) if j != k]) <= c2_available)

# Also need to ensure c2 available is non-negative at all times
# This is a simplification - we're checking final state feasibility
# but the intermediate steps might not be feasible.
# Let me add constraints that c2 can't go negative.
for k in range(3):
    c2_after_B = init_c2[k] + 2*(Sum([x[k][j] for j in range(3) if j != k]) - Sum([x[j][k] for j in range(3) if j != k]))
    solver.add(c2_after_B >= 0)

print("Checking...")
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
    
    # Enumerate all solutions
    print("\n--- Enumerating all solutions ---")
    decision_vars = final_owner
    
    solutions = []
    solver.push()
    while solver.check() == sat:
        m2 = solver.model()
        sol = tuple(m2.eval(v, model_completion=True).as_long() for v in decision_vars)
        solutions.append(sol)
        solver.add(Or([v != m2.eval(v, model_completion=True) for v in decision_vars]))
    solver.pop()
    
    print(f"Total distinct solutions: {len(solutions)}")
    
    # Check each option across all solutions
    a_true_all = True
    b_true_all = True
    c_true_all = True
    d_true_all = True
    e_true_all = True
    
    for sol in solutions:
        # A: TC owns a c1 building (building 0 or 3)
        if not (sol[0] == 2 or sol[3] == 2):
            a_true_all = False
        
        # B: TC owns Meyer (building 6)
        if not (sol[6] == 2):
            b_true_all = False
        
        # C: SC owns a c2 building (4,5,6,7)
        if not (sol[4] == 1 or sol[5] == 1 or sol[6] == 1 or sol[7] == 1):
            c_true_all = False
        
        # D: SC owns both c3 buildings (1,2)
        if not (sol[1] == 1 and sol[2] == 1):
            d_true_all = False
        
        # E: SC owns Flores (building 3)
        if not (sol[3] == 1):
            e_true_all = False
    
    print(f"\nOption A (TC owns a c1 building) must be true: {a_true_all}")
    print(f"Option B (TC owns Meyer) must be true: {b_true_all}")
    print(f"Option C (SC owns a c2 building) must be true: {c_true_all}")
    print(f"Option D (SC owns both c3 buildings) must be true: {d_true_all}")
    print(f"Option E (SC owns Flores) must be true: {e_true_all}")
    
    # Now use the multiple choice skeleton
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
        c2_available = init_c2[k] + 2*(Sum([x[k][j] for j in range(3) if j != k]) - Sum([x[j][k] for j in range(3) if j != k])) + Sum([y[j][k] for j in range(3) if j != k])
        solver2.add(Sum([y[k][j] for j in range(3) if j != k]) <= c2_available)
    
    for k in range(3):
        c2_after_B = init_c2[k] + 2*(Sum([x[k][j] for j in range(3) if j != k]) - Sum([x[j][k] for j in range(3) if j != k]))
        solver2.add(c2_after_B >= 0)
    
    opt_a = Or([final_owner[0] == 2, final_owner[3] == 2])
    opt_b = (final_owner[6] == 2)
    opt_c = Or([final_owner[4] == 1, final_owner[5] == 1, final_owner[6] == 1, final_owner[7] == 1])
    opt_d = And(final_owner[1] == 1, final_owner[2] == 1)
    opt_e = (final_owner[3] == 1)
    
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
    print("UNSAT - need to refine model")