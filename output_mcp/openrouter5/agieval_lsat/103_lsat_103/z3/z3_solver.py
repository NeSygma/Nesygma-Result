from z3 import *

# Clients: Image (I), Solide (S), Truvest (T)
# Targets: 1 day, 2 days, 3 days
# For each client: website target (w) and voicemail target (v)

# Variables: I_w, I_v, S_w, S_v, T_w, T_v
I_w, I_v, S_w, S_v, T_w, T_v = Ints('I_w I_v S_w S_v T_w T_v')

solver = Solver()

# Domain: each target is 1, 2, or 3
for var in [I_w, I_v, S_w, S_v, T_w, T_v]:
    solver.add(Or(var == 1, var == 2, var == 3))

# Condition 1: None of the clients can have a website target that is longer than its voicemail target.
# i.e., website <= voicemail for each client
solver.add(I_w <= I_v)
solver.add(S_w <= S_v)
solver.add(T_w <= T_v)

# Condition 2: Image's voicemail target must be shorter than the other clients' voicemail targets.
# i.e., I_v < S_v and I_v < T_v
solver.add(I_v < S_v)
solver.add(I_v < T_v)

# Condition 3: Solide's website target must be shorter than Truvest's website target.
# i.e., S_w < T_w
solver.add(S_w < T_w)

# Additional condition from the question: None of the clients has a voicemail target of 3 days.
# So I_v != 3, S_v != 3, T_v != 3
solver.add(I_v != 3)
solver.add(S_v != 3)
solver.add(T_v != 3)

# Now evaluate each option as "must be true" under these constraints.
# We need to find which option is NOT necessarily true.
# So we check: is the negation of the option satisfiable?
# If the negation is satisfiable, then the option is NOT necessarily true (it could be false).
# If the negation is unsat, then the option MUST be true.

# Option A: Image's website target is 1 day. (I_w == 1)
# Option B: Solide's website target is 2 days. (S_w == 2)
# Option C: Solide's voicemail target is 2 days. (S_v == 2)
# Option D: Truvest's website target is 2 days. (T_w == 2)
# Option E: Truvest's voicemail target is 2 days. (T_v == 2)

# We want the one that is NOT necessarily true.
# So we check each: if Not(option) is sat, then option is not necessarily true.

options = [
    ("A", I_w == 1),
    ("B", S_w == 2),
    ("C", S_v == 2),
    ("D", T_w == 2),
    ("E", T_v == 2)
]

not_necessarily_true = []
for letter, constr in options:
    solver.push()
    solver.add(Not(constr))  # Can the option be false?
    if solver.check() == sat:
        not_necessarily_true.append(letter)
    solver.pop()

# The question asks: "each of the following must be true EXCEPT"
# So we want the option(s) that are NOT necessarily true.
# If exactly one option is not necessarily true, that's our answer.

if len(not_necessarily_true) == 1:
    print("STATUS: sat")
    print(f"answer:{not_necessarily_true[0]}")
elif len(not_necessarily_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {not_necessarily_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")