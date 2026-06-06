from z3 import *

# We need to model the state of ownership of buildings.
# Buildings: Garza Tower (G), Yates House (Y), Zimmer House (Z),
# Flores Tower (F), Lynch Building (L),
# King Building (K), Meyer Building (M), Ortiz Building (O).
# Classes:
# Class 1: G, F
# Class 2: L, K, M, O
# Class 3: Y, Z

# Initial ownership:
# RealProp: G, Y, Z
# Southco: F, L
# Trustcorp: K, M, O

# Trades allowed:
# 1) One building for one other building of the same class.
# 2) One class 1 building for two class 2 buildings.
# 3) One class 2 building for two class 3 buildings.

# We need to determine what ownership configurations are reachable via any number of trades.
# The question asks: which one CANNOT be true, no matter how many trades are made?
# So we need to check each option for reachability.

# Approach: Model the state as a set of buildings owned by each company.
# Since trades are reversible? Not necessarily symmetric, but we can think of reachable states.
# Better: Model the total "value" or "counts" invariants.

# Let's think about invariants.
# Each building has a class. Let's assign "points" or "units" to each class.
# Trade 1: same class -> no change in class counts.
# Trade 2: 1 class 1 -> 2 class 2. So class1 count decreases by 1, class2 count increases by 2.
# Trade 3: 1 class 2 -> 2 class 3. So class2 count decreases by 1, class3 count increases by 2.

# Let c1, c2, c3 be total counts of class 1, 2, 3 buildings in the system.
# Initially: c1=2 (G,F), c2=4 (L,K,M,O), c3=2 (Y,Z). Total = 8 buildings.
# Trade 1: no change.
# Trade 2: c1 -= 1, c2 += 2. Total buildings: -1+2 = +1.
# Trade 3: c2 -= 1, c3 += 2. Total buildings: -1+2 = +1.

# So total number of buildings can increase! But we have a fixed set of named buildings.
# Actually, the buildings are specific named entities. Trades exchange ownership of specific buildings.
# So the set of buildings is fixed (8 buildings). Each trade exchanges ownership.
# So total buildings per company can change, but total buildings overall is always 8.

# Let's model ownership as: for each building, which company owns it.
# Companies: RealProp (0), Southco (1), Trustcorp (2).

# We need to model trades as transitions. Since number of trades is unbounded, we need to find
# the set of reachable states. This is a graph reachability problem.

# However, we can think about invariants more cleverly.
# Let's assign each building a "weight" such that trades preserve total weight.
# For trade 1: same class -> weight of building A = weight of building B. So all buildings of same class have same weight.
# For trade 2: weight(class1) = 2 * weight(class2). So w1 = 2*w2.
# For trade 3: weight(class2) = 2 * weight(class3). So w2 = 2*w3.
# So w1 = 4*w3, w2 = 2*w3. Let w3 = 1, then w2 = 2, w1 = 4.

# Total weight of all buildings = 2*4 + 4*2 + 2*1 = 8 + 8 + 2 = 18.
# Each company's total weight is invariant under trades? Let's check:
# Trade 1: company A gives building of class X, gets building of same class X. Weight unchanged for both.
# Trade 2: company gives class 1 (weight 4), gets two class 2 (weight 2+2=4). So weight unchanged for both.
# Trade 3: company gives class 2 (weight 2), gets two class 3 (weight 1+1=2). So weight unchanged for both.
# So each company's total weight is invariant!

# Initial weights:
# RealProp: G(4) + Y(1) + Z(1) = 6
# Southco: F(4) + L(2) = 6
# Trustcorp: K(2) + M(2) + O(2) = 6

# So each company always has total weight 6.

# Now let's check each option:

# Option A: RealProp owns L, M, O. L(2)+M(2)+O(2)=6. Weight matches. Possible?
# Option B: Southco owns G and M. G(4)+M(2)=6. Weight matches. Possible?
# Option C: Southco owns K, M, O. K(2)+M(2)+O(2)=6. Weight matches. Possible?
# Option D: Trustcorp owns F and Y. F(4)+Y(1)=5. Weight is 5, not 6. IMPOSSIBLE!
# Option E: Trustcorp owns G and L. G(4)+L(2)=6. Weight matches. Possible?

# So D is impossible by weight invariant alone. But let's verify with Z3 to be safe.

# Let's model the problem more carefully with Z3 to confirm.

# We'll model ownership as integer variables for each building: 0=RealProp, 1=Southco, 2=Trustcorp.
# Initial state: G=0, Y=0, Z=0, F=1, L=1, K=2, M=2, O=2.
# We need to check if a target state is reachable via trades.

# Since trades are reversible (each trade type has an inverse? Let's check:
# Trade 1: A gives X, gets Y (same class). Inverse: A gives Y, gets X. Same type.
# Trade 2: A gives 1 class1, gets 2 class2. Inverse: A gives 2 class2, gets 1 class1. But is this a valid trade type? 
#   The allowed trades are only: 1-for-1 same class, 1 class1 for 2 class2, 1 class2 for 2 class3.
#   The inverse of trade 2 would be: give 2 class2, get 1 class1. This is NOT listed as an allowed trade.
# So trades are NOT reversible in general.

# However, we can think of this as: we can apply trades forward only.
# But we can also think of it as: we can apply trades in any order, and the weight invariant holds.

# Let's use Z3 to model reachability via BFS up to some bound, or use the invariant approach.

# Actually, the weight invariant is sufficient to prove D impossible.
# But let's also check if the other options are actually reachable, to be thorough.

# For a more rigorous check, let's model the state space with Z3 using a bounded number of trades.
# Since we have 8 buildings and 3 companies, the state space is 3^8 = 6561 states.
# We can model this as a graph and check reachability.

