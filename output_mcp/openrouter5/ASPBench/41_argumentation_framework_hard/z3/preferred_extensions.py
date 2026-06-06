from z3 import *

# Arguments
args = ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9", "a10", "a11", "a12", "a13", "a14", "a15", "a16"]
n = len(args)

# Levels
levels = {
    "a1": 1, "a2": 1, "a3": 1, "a4": 1, "a5": 1, "a6": 1,
    "a7": 2, "a8": 2, "a9": 2, "a10": 2, "a11": 2, "a12": 2,
    "a13": 3, "a14": 3, "a15": 3, "a16": 3
}

# Strong attacks: (attacker, target)
strong_attacks = [
    ("a2", "a1"), ("a9", "a8"), ("a14", "a13"), ("a15", "a16"),
    ("a1", "a14"), ("a16", "a15"), ("a1", "a3"), ("a1", "a4"),
    ("a13", "a7"), ("a13", "a10"), ("a3", "a5"), ("a5", "a3")
]

# Weak attacks: (attacker, target)
weak_attacks = [
    ("a8", "a2"), ("a13", "a9"), ("a8", "a5"), ("a8", "a6"),
    ("a16", "a11"), ("a16", "a12"), ("a2", "a7"), ("a10", "a13")
]

# Map argument name to index
arg_index = {a: i for i, a in enumerate(args)}

# Decision variables: in_ext[i] = True if arg i is in the extension
in_ext = [Bool(f"in_{args[i]}") for i in range(n)]

solver = Solver()

# Build list of all successful attacks (attacker_idx, target_idx)
# Strong attacks are always successful.
# Weak attacks are successful iff level(attacker) > level(target).
successful_attacks = []
for att, tgt in strong_attacks:
    successful_attacks.append((arg_index[att], arg_index[tgt]))
for att, tgt in weak_attacks:
    if levels[att] > levels[tgt]:
        successful_attacks.append((arg_index[att], arg_index[tgt]))

# Build targets_of: for each attacker, list of targets it successfully attacks
targets_of = {i: [] for i in range(n)}
for att_idx, tgt_idx in successful_attacks:
    targets_of[att_idx].append(tgt_idx)

# Build attackers_of: for each target, list of attackers that successfully attack it
attackers_of = {i: [] for i in range(n)}
for att_idx, tgt_idx in successful_attacks:
    attackers_of[tgt_idx].append(att_idx)

# --- Constraint 1: Conflict-Free ---
# No argument in the extension successfully attacks another argument in the extension.
for att_idx, tgt_idx in successful_attacks:
    solver.add(Not(And(in_ext[att_idx], in_ext[tgt_idx])))

# --- Constraint 2: Self-Defending ---
# For every argument A in the extension and every external argument B that successfully attacks A,
# there must be an argument C in the extension that successfully attacks B.
for a_idx in range(n):
    for b_idx in attackers_of[a_idx]:
        defenders = targets_of[b_idx]  # all C that successfully attack B
        if len(defenders) == 0:
            # No one attacks B, so if B attacks a member, it's impossible to defend.
            solver.add(Not(And(in_ext[a_idx], Not(in_ext[b_idx]))))
        else:
            defender_cond = Or([in_ext[c_idx] for c_idx in defenders])
            solver.add(Implies(And(in_ext[a_idx], Not(in_ext[b_idx])), defender_cond))

# --- Constraint 3: Maximal Admissible (Preferred Extension) ---
# For each argument X not in the extension, adding X would violate conflict-free or self-defending.
for x_idx in range(n):
    # Collect reasons why X cannot be added
    reasons = []
    
    # (a) X attacks some member Y in ext
    cond_a_parts = [in_ext[y_idx] for y_idx in targets_of[x_idx]]
    if cond_a_parts:
        reasons.append(Or(cond_a_parts))
    
    # (b) Some member Y in ext attacks X
    cond_b_parts = [in_ext[y_idx] for y_idx in attackers_of[x_idx]]
    if cond_b_parts:
        reasons.append(Or(cond_b_parts))
    
    # (c) There exists an external attacker B of X such that no member C in ext attacks B
    cond_c_parts = []
    for b_idx in attackers_of[x_idx]:
        defenders_of_b = targets_of[b_idx]
        if len(defenders_of_b) == 0:
            cond_c_parts.append(Not(in_ext[b_idx]))
        else:
            no_defender = And([Not(in_ext[c_idx]) for c_idx in defenders_of_b])
            cond_c_parts.append(And(Not(in_ext[b_idx]), no_defender))
    if cond_c_parts:
        reasons.append(Or(cond_c_parts))
    
    if reasons:
        solver.add(Implies(Not(in_ext[x_idx]), Or(reasons)))
    else:
        # If no reasons, X can always be added, so X must be in the extension
        solver.add(in_ext[x_idx])

# Solve and enumerate all solutions
solutions = []
while solver.check() == sat:
    m = solver.model()
    ext = sorted([args[i] for i in range(n) if is_true(m[in_ext[i]])])
    solutions.append(ext)
    
    # Block this solution
    solver.add(Or([in_ext[i] != m[in_ext[i]] for i in range(n)]))

print(f"STATUS: sat")
print(f"Total preferred extensions: {len(solutions)}")
for i, ext in enumerate(solutions):
    print(f"Extension {i+1}: {ext}")