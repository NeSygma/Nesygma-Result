from collections import deque

buildings = ['G', 'Y', 'Z', 'F', 'L', 'K', 'M', 'O']
classes = {'G': 1, 'Y': 3, 'Z': 3, 'F': 1, 'L': 2, 'K': 2, 'M': 2, 'O': 2}

# State: (owner_G, owner_Y, owner_Z, owner_F, owner_L, owner_K, owner_M, owner_O, has_traded_S_T)
initial_state = ('R', 'R', 'R', 'S', 'S', 'T', 'T', 'T', False)

def get_next_states(state):
    next_states = []
    owners_map = state[:8]
    has_traded_S_T = state[8]
    
    counts = {'R': {1:0, 2:0, 3:0}, 'S': {1:0, 2:0, 3:0}, 'T': {1:0, 2:0, 3:0}}
    for i, owner in enumerate(owners_map):
        counts[owner][classes[buildings[i]]] += 1
    
    owners = ['R', 'S', 'T']
    for i in range(3):
        for j in range(i + 1, 3):
            o1, o2 = owners[i], owners[j]
            new_has_traded = has_traded_S_T or ((o1 == 'S' and o2 == 'T') or (o1 == 'T' and o2 == 'S'))
            
            # Type 1: 1-for-1 same class c
            for c in [1, 2, 3]:
                if counts[o1][c] >= 1 and counts[o2][c] >= 1:
                    b1_list = [b_idx for b_idx, b in enumerate(buildings) if owners_map[b_idx] == o1 and classes[b] == c]
                    b2_list = [b_idx for b_idx, b in enumerate(buildings) if owners_map[b_idx] == o2 and classes[b] == c]
                    for b1 in b1_list:
                        for b2 in b2_list:
                            new_state = list(owners_map)
                            new_state[b1] = o2
                            new_state[b2] = o1
                            next_states.append(tuple(new_state + [new_has_traded]))
            
            # Type 2: 1 class 1 for 2 class 2
            # o1 gives 1 class 1, o2 gives 2 class 2
            if counts[o1][1] >= 1 and counts[o2][2] >= 2:
                b1_list = [b_idx for b_idx, b in enumerate(buildings) if owners_map[b_idx] == o1 and classes[b] == 1]
                b2_list = [b_idx for b_idx, b in enumerate(buildings) if owners_map[b_idx] == o2 and classes[b] == 2]
                for b1 in b1_list:
                    for b2_idx1 in range(len(b2_list)):
                        for b2_idx2 in range(b2_idx1 + 1, len(b2_list)):
                            new_state = list(owners_map)
                            new_state[b1] = o2
                            new_state[b2_list[b2_idx1]] = o1
                            new_state[b2_list[b2_idx2]] = o1
                            next_states.append(tuple(new_state + [new_has_traded]))
            
            # o2 gives 1 class 1, o1 gives 2 class 2
            if counts[o2][1] >= 1 and counts[o1][2] >= 2:
                b2_list = [b_idx for b_idx, b in enumerate(buildings) if owners_map[b_idx] == o2 and classes[b] == 1]
                b1_list = [b_idx for b_idx, b in enumerate(buildings) if owners_map[b_idx] == o1 and classes[b] == 2]
                for b2 in b2_list:
                    for b1_idx1 in range(len(b1_list)):
                        for b1_idx2 in range(b1_idx1 + 1, len(b1_list)):
                            new_state = list(owners_map)
                            new_state[b2] = o1
                            new_state[b1_list[b1_idx1]] = o2
                            new_state[b1_list[b1_idx2]] = o2
                            next_states.append(tuple(new_state + [new_has_traded]))
            
            # Type 3: 1 class 2 for 2 class 3
            # o1 gives 1 class 2, o2 gives 2 class 3
            if counts[o1][2] >= 1 and counts[o2][3] >= 2:
                b1_list = [b_idx for b_idx, b in enumerate(buildings) if owners_map[b_idx] == o1 and classes[b] == 2]
                b2_list = [b_idx for b_idx, b in enumerate(buildings) if owners_map[b_idx] == o2 and classes[b] == 3]
                for b1 in b1_list:
                    for b2_idx1 in range(len(b2_list)):
                        for b2_idx2 in range(b2_idx1 + 1, len(b2_list)):
                            new_state = list(owners_map)
                            new_state[b1] = o2
                            new_state[b2_list[b2_idx1]] = o1
                            new_state[b2_list[b2_idx2]] = o1
                            next_states.append(tuple(new_state + [new_has_traded]))
            
            # o2 gives 1 class 2, o1 gives 2 class 3
            if counts[o2][2] >= 1 and counts[o1][3] >= 2:
                b2_list = [b_idx for b_idx, b in enumerate(buildings) if owners_map[b_idx] == o2 and classes[b] == 2]
                b1_list = [b_idx for b_idx, b in enumerate(buildings) if owners_map[b_idx] == o1 and classes[b] == 3]
                for b2 in b2_list:
                    for b1_idx1 in range(len(b1_list)):
                        for b1_idx2 in range(b1_idx1 + 1, len(b1_list)):
                            new_state = list(owners_map)
                            new_state[b2] = o1
                            new_state[b1_list[b1_idx1]] = o2
                            new_state[b1_list[b1_idx2]] = o2
                            next_states.append(tuple(new_state + [new_has_traded]))
                            
    return next_states

visited = {initial_state}
queue = deque([initial_state])
target_states = []

while queue:
    state = queue.popleft()
    
    counts = {'R': {1:0, 2:0, 3:0}, 'S': {1:0, 2:0, 3:0}, 'T': {1:0, 2:0, 3:0}}
    for i, owner in enumerate(state[:8]):
        counts[owner][classes[buildings[i]]] += 1
    
    if counts['T'][2] == 0:
        target_states.append(state)
    
    for next_state in get_next_states(state):
        if next_state not in visited:
            visited.add(next_state)
            queue.append(next_state)

print(f"Found {len(target_states)} target states.")

# Check options
def check_option(option_func):
    return all(option_func(s) for s in target_states)

# (A) RealProp owns a class 1 building.
def opt_a(s):
    counts = {'R': {1:0, 2:0, 3:0}}
    for i, owner in enumerate(s[:8]):
        if owner == 'R': counts['R'][classes[buildings[i]]] += 1
    return counts['R'][1] > 0

# (B) Southco owns only class 2 buildings.
def opt_b(s):
    counts = {'S': {1:0, 2:0, 3:0}}
    total_S = 0
    for i, owner in enumerate(s[:8]):
        if owner == 'S': 
            counts['S'][classes[buildings[i]]] += 1
            total_S += 1
    return total_S > 0 and counts['S'][1] == 0 and counts['S'][3] == 0

# (C) Southco has made at least one trade with Trustcorp.
def opt_c(s):
    return s[8]

# (D) Trustcorp owns the Garza Tower.
def opt_d(s):
    return s[buildings.index('G')] == 'T'

# (E) Trustcorp owns the Zimmer House.
def opt_e(s):
    return s[buildings.index('Z')] == 'T'

print("A:", check_option(opt_a))
print("B:", check_option(opt_b))
print("C:", check_option(opt_c))
print("D:", check_option(opt_d))
print("E:", check_option(opt_e))