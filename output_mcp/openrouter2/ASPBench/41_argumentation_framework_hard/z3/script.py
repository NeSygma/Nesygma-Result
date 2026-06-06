from z3 import *

# Argument names
args = [f"a{i}" for i in range(1, 17)]
arg_index = {name: i for i, name in enumerate(args)}

# Levels
levels = {
    'a1':1,'a2':1,'a3':1,'a4':1,'a5':1,'a6':1,
    'a7':2,'a8':2,'a9':2,'a10':2,'a11':2,'a12':2,
    'a13':3,'a14':3,'a15':3,'a16':3
}

# Attack lists
strong_attacks = [
    ('a2','a1'),('a9','a8'),('a14','a13'),('a15','a16'),
    ('a1','a14'),('a16','a15'),('a1','a3'),('a1','a4'),
    ('a13','a7'),('a13','a10'),('a3','a5'),('a5','a3')
]
weak_attacks = [
    ('a8','a2'),('a13','a9'),('a8','a5'),('a8','a6'),
    ('a16','a11'),('a16','a12'),('a2','a7'),('a10','a13')
]

# Precompute attack_successful matrix
n = len(args)
attack_successful = [[BoolVal(False) for _ in range(n)] for _ in range(n)]
# Strong attacks always true
for a,b in strong_attacks:
    i,j = arg_index[a], arg_index[b]
    attack_successful[i][j] = BoolVal(True)
# Weak attacks: true iff level(attacker) > level(target)
for a,b in weak_attacks:
    i,j = arg_index[a], arg_index[b]
    if levels[a] > levels[b]:
        attack_successful[i][j] = BoolVal(True)
    else:
        attack_successful[i][j] = BoolVal(False)

# Boolean variables for inclusion in extension
arg_vars = [Bool(f"in_{name}") for name in args]

solver = Solver()

# Conflict-free: no successful attack between members
for i in range(n):
    for j in range(n):
        if i==j: continue
        solver.add(Not(And(arg_vars[i], arg_vars[j], attack_successful[i][j])))

# Self-defending: for each member A, every external attacker B must be counter-attacked by some member C
for i in range(n):  # A
    for j in range(n):  # B
        if i==j: continue
        # If B attacks A successfully and B not in extension, then need defender
        cond = And(arg_vars[i], Not(arg_vars[j]), attack_successful[j][i])
        # Defender exists?
        defenders = [And(arg_vars[k], attack_successful[k][j]) for k in range(n)]
        solver.add(Implies(cond, Or(defenders)))

# Maximality: for any argument X not in extension, either conflict with some member or there is an attacker B not in extension that cannot be defended
for i in range(n):  # X
    # conflict with some member
    conflict_with = Or([And(arg_vars[j], attack_successful[i][j]) for j in range(n)])
    conflict_by = Or([And(arg_vars[j], attack_successful[j][i]) for j in range(n)])
    conflict = Or(conflict_with, conflict_by)
    # lack of defense: exists attacker B not in extension that cannot be defended
    lack_def = Or([And(Not(arg_vars[b]), attack_successful[b][i],
                        And([Not(And(arg_vars[c], attack_successful[c][b])) for c in range(n)]))
                   for b in range(n)])
    solver.add(Implies(Not(arg_vars[i]), Or(conflict, lack_def)))

# Enumerate all maximal admissible extensions
extensions = []
while solver.check() == sat:
    m = solver.model()
    ext = [args[i] for i in range(n) if is_true(m[arg_vars[i]])]
    ext.sort()
    extensions.append(ext)
    # block this model
    block = Or([Not(arg_vars[i]) if is_true(m[arg_vars[i]]) else arg_vars[i] for i in range(n)])
    solver.add(block)

# Output
print("STATUS: sat")
print("hierarchical_stable_extensions = [")
for ext in extensions:
    print("  [" + ", ".join(f'\'{name}\'' for name in ext) + "],")
print("]")