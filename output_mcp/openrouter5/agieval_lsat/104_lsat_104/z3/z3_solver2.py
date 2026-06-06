from z3 import *

# We have 3 clients: Image, Solide, Truvest
# For each client, two targets: website and voicemail
# Targets are 1, 2, or 3 days (1 = shortest, 3 = longest)

I_w, I_v = Ints('I_w I_v')  # Image website, Image voicemail
S_w, S_v = Ints('S_w S_v')  # Solide website, Solide voicemail
T_w, T_v = Ints('T_w T_v')  # Truvest website, Truvest voicemail

solver = Solver()

# Domain constraints: each target is 1, 2, or 3 days
for var in [I_w, I_v, S_w, S_v, T_w, T_v]:
    solver.add(Or(var == 1, var == 2, var == 3))

# Condition 1: None of the clients can have a website target that is longer than its voicemail target.
# So website <= voicemail for each client
solver.add(I_w <= I_v)
solver.add(S_w <= S_v)
solver.add(T_w <= T_v)

# Condition 2: Image's voicemail target must be shorter than the other clients' voicemail targets.
# I_v < S_v and I_v < T_v
solver.add(I_v < S_v)
solver.add(I_v < T_v)

# Condition 3: Solide's website target must be shorter than Truvest's website target.
# S_w < T_w
solver.add(S_w < T_w)

# Additional condition from the question: Truvest's website target is shorter than its voicemail target.
# T_w < T_v
solver.add(T_w < T_v)

# Now use the multiple choice skeleton
# Each option is a constraint that we test for satisfiability WITHIN the base constraints
found_options = []
for letter, constr in [("A", I_v == 2), ("B", I_w == 2), ("C", I_w == 1), ("D", S_w == 2), ("E", S_w == 1)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")