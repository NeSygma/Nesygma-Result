from z3 import *
import itertools

# Businesses: 0:Optometrist, 1:Pharmacy, 2:Restaurant1, 3:Restaurant2, 4:Shoe, 5:Toy, 6:Veterinarian
# Spaces: 0 to 6 (representing 1 to 7)

def get_valid_permutations(constraint_2_func):
    valid_perms = []
    # Permutations of [0, 1, 2, 3, 4, 5, 6]
    # 0:O, 1:P, 2:R1, 3:R2, 4:S, 5:T, 6:V
    for p in itertools.permutations(range(7)):
        # p[i] is the business at space i
        # pos[business] is the space of the business
        pos = [0] * 7
        for space, business in enumerate(p):
            pos[business] = space
        
        # Constraint 1: Pharmacy at one end, one restaurant at the other
        c1 = (pos[1] == 0 and (pos[2] == 6 or pos[3] == 6)) or \
             (pos[1] == 6 and (pos[2] == 0 or pos[3] == 0))
        
        if not c1: continue
        
        # Constraint 2 (Variable)
        if not constraint_2_func(pos): continue
        
        # Constraint 3: Pharmacy next to O or V
        c3 = (abs(pos[1] - pos[0]) == 1) or (abs(pos[1] - pos[6]) == 1)
        if not c3: continue
        
        # Constraint 4: Toy store not next to V
        c4 = abs(pos[5] - pos[6]) != 1
        if not c4: continue
        
        valid_perms.append(p)
    return set(valid_perms)

# Original Constraint 2: Two restaurants separated by at least two other businesses
def original_c2(pos):
    return abs(pos[2] - pos[3]) >= 3

# Options
def opt_a(pos):
    # A restaurant must be in either space 3, 4, or 5 (indices 2, 3, 4)
    return (pos[2] in [2, 3, 4]) or (pos[3] in [2, 3, 4])

def opt_b(pos):
    # A restaurant must be next to either the optometrist or the veterinarian
    return (abs(pos[2] - pos[0]) == 1 or abs(pos[2] - pos[6]) == 1) or \
           (abs(pos[3] - pos[0]) == 1 or abs(pos[3] - pos[6]) == 1)

def opt_c(pos):
    # Either the toy store or the veterinarian must be somewhere between the two restaurants
    # Between means pos[R1] < pos[T] < pos[R2] or pos[R2] < pos[T] < pos[R1]
    # OR pos[R1] < pos[V] < pos[R2] or pos[R2] < pos[V] < pos[R1]
    between_t = (pos[2] < pos[5] < pos[3]) or (pos[3] < pos[5] < pos[2])
    between_v = (pos[2] < pos[6] < pos[3]) or (pos[3] < pos[6] < pos[2])
    return between_t or between_v

def opt_d(pos):
    # No more than two businesses can separate the pharmacy and the restaurant nearest it
    # "The restaurant nearest it" - let's find which restaurant is closer to P
    # P is at 0 or 6.
    # If P is at 0, distance to R1 is pos[2], distance to R2 is pos[3].
    # Nearest is min(pos[2], pos[3]).
    # "No more than two businesses can separate" means distance <= 3.
    if pos[1] == 0:
        return min(pos[2], pos[3]) <= 3
    else:
        return min(6 - pos[2], 6 - pos[3]) <= 3

def opt_e(pos):
    # The optometrist cannot be next to the shoe store
    return abs(pos[0] - pos[4]) != 1

# Calculate sets
s_orig = get_valid_permutations(original_c2)
print(f"Original set size: {len(s_orig)}")

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]
for name, func in options:
    s_opt = get_valid_permutations(func)
    if s_orig == s_opt:
        print(f"Option {name} is equivalent.")
    else:
        print(f"Option {name} is NOT equivalent. Size: {len(s_opt)}")