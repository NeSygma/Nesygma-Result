from z3 import *

solver = Solver()

# Clients: Image=0, Solide=1, Truvest=2
# Website targets and Voicemail targets for each client
W = [Int(f'W_{c}') for c in ['Image', 'Solide', 'Truvest']]
V = [Int(f'V_{c}') for c in ['Image', 'Solide', 'Truvest']]

# Domain: targets are 1, 2, or 3 days
for i in range(3):
    solver.add(And(W[i] >= 1, W[i] <= 3))
    solver.add(And(V[i] >= 1, V[i] <= 3))

# Constraint 1: Website target <= Voicemail target for each client
for i in range(3):
    solver.add(W[i] <= V[i])

# Constraint 2: Image's voicemail < Solide's voicemail AND Image's voicemail < Truvest's voicemail
solver.add(V[0] < V[1])
solver.add(V[0] < V[2])

# Constraint 3: Solide's website < Truvest's website
solver.add(W[1] < W[2])

# Additional condition: No client has voicemail target of 3 days
solver.add(V[0] != 3)
solver.add(V[1] != 3)
solver.add(V[2] != 3)

# Define the options
# (A) Image's website target is 1 day
opt_a = (W[0] == 1)
# (B) Solide's website target is 2 days
opt_b = (W[1] == 2)
# (C) Solide's voicemail target is 2 days
opt_c = (V[1] == 2)
# (D) Truvest's website target is 2 days
opt_d = (W[2] == 2)
# (E) Truvest's voicemail target is 2 days
opt_e = (V[2] == 2)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

# The question asks: which does NOT must be true?
# An option "must be true" means its negation is unsatisfiable (no model where it's false).
# The answer is the option whose negation IS satisfiable (it can be false).

must_be_true = []
can_be_false = []

for letter, constr in options:
    solver.push()
    solver.add(Not(constr))
    result = solver.check()
    if result == unsat:
        # The negation is unsat, so the option MUST be true
        must_be_true.append(letter)
    else:
        # The negation is sat, so the option can be false (does NOT must be true)
        can_be_false.append(letter)
    solver.pop()

print(f"Must be true: {must_be_true}")
print(f"Can be false (EXCEPT): {can_be_false}")

if len(can_be_false) == 1:
    print("STATUS: sat")
    print(f"answer:{can_be_false[0]}")
elif len(can_be_false) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options can be false {can_be_false}")
else:
    print("STATUS: unsat")
    print("Refine: All options must be true, no EXCEPT found")