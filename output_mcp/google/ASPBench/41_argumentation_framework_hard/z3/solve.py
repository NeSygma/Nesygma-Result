from z3 import *

# Arguments
args = [f"a{i}" for i in range(1, 17)]
arg_to_idx = {arg: i for i, arg in enumerate(args)}
n = len(args)

# Levels
levels = {
    1: ["a1", "a2", "a3", "a4", "a5", "a6"],
    2: ["a7", "a8", "a9", "a10", "a11", "a12"],
    3: ["a13", "a14", "a15", "a16"]
}
arg_level = {}
for lvl, arg_list in levels.items():
    for a in arg_list:
        arg_level[a] = lvl

# Attacks
attacks = [
    ("a2", "a1", 0), ("a9", "a8", 0), ("a14", "a13", 0), ("a15", "a16", 0),
    ("a1", "a14", 0), ("a16", "a15", 0), ("a1", "a3", 0), ("a1", "a4", 0),
    ("a13", "a7", 0), ("a13", "a10", 0), ("a3", "a5", 0), ("a5", "a3", 0),
    ("a8", "a2", 1), ("a13", "a9", 1), ("a8", "a5", 1), ("a8", "a6", 1),
    ("a16", "a11", 1), ("a16", "a12", 1), ("a2", "a7", 1), ("a10", "a13", 1)
]

def is_successful(attacker, target):
    attack_type = None
    for a, t, typ in attacks:
        if a == attacker and t == target:
            attack_type = typ
            break
    if attack_type is None: return False
    if attack_type == 0: return True
    else: return arg_level[attacker] > arg_level[target]

success_matrix = [[False for _ in range(n)] for _ in range(n)]
for a, t, typ in attacks:
    if is_successful(a, t):
        success_matrix[arg_to_idx[a]][arg_to_idx[t]] = True

# Enumerate all admissible sets
# Admissible: Conflict-free AND Self-defending
def get_all_admissible():
    admissible_sets = []
    # Iterate all 2^16 subsets
    import itertools
    for i in range(1 << n):
        subset = [bool((i >> j) & 1) for j in range(n)]
        
        # Conflict-free
        cf = True
        for a in range(n):
            for b in range(n):
                if subset[a] and subset[b] and success_matrix[a][b]:
                    cf = False
                    break
            if not cf: break
        if not cf: continue
        
        # Self-defending
        sd = True
        for a in range(n):
            if subset[a]:
                # For all b that attack a
                for b in range(n):
                    if success_matrix[b][a]:
                        # Must have c in subset that attacks b
                        defended = False
                        for c in range(n):
                            if subset[c] and success_matrix[c][b]:
                                defended = True
                                break
                        if not defended:
                            sd = False
                            break
            if not sd: break
        if sd:
            admissible_sets.append(subset)
    return admissible_sets

admissible_sets = get_all_admissible()

# Filter for maximal ones
preferred = []
for i in range(len(admissible_sets)):
    is_maximal = True
    for j in range(len(admissible_sets)):
        if i == j: continue
        # Check if admissible_sets[j] is a strict superset of admissible_sets[i]
        is_subset = True
        for k in range(n):
            if admissible_sets[i][k] and not admissible_sets[j][k]:
                is_subset = False
                break
        if is_subset:
            # Check if strict
            is_strict = False
            for k in range(n):
                if admissible_sets[j][k] and not admissible_sets[i][k]:
                    is_strict = True
                    break
            if is_strict:
                is_maximal = False
                break
    if is_maximal:
        preferred.append(admissible_sets[i])

print("STATUS: sat")
for sol in preferred:
    ext = [args[i] for i in range(n) if sol[i]]
    print(sorted(ext))