# Let's do it properly with Z3 using iterative deepening / BFS.

# First, let's just check the weight invariant for all options.

print("Checking weight invariant for each option:")

# Building classes
classes = {
    "G": 1, "F": 1,
    "L": 2, "K": 2, "M": 2, "O": 2,
    "Y": 3, "Z": 3
}

# Weights
weights = {"G": 4, "F": 4, "L": 2, "K": 2, "M": 2, "O": 2, "Y": 1, "Z": 1}

# Initial ownership
init_owner = {"G": "R", "Y": "R", "Z": "R", "F": "S", "L": "S", "K": "T", "M": "T", "O": "T"}

def weight_of(owner, assignment):
    total = 0
    for b, o in assignment.items():
        if o == owner:
            total += weights[b]
    return total

# Check each option
options = {
    "A": {"R": ["L", "M", "O"], "S": [], "T": []},  # only specifies RealProp
    "B": {"S": ["G", "M"]},
    "C": {"S": ["K", "M", "O"]},
    "D": {"T": ["F", "Y"]},
    "E": {"T": ["G", "L"]}
}

# For options that only specify some companies, the remaining buildings go to the remaining companies.
# But we need to check if there exists ANY assignment of remaining buildings to remaining companies
# that satisfies the weight invariant and is reachable.

# Actually, the options specify the full set of buildings owned by a particular company.
# The remaining buildings must be owned by the other two companies.
# Let's check weight invariant first.

all_buildings = list(classes.keys())

for letter, spec in options.items():
    print(f"\nOption {letter}:")
    for company, bldgs in spec.items():
        w = sum(weights[b] for b in bldgs)
        print(f"  {company} owns {bldgs}, weight = {w}")
        if w != 6:
            print(f"  -> Weight is {w}, not 6. IMPOSSIBLE by invariant.")

# Option D: Trustcorp owns F(4) and Y(1) = 5. Not 6. So D is impossible.

# Let's verify with a full Z3 reachability model to be absolutely sure.

print("\n\nNow verifying with Z3 reachability model...")

# We'll model the state as 8 integer variables (0=R, 1=S, 2=T).
# We'll use BFS up to some depth to check reachability.

from collections import deque

# State: tuple of 8 ints
# Index mapping: 0=G, 1=Y, 2=Z, 3=F, 4=L, 5=K, 6=M, 7=O
building_names = ["G", "Y", "Z", "F", "L", "K", "M", "O"]
building_classes = [1, 3, 3, 1, 2, 2, 2, 2]

init_state = (0, 0, 0, 1, 1, 2, 2, 2)  # R=0, S=1, T=2

def get_owners(state):
    owners = {0: [], 1: [], 2: []}
    for i, o in enumerate(state):
        owners[o].append(i)
    return owners

def get_next_states(state):
    """Generate all states reachable by one trade."""
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
                        # A gives b_a, gets b_b
                        new_state = list(state)
                        new_state[b_a] = company_b
                        new_state[b_b] = company_a
                        next_states.append(tuple(new_state))
    
    # Trade type 2: one class 1 building for two class 2 buildings
    for company_a in range(3):
        for company_b in range(3):
            if company_a == company_b:
                continue
            # A gives a class 1 building, gets two class 2 buildings from B
            for b_a in owners[company_a]:
                if building_classes[b_a] != 1:
                    continue
                # B gives two class 2 buildings
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
                        new_state[b_a] = company_b  # A gives b_a to B
                        new_state[b_b1] = company_a  # B gives b_b1 to A
                        new_state[b_b2] = company_a  # B gives b_b2 to A
                        next_states.append(tuple(new_state))
    
    # Trade type 3: one class 2 building for two class 3 buildings
    for company_a in range(3):
        for company_b in range(3):
            if company_a == company_b:
                continue
            # A gives a class 2 building, gets two class 3 buildings from B
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
                        new_state[b_a] = company_b  # A gives b_a to B
                        new_state[b_b1] = company_a  # B gives b_b1 to A
                        new_state[b_b2] = company_a  # B gives b_b2 to A
                        next_states.append(tuple(new_state))
    
    return next_states

# BFS to find all reachable states
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

# Now check each option
def state_matches_option(state, letter):
    """Check if state matches the given option's specification."""
    # state is tuple of 8 ints
    # Option A: RealProp owns L, M, O
    if letter == "A":
        # RealProp (0) must own L(idx=4), M(idx=6), O(idx=7)
        return state[4] == 0 and state[6] == 0 and state[7] == 0
    # Option B: Southco owns G and M
    elif letter == "B":
        # Southco (1) owns G(idx=0), M(idx=6)
        return state[0] == 1 and state[6] == 1
    # Option C: Southco owns K, M, O
    elif letter == "C":
        # Southco (1) owns K(idx=5), M(idx=6), O(idx=7)
        return state[5] == 1 and state[6] == 1 and state[7] == 1
    # Option D: Trustcorp owns F and Y
    elif letter == "D":
        # Trustcorp (2) owns F(idx=3), Y(idx=1)
        return state[3] == 2 and state[1] == 2
    # Option E: Trustcorp owns G and L
    elif letter == "E":
        # Trustcorp (2) owns G(idx=0), L(idx=4)
        return state[0] == 2 and state[4] == 2
    return False

for letter in ["A", "B", "C", "D", "E"]:
    reachable = any(state_matches_option(s, letter) for s in visited)
    print(f"Option {letter}: {'REACHABLE' if reachable else 'NOT REACHABLE'}")

# The answer should be the one that is NOT reachable.