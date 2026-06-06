from z3 import *

# Define arguments and attacks
arguments = ['a','b','c','d','e','f']
attacks = [('a','b'),('b','c'),('c','d'),('d','e'),('e','f'),('f','a'),('b','f'),('d','b')]

# Boolean variable for each argument: True if in the extension
inS = {arg: Bool(arg) for arg in arguments}

solver = Solver()

# Conflict-free: no two arguments in the extension attack each other
for (x,y) in attacks:
    solver.add(Not(And(inS[x], inS[y])))

# Compute attackers for each argument
attackers_of = {arg: [] for arg in arguments}
for (attacker, target) in attacks:
    attackers_of[target].append(attacker)

# Self-defending: for each argument in the extension, all its attackers must be attacked by some argument in the extension
for x in arguments:
    for attacker in attackers_of[x]:
        # attackers_of[attacker] may be empty
        if attackers_of[attacker]:
            solver.add(Implies(inS[x], Or([inS[z] for z in attackers_of[attacker]])))
        else:
            # If attacker has no attackers, x cannot be in the extension
            solver.add(Implies(inS[x], False))

# Maximality: every argument not in the extension must be attacked by some argument in the extension
for y in arguments:
    if attackers_of[y]:
        solver.add(Implies(Not(inS[y]), Or([inS[z] for z in attackers_of[y]])))
    else:
        # If y has no attackers, it must be in the extension
        solver.add(inS[y])

# Enumerate all stable extensions
extensions = []
while solver.check() == sat:
    m = solver.model()
    ext = [arg for arg in arguments if is_true(m.eval(inS[arg], model_completion=True))]
    extensions.append(ext)
    # Block this model
    solver.add(Or([inS[arg] != m.eval(inS[arg], model_completion=True) for arg in arguments]))

if extensions:
    print("STATUS: sat")
    print("stable_extensions:", extensions)
else:
    print("STATUS: unsat")
    print("stable_extensions:", extensions)