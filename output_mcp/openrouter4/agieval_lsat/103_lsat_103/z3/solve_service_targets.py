from z3 import *

# Variables: website (w) and voicemail (v) targets for each client
# 1 = 1 day, 2 = 2 days, 3 = 3 days
I_w, I_v = Ints('I_w I_v')
S_w, S_v = Ints('S_w S_v')
T_w, T_v = Ints('T_w T_v')

all_vars = [I_w, I_v, S_w, S_v, T_w, T_v]

solver = Solver()

# Domain: 1, 2, or 3 days
for v in all_vars:
    solver.add(1 <= v, v <= 3)

# Condition 1: None of the clients can have a website target longer than its voicemail target
solver.add(I_w <= I_v)
solver.add(S_w <= S_v)
solver.add(T_w <= T_v)

# Condition 2: Image's voicemail target must be shorter than the other clients' voicemail targets
solver.add(I_v < S_v)
solver.add(I_v < T_v)

# Condition 3: Solide's website target must be shorter than Truvest's website target
solver.add(S_w < T_w)

# Additional condition from Q: None of the clients has a voicemail target of 3 days
solver.add(I_v != 3)
solver.add(S_v != 3)
solver.add(T_v != 3)

# Now test each option: we want the one that is NOT necessarily true.
# An option "must be true" if its negation leads to UNSAT.
# The "EXCEPT" answer is the one whose negation is SAT (i.e., it doesn't have to be true).

option_negations = [
    ("A", I_w != 1),   # Negation of "Image's website target is 1 day"
    ("B", S_w != 2),   # Negation of "Solide's website target is 2 days"
    ("C", S_v != 2),   # Negation of "Solide's voicemail target is 2 days"
    ("D", T_w != 2),   # Negation of "Truvest's website target is 2 days"
    ("E", T_v != 2),   # Negation of "Truvest's voicemail target is 2 days"
]

not_necessarily_true = []  # Options whose negation is SAT (not necessarily true)
necessarily_true = []      # Options whose negation is UNSAT (must be true)

for letter, neg_constr in option_negations:
    solver.push()
    solver.add(neg_constr)
    res = solver.check()
    if res == sat:
        not_necessarily_true.append(letter)
        print(f"Option {letter} negation is SAT -> not necessarily true")
    elif res == unsat:
        necessarily_true.append(letter)
        print(f"Option {letter} negation is UNSAT -> must be true")
    solver.pop()

print()
print(f"Not necessarily true: {not_necessarily_true}")
print(f"Must be true: {necessarily_true}")

# The answer is the one that is NOT necessarily true (the EXCEPT answer)
if len(not_necessarily_true) == 1:
    print(f"STATUS: sat")
    print(f"answer:{not_necessarily_true[0]}")
elif len(not_necessarily_true) == 0:
    print("STATUS: unsat")
    print("Refine: All options must be true")
else:
    print("STATUS: unsat")
    print(f"Refine: Multiple options not necessarily true: {not_necessarily_true}")