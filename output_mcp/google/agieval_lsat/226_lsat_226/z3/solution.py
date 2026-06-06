from z3 import *

# Buildings and their classes
# G1: Garza Tower (1), Y3: Yates House (3), Z3: Zimmer House (3)
# F1: Flores Tower (1), L2: Lynch Building (2)
# K2: King Building (2), M2: Meyer Building (2), O2: Ortiz Building (2)

# Initial ownership
# R: {G1, Y3, Z3}, S: {F1, L2}, T: {K2, M2, O2}

# Define buildings
buildings = ['G1', 'Y3', 'Z3', 'F1', 'L2', 'K2', 'M2', 'O2']
classes = {'G1': 1, 'Y3': 3, 'Z3': 3, 'F1': 1, 'L2': 2, 'K2': 2, 'M2': 2, 'O2': 2}

# Represent ownership as a function from building to company
# 0: RealProp, 1: Southco, 2: Trustcorp
def get_initial_owner(b):
    if b in ['G1', 'Y3', 'Z3']: return 0
    if b in ['F1', 'L2']: return 1
    if b in ['K2', 'M2', 'O2']: return 2
    return -1

# Define the state after one trade
# We need to check if the transition from initial to final is a valid trade
def is_valid_trade(initial_owners, final_owners):
    # Identify which buildings changed owners
    changed = [b for b in buildings if initial_owners[b] != final_owners[b]]
    
    # If no buildings changed, not a trade
    if not changed: return False
    
    # A trade involves two companies. Let's find which companies were involved.
    # The set of buildings given by company A to company B, and vice versa.
    # This is complex. Let's simplify:
    # A trade is a swap of sets of buildings between two companies.
    # Let the two companies be C1 and C2.
    # C1 gives set S1 to C2.
    # C2 gives set S2 to C1.
    # The trade types:
    # 1. |S1| = 1, |S2| = 1, Class(S1) = Class(S2)
    # 2. |S1| = 1, |S2| = 2, Class(S1) = 1, Class(S2) = 2
    # 3. |S1| = 1, |S2| = 2, Class(S1) = 2, Class(S2) = 3
    
    # Let's find the companies involved.
    # For each company, calculate the set of buildings it gained and lost.
    gained = {c: [] for c in range(3)}
    lost = {c: [] for c in range(3)}
    for b in buildings:
        if initial_owners[b] != final_owners[b]:
            lost[initial_owners[b]].append(b)
            gained[final_owners[b]].append(b)
            
    # Only two companies should be involved in a trade.
    involved = [c for c in range(3) if lost[c] or gained[c]]
    if len(involved) != 2: return False
    
    c1, c2 = involved
    # C1 lost S1, gained S2. C2 lost S2, gained S1.
    # So S1 = lost[c1] = gained[c2]
    # And S2 = lost[c2] = gained[c1]
    s1 = lost[c1]
    s2 = lost[c2]
    
    # Check trade types
    # Type 1: |S1| = 1, |S2| = 1, Class(S1) = Class(S2)
    if len(s1) == 1 and len(s2) == 1:
        if classes[s1[0]] == classes[s2[0]]: return True
        
    # Type 2: 1 (class 1) for 2 (class 2)
    if len(s1) == 1 and len(s2) == 2:
        if classes[s1[0]] == 1 and all(classes[b] == 2 for b in s2): return True
    if len(s1) == 2 and len(s2) == 1:
        if classes[s2[0]] == 1 and all(classes[b] == 2 for b in s1): return True
        
    # Type 3: 1 (class 2) for 2 (class 3)
    if len(s1) == 1 and len(s2) == 2:
        if classes[s1[0]] == 2 and all(classes[b] == 3 for b in s2): return True
    if len(s1) == 2 and len(s2) == 1:
        if classes[s2[0]] == 2 and all(classes[b] == 3 for b in s1): return True
        
    return False

# Define the options
def get_owners_from_option(option_str):
    # This is a bit manual, but we can parse the option strings
    # (A) R: {F1, G1}, S: {L2, Y3, Z3}, T: {K2, M2, O2}
    # (B) R: {G1, K2, O2}, S: {F1, L2}, T: {M2, Y3, Z3}
    # (C) R: {G1, L2}, S: {F1, Y3, Z3}, T: {K2, M2, O2}
    # (D) R: {G1, M2, Y3}, S: {F1, L2}, T: {K2, O2, Z3}
    # (E) R: {G1, Y3, Z3}, S: {L2, O2}, T: {F1, K2, M2}
    
    # Let's just hardcode the final ownership for each option
    if option_str == "A":
        return {'G1':0, 'F1':0, 'L2':1, 'Y3':1, 'Z3':1, 'K2':2, 'M2':2, 'O2':2}
    if option_str == "B":
        return {'G1':0, 'K2':0, 'O2':0, 'F1':1, 'L2':1, 'M2':2, 'Y3':2, 'Z3':2}
    if option_str == "C":
        return {'G1':0, 'L2':0, 'F1':1, 'Y3':1, 'Z3':1, 'K2':2, 'M2':2, 'O2':2}
    if option_str == "D":
        return {'G1':0, 'M2':0, 'Y3':0, 'F1':1, 'L2':1, 'K2':2, 'O2':2, 'Z3':2}
    if option_str == "E":
        return {'G1':0, 'Y3':0, 'Z3':0, 'L2':1, 'O2':1, 'F1':2, 'K2':2, 'M2':2}
    return None

initial_owners = {b: get_initial_owner(b) for b in buildings}

found_options = []
for letter in ["A", "B", "C", "D", "E"]:
    final_owners = get_owners_from_option(letter)
    if is_valid_trade(initial_owners, final_owners):
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")