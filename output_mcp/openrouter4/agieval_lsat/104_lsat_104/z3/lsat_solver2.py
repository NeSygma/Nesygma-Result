from z3 import *

# Clients: 0=Image, 1=Solide, 2=Truvest
# Domain: 1, 2, or 3 days

W = [Int(f'W_{i}') for i in range(3)]  # website targets
V = [Int(f'V_{i}') for i in range(3)]  # voicemail targets

solver = Solver()

# Domain constraints: 1, 2, or 3
for i in range(3):
    solver.add(Or(W[i] == 1, W[i] == 2, W[i] == 3))
    solver.add(Or(V[i] == 1, V[i] == 2, V[i] == 3))

# Condition 1: For each client, website <= voicemail
for i in range(3):
    solver.add(W[i] <= V[i])

# Condition 2: Image's voicemail < Solide's voicemail AND Image's voicemail < Truvest's voicemail
solver.add(V[0] < V[1])
solver.add(V[0] < V[2])

# Condition 3: Solide's website < Truvest's website
solver.add(W[1] < W[2])

# Additional condition from Q: Truvest's website < Truvest's voicemail
solver.add(W[2] < V[2])

# Now we need to find which option MUST be true.
# We check: adding Not(option) makes the system unsat => option must be true.
# But we must also check that the base premises are satisfiable (they are).

# First, verify base is sat
solver_base = Solver()
for i in range(3):
    solver_base.add(Or(W[i] == 1, W[i] == 2, W[i] == 3))
    solver_base.add(Or(V[i] == 1, V[i] == 2, V[i] == 3))
for i in range(3):
    solver_base.add(W[i] <= V[i])
solver_base.add(V[0] < V[1])
solver_base.add(V[0] < V[2])
solver_base.add(W[1] < W[2])
solver_base.add(W[2] < V[2])
print("Base check:", solver_base.check())
if solver_base.check() == sat:
    m = solver_base.model()
    for i in range(3):
        print(f"W[{i}] = {m[W[i]]}, V[{i}] = {m[V[i]]}")

# Now check each option's negation
found_options = []
for letter, not_constr in [("A", Not(V[0] == 2)), ("B", Not(W[0] == 2)), ("C", Not(W[0] == 1)), ("D", Not(W[1] == 2)), ("E", Not(W[1] == 1))]:
    s = Solver()
    # Add all base constraints
    for i in range(3):
        s.add(Or(W[i] == 1, W[i] == 2, W[i] == 3))
        s.add(Or(V[i] == 1, V[i] == 2, V[i] == 3))
    for i in range(3):
        s.add(W[i] <= V[i])
    s.add(V[0] < V[1])
    s.add(V[0] < V[2])
    s.add(W[1] < W[2])
    s.add(W[2] < V[2])
    s.add(not_constr)
    res = s.check()
    print(f"Not({letter}): {res}")
    if res == unsat:
        found_options.append(letter)

print(f"Options that must be true: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")