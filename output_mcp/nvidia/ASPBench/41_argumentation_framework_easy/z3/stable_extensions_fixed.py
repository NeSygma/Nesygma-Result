from z3 import *

# Arguments: a, b, c, d, e, f
args = ['a', 'b', 'c', 'd', 'e', 'f']
# Boolean variable for each argument: True iff the argument is in the extension
in_arg = {arg: Bool(f'in_{arg}') for arg in args}

# Attack relation: attacker -> list of attacked arguments
attacks = {
    'a': ['b'],
    'b': ['c', 'f'],
    'c': ['d'],
    'd': ['e'],
    'e': ['f'],
    'f': ['a']
}

# Compute attackers of each argument (who attacks it)
attackers = {arg: [] for arg in args}
for attacker, targets in attacks.items():
    for target in targets:
        attackers[target].append(attacker)

solver = Solver()

# 1. Conflict‑free: no argument attacks another inside the extension
for x, targets in attacks.items():
    for y in targets:
        # not (x in extension and y in extension)
        solver.add(Not(And(in_arg[x], in_arg[y])))

# 2. Self‑defending: if x is in the extension, every attacker of x must be attacked
# by some argument in the extension.
for x in args:
    for y in attackers[x]:
        # defenders_of_y = arguments that attack y (i.e., attackers[y])
        defenders_of_y = attackers[y]
        if defenders_of_y:
            # at least one defender is in the extension
            solver.add(Implies(in_arg[x], Or([in_arg[z] for z in defenders_of_y])))
        else:
            # no defender exists, so x cannot be in the extension
            solver.add(Implies(in_arg[x], False))

# 3. Maximality: every argument not in the extension must be attacked by some argument in it
for w in args:
    attackers_of_w = attackers[w]
    if attackers_of_w:
        # if w is not in the extension, some attacker of w must be in the extension
        solver.add(Implies(Not(in_arg[w]), Or([in_arg[v] for v in attackers_of_w])))
    else:
        # w has no attackers, so it must be in the extension to satisfy maximality
        solver.add(Implies(Not(in_arg[w]), False))

# Enumerate all stable extensions
while True:
    result = solver.check()
    if result != sat:
        break
    model = solver.model()
    # Collect arguments that are True in the model
    extension = [arg for arg in args if bool(model[in_arg[arg]])]
    # Output the found stable extension
    print("STATUS: sat")
    print("extension:", extension)
    # Block this extension to find the next one
    block = Or([in_arg[arg] != model[in_arg[arg]] for arg in args])
    solver.add(block)

# Indicate that no more extensions exist
print("STATUS: unknown")