from z3 import *

# Let me re-examine the problem more carefully.

# The options specify what a particular company owns. The remaining buildings go to the other companies.
# For Option A: "The buildings owned by RealProp are the Lynch Building, the Meyer Building, and the Ortiz Building."
# This means RealProp owns exactly {L, M, O}. The other buildings (G, Y, Z, F, K) are owned by Southco and Trustcorp.
# We need to check if there exists some assignment of the remaining buildings to Southco and Trustcorp
# such that the state is reachable.

# My BFS check for Option A was too loose - I only checked that RealProp owns L, M, O, but didn't check
# that RealProp doesn't own any other buildings. Let me fix that.

# Also, my BFS found Option D as reachable, which contradicts the weight invariant.
# Let me check: Option D says Trustcorp owns F and Y. F is class 1 (weight 4), Y is class 3 (weight 1).
# Total weight = 5. But Trustcorp must have weight 6. So this is impossible.
# My BFS check for D was: state[3] == 2 and state[1] == 2. But this doesn't check that Trustcorp
# doesn't own other buildings. If Trustcorp owns F, Y, and something else, weight could be 6.
# But the option says "The buildings owned by Trustcorp are the Flores Tower and the Yates House."
# This means Trustcorp owns EXACTLY those two buildings, no more.

# Let me redo the BFS with exact matching.

from collections import deque

building_names = ["G", "Y", "Z", "F", "L", "K", "M", "O"]
building_classes = [1, 3, 3, 1, 2, 2, 2, 2]

init_state = (0, 0, 0, 1, 1, 2, 2, 2)  # R=0, S=1, T=2

def get_owners(state):
    owners = {0: [], 1: [], 2: []}
    for i, o in enumerate(state):
        owners[o].append(i)
    return owners

def get_next_states(state):
    owners = get_owners(state)
    next_states = []
    
    # Trade type 1: one building for one other building of the same class
    for company_a in range(3):
        for company_b in range(3):
            if company_a == company_b:
                continue
            for b_a in owners[company_a]:
                for b_b in owners[company_b]:
                    if building_classes[b_a] == building_classes[b_b]:
                        new_state = list(state)
                        new_state[b_a] = company_b
                        new_state[b_b] = company_a
                        next_states.append(tuple(new_state))
    
    # Trade type 2: one class 1 building for two class 2 buildings
    for company_a in range(3):
        for company_b in range(3):
            if company_a == company_b:
                continue
            for b_a in owners[company_a]:
                if building_classes[b_a] != 1:
                    continue
                b_list = owners[company_b]
                for i in range(len(b_list)):
                    if building_classes[b_list[i]] != 2:
                        continue
                    for j in range(i+1, len(b_list)):
                        if building_classes[b_list[j]] != 2:
                            continue
                        b_b1 = b_list[i]
                        b_b2 = b_list[j]
                        new_state = list(state)
                        new_state[b_a] = company_b
                        new_state[b_b1] = company_a
                        new_state[b_b2] = company_a
                        next_states.append(tuple(new_state))
    
    # Trade type 3: one class 2 building for two class 3 buildings
    for company_a in range(3):
        for company_b in range(3):
            if company_a == company_b:
                continue
            for b_a in owners[company_a]:
                if building_classes[b_a] != 2:
                    continue
                b_list = owners[company_b]
                for i in range(len(b_list)):
                    if building_classes[b_list[i]] != 3:
                        continue
                    for j in range(i+1, len(b_list)):
                        if building_classes[b_list[j]] != 3:
                            continue
                        b_b1 = b_list[i]
                        b_b2 = b_list[j]
                        new_state = list(state)
                        new_state[b_a] = company_b
                        new_state[b_b1] = company_a
                        new_state[b_b2] = company_a
                        next_states.append(tuple(new_state))
    
    return next_states

# BFS
visited = set()
queue = deque()
queue.append(init_state)
visited.add(init_state)

while queue:
    curr = queue.popleft()
    for nxt in get_next_states(curr):
        if nxt not in visited:
            visited.add(nxt)
            queue.append(nxt)

print(f"Total reachable states: {len(visited)}")

# Now check each option with EXACT matching
def state_matches_option_exact(state, letter):
    """Check if state matches the given option's specification EXACTLY."""
    # Option A: RealProp (0) owns exactly {L, M, O}
    if letter == "A":
        # RealProp must own L(4), M(6), O(7) and NOT own any other building
        if not (state[4] == 0 and state[6] == 0 and state[7] == 0):
            return False
        # Check RealProp doesn't own any other building
        for i in [0, 1, 2, 3, 5]:
            if state[i] == 0:
                return False
        return True
    
    # Option B: Southco (1) owns exactly {G, M}
    elif letter == "B":
        if not (state[0] == 1 and state[6] == 1):
            return False
        for i in [1, 2, 3, 4, 5, 7]:
            if state[i] == 1:
                return False
        return True
    
    # Option C: Southco (1) owns exactly {K, M, O}
    elif letter == "C":
        if not (state[5] == 1 and state[6] == 1 and state[7] == 1):
            return False
        for i in [0, 1, 2, 3, 4]:
            if state[i] == 1:
                return False
        return True
    
    # Option D: Trustcorp (2) owns exactly {F, Y}
    elif letter == "D":
        if not (state[3] == 2 and state[1] == 2):
            return False
        for i in [0, 2, 4, 5, 6, 7]:
            if state[i] == 2:
                return False
        return True
    
    # Option E: Trustcorp (2) owns exactly {G, L}
    elif letter == "E":
        if not (state[0] == 2 and state[4] == 2):
            return False
        for i in [1, 2, 3, 5, 6, 7]:
            if state[i] == 2:
                return False
        return True
    
    return False

for letter in ["A", "B", "C", "D", "E"]:
    reachable = any(state_matches_option_exact(s, letter) for s in visited)
    print(f"Option {letter}: {'REACHABLE' if reachable else 'NOT REACHABLE'}")

# Also compute weights for each option
print("\n\nWeight check for each option (exact ownership):")
for letter in ["A", "B", "C", "D", "E"]:
    print(f"\nOption {letter}:")
    if letter == "A":
        # R: L(2), M(2), O(2) = 6
        print(f"  RealProp: L(2)+M(2)+O(2) = 6")
        # Remaining: G(4), Y(1), Z(1), F(4), K(2) = 12, split between S and T
        # S and T must each have weight 6
        # Possible: S gets G(4)+Y(1)+Z(1)=6, T gets F(4)+K(2)=6. Yes!
    elif letter == "B":
        # S: G(4)+M(2) = 6
        print(f"  Southco: G(4)+M(2) = 6")
        # Remaining: Y(1), Z(1), F(4), L(2), K(2), O(2) = 12
        # R and T must each have 6
        # R could have Y(1)+Z(1)+F(4)=6, T could have L(2)+K(2)+O(2)=6. Yes!
    elif letter == "C":
        # S: K(2)+M(2)+O(2) = 6
        print(f"  Southco: K(2)+M(2)+O(2) = 6")
        # Remaining: G(4), Y(1), Z(1), F(4), L(2) = 12
        # R and T must each have 6
        # R could have G(4)+Y(1)+Z(1)=6? No, G is class 1, Y and Z are class 3. 4+1+1=6. Yes!
        # T could have F(4)+L(2)=6. Yes!
    elif letter == "D":
        # T: F(4)+Y(1) = 5
        print(f"  Trustcorp: F(4)+Y(1) = 5")
        print(f"  Weight is 5, not 6. IMPOSSIBLE!")
    elif letter == "E":
        # T: G(4)+L(2) = 6
        print(f"  Trustcorp: G(4)+L(2) = 6")
        # Remaining: Y(1), Z(1), F(4), K(2), M(2), O(2) = 12
        # R and S must each have 6
        # R could have Y(1)+Z(1)+F(4)=6, S could have K(2)+M(2)+O(2)=6. Yes!