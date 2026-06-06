from z3 import *

# Define arguments as indices 0-15 (a1 to a16)
args = list(range(16))
arg_names = [f"a{i+1}" for i in range(16)]

# Define levels: level 1 for indices 0-5, level 2 for 6-11, level 3 for 12-15
level = [1 if i < 6 else 2 if i < 12 else 3 for i in range(16)]

# Define attack relations as (attacker, target) tuples
strong_attacks = [
    (1, 0),   # a2 → a1
    (8, 7),   # a9 → a8
    (13, 12), # a14 → a13
    (14, 15), # a15 → a16
    (0, 13),  # a1 → a14
    (15, 14), # a16 → a15
    (0, 2),   # a1 → a3
    (0, 3),   # a1 → a4
    (12, 6),  # a13 → a7
    (12, 9),  # a13 → a10
    (2, 4),   # a3 → a5
    (4, 2),   # a5 → a3
]

weak_attacks = [
    (7, 1),   # a8 → a2
    (12, 8),  # a13 → a9
    (7, 4),   # a8 → a5
    (7, 5),   # a8 → a6
    (15, 10), # a16 → a11
    (15, 11), # a16 → a12
    (1, 6),   # a2 → a7
    (9, 12),  # a10 → a13
]

# Create a function to check if an attack is successful
def successful_attack(attacker, target):
    """Returns a Z3 Bool expression indicating if attack from attacker to target is successful."""
    # Check if it's a strong attack
    if (attacker, target) in strong_attacks:
        return BoolVal(True)
    # Check if it's a weak attack
    if (attacker, target) in weak_attacks:
        # Successful only if attacker level > target level
        return level[attacker] > level[target]
    # No attack exists
    return BoolVal(False)

# Create solver
solver = Solver()

# Boolean variables for each argument being in the extension
in_ext = [Bool(f"in_ext_{i}") for i in range(16)]

# 1. Conflict-free constraint: No argument in extension attacks another in extension
for i in range(16):
    for j in range(16):
        if i != j:
            # If both i and j are in extension, then attack(i,j) must be false
            solver.add(Implies(And(in_ext[i], in_ext[j]), Not(successful_attack(i, j))))

# 2. Self-defending constraint: For every A in extension and external B that attacks A,
#    there must be some C in extension that attacks B
for A in range(16):
    for B in range(16):
        if A != B:
            # If A is in extension and B successfully attacks A, then there must be some C in extension that attacks B
            attacker_condition = successful_attack(B, A)
            defender_exists = Or([And(in_ext[C], successful_attack(C, B)) for C in range(16) if C != B])
            solver.add(Implies(And(in_ext[A], attacker_condition), defender_exists))

# 3. Maximal admissible constraint: For each argument not in extension,
#    adding it would violate either conflict-free or self-defending
for x in range(16):
    # x not in extension
    not_in_x = Not(in_ext[x])
    
    # Check if adding x would violate conflict-free
    conflict_free_violation = Or([And(in_ext[y], successful_attack(x, y)) for y in range(16) if y != x])
    conflict_free_violation = Or(conflict_free_violation, Or([And(in_ext[y], successful_attack(y, x)) for y in range(16) if y != x]))
    
    # Check if adding x would violate self-defending for x
    # For any external attacker z of x, there must be a defender in the new set (including x itself)
    self_defending_violation = False
    for z in range(16):
        if z != x:
            # z successfully attacks x
            if successful_attack(z, x):
                # Check if there's a defender in the new set (extension plus x)
                # Defender can be x itself only if x attacks z
                defender_exists = Or(
                    [And(in_ext[w], successful_attack(w, z)) for w in range(16) if w != z],
                    [And(BoolVal(True), successful_attack(x, z))]  # x can defend itself if it attacks z
                )
                # If no defender exists, then adding x violates self-defending
                self_defending_violation = Or(self_defending_violation, Not(defender_exists))
    
    # If x is not in extension, then at least one of these violations must occur
    solver.add(Implies(not_in_x, Or(conflict_free_violation, self_defending_violation)))

# Find all models (admissible sets)
print("Finding all admissible sets...")
models = []
while solver.check() == sat:
    m = solver.model()
    # Extract the extension
    extension = [i for i in range(16) if is_true(m[in_ext[i]])]
    models.append(extension)
    # Block this model to find next one
    block = Or([in_ext[i] != m[in_ext[i]] for i in range(16)])
    solver.add(block)

print(f"Found {len(models)} admissible sets")

# Filter for maximal admissible sets (preferred extensions)
# A set is maximal if no proper superset is admissible
preferred_extensions = []
for ext in models:
    is_maximal = True
    for other_ext in models:
        if set(ext) < set(other_ext):  # proper subset
            is_maximal = False
            break
    if is_maximal:
        preferred_extensions.append(ext)

print(f"Found {len(preferred_extensions)} preferred extensions")

# Convert to argument names and sort
result = []
for ext in preferred_extensions:
    names = [arg_names[i] for i in ext]
    names.sort()  # Sort alphabetically
    result.append(names)

# Print result in required format
print("STATUS: sat")
print("hierarchical_stable_extensions =", result)