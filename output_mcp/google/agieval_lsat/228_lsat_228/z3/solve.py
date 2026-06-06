from z3 import *

# Buildings:
# RealProp: G(1), Y(3), Z(3)
# Southco: F(1), L(2)
# Trustcorp: K(2), M(2), O(2)

# Total:
# C1: G, F
# C2: L, K, M, O
# C3: Y, Z

# Let's represent the state as a mapping from building to owner.
# Buildings: G, Y, Z, F, L, K, M, O
# Owners: R, S, T

def solve():
    # Initial state
    # G:R, Y:R, Z:R, F:S, L:S, K:T, M:T, O:T
    initial_state = ('R', 'R', 'R', 'S', 'S', 'T', 'T', 'T')
    
    # Building classes:
    # G:1, Y:3, Z:3, F:1, L:2, K:2, M:2, O:2
    classes = {'G':1, 'Y':3, 'Z':3, 'F':1, 'L':2, 'K':2, 'M':2, 'O':2}
    
    reachable = {initial_state}
    queue = [initial_state]
    
    while queue:
        curr = queue.pop(0)
        
        # Get current owners
        # G, Y, Z, F, L, K, M, O
        owners = {'G':curr[0], 'Y':curr[1], 'Z':curr[2], 'F':curr[3], 'L':curr[4], 'K':curr[5], 'M':curr[6], 'O':curr[7]}
        
        # Possible trades:
        # 1. 1-for-1 same class
        # 2. 1 C1 for 2 C2s
        # 3. 1 C2 for 2 C3s
        
        # Find all buildings owned by each company
        comp_buildings = {'R':[], 'S':[], 'T':[]}
        for b, o in owners.items():
            comp_buildings[o].append(b)
            
        # Try all trades
        for c1 in ['R', 'S', 'T']:
            for c2 in ['R', 'S', 'T']:
                if c1 == c2: continue
                
                # Type 1: 1-for-1 same class
                for b1 in comp_buildings[c1]:
                    for b2 in comp_buildings[c2]:
                        if classes[b1] == classes[b2]:
                            # Swap
                            new_owners = owners.copy()
                            new_owners[b1] = c2
                            new_owners[b2] = c1
                            new_state = tuple(new_owners[b] for b in ['G', 'Y', 'Z', 'F', 'L', 'K', 'M', 'O'])
                            if new_state not in reachable:
                                reachable.add(new_state)
                                queue.append(new_state)
                                
                # Type 2: 1 C1 for 2 C2s
                # c1 gives 1 C1, c2 gives 2 C2s
                c1_c1s = [b for b in comp_buildings[c1] if classes[b] == 1]
                c2_c2s = [b for b in comp_buildings[c2] if classes[b] == 2]
                
                if len(c1_c1s) >= 1 and len(c2_c2s) >= 2:
                    for b1 in c1_c1s:
                        for i in range(len(c2_c2s)):
                            for j in range(i+1, len(c2_c2s)):
                                b2a, b2b = c2_c2s[i], c2_c2s[j]
                                new_owners = owners.copy()
                                new_owners[b1] = c2
                                new_owners[b2a] = c1
                                new_owners[b2b] = c1
                                new_state = tuple(new_owners[b] for b in ['G', 'Y', 'Z', 'F', 'L', 'K', 'M', 'O'])
                                if new_state not in reachable:
                                    reachable.add(new_state)
                                    queue.append(new_state)
                                    
                # Type 3: 1 C2 for 2 C3s
                # c1 gives 1 C2, c2 gives 2 C3s
                c1_c2s = [b for b in comp_buildings[c1] if classes[b] == 2]
                c2_c3s = [b for b in comp_buildings[c2] if classes[b] == 3]
                
                if len(c1_c2s) >= 1 and len(c2_c3s) >= 2:
                    for b1 in c1_c2s:
                        for i in range(len(c2_c3s)):
                            for j in range(i+1, len(c2_c3s)):
                                b2a, b2b = c2_c3s[i], c2_c3s[j]
                                new_owners = owners.copy()
                                new_owners[b1] = c2
                                new_owners[b2a] = c1
                                new_owners[b2b] = c1
                                new_state = tuple(new_owners[b] for b in ['G', 'Y', 'Z', 'F', 'L', 'K', 'M', 'O'])
                                if new_state not in reachable:
                                    reachable.add(new_state)
                                    queue.append(new_state)

    # Filter states where RealProp owns only class 2 buildings
    # RealProp buildings: G, Y, Z
    # RealProp owns only class 2:
    # G is class 1, Y is class 3, Z is class 3.
    # Wait, if RealProp owns only class 2 buildings, it must own NO G, Y, or Z.
    # But it must own SOME buildings.
    # Let's re-read: "If RealProp owns only class 2 buildings after some number of trades"
    # This means all buildings RealProp owns are class 2.
    
    final_states = []
    for s in reachable:
        owners = {'G':s[0], 'Y':s[1], 'Z':s[2], 'F':s[3], 'L':s[4], 'K':s[5], 'M':s[6], 'O':s[7]}
        rp_buildings = [b for b, o in owners.items() if o == 'R']
        if len(rp_buildings) > 0 and all(classes[b] == 2 for b in rp_buildings):
            final_states.append(s)
            
    print(f"Number of final states: {len(final_states)}")
    
    # Check options:
    # (A) Trustcorp owns a class 1 building.
    # (B) Trustcorp owns the Meyer Building.
    # (C) Southco owns a class 2 Building.
    # (D) Southco owns both of the class 3 buildings.
    # (E) Southco owns the Flores Tower.
    
    for s in final_states:
        owners = {'G':s[0], 'Y':s[1], 'Z':s[2], 'F':s[3], 'L':s[4], 'K':s[5], 'M':s[6], 'O':s[7]}
        
        # (A) Trustcorp owns a class 1 building.
        # T1 buildings: G, F
        a = (owners['G'] == 'T' or owners['F'] == 'T')
        
        # (B) Trustcorp owns the Meyer Building.
        b = (owners['M'] == 'T')
        
        # (C) Southco owns a class 2 Building.
        # C2 buildings: L, K, M, O
        c = (owners['L'] == 'S' or owners['K'] == 'S' or owners['M'] == 'S' or owners['O'] == 'S')
        
        # (D) Southco owns both of the class 3 buildings.
        # C3 buildings: Y, Z
        d = (owners['Y'] == 'S' and owners['Z'] == 'S')
        
        # (E) Southco owns the Flores Tower.
        e = (owners['F'] == 'S')
        
        print(f"State: {s}, A:{a}, B:{b}, C:{c}, D:{d}, E:{e}")

solve()