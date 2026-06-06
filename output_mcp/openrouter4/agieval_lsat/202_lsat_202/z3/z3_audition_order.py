from z3 import *

solver = Solver()

# Variables: position of each singer (1 to 6)
K, L, T, W, Y, Z = Ints('K L T W Y Z')
names = [K, L, T, W, Y, Z]

# Domain: positions 1-6, all distinct
for n in names:
    solver.add(n >= 1, n <= 6)
solver.add(Distinct(names))

# Recorded: Kammer and Lugo
# Fourth audition cannot be recorded: position 4 is not K and not L
solver.add(K != 4)
solver.add(L != 4)

# Fifth audition must be recorded: position 5 is either K or L
solver.add(Or(K == 5, L == 5))

# Waite's audition earlier than the two recorded auditions
solver.add(W < K)
solver.add(W < L)

# Kammer earlier than Trillo
solver.add(K < T)

# Zinn earlier than Yoshida
solver.add(Z < Y)

# Options
option_a = And(K == 1, T == 2, Z == 3, W == 4, L == 5, Y == 6)
option_b = And(W == 1, K == 2, Y == 3, Z == 4, L == 5, T == 6)
option_c = And(W == 1, L == 2, K == 3, T == 4, Z == 5, Y == 6)
option_d = And(W == 1, Z == 2, K == 3, T == 4, L == 5, Y == 6)
option_e = And(Z == 1, Y == 2, W == 3, L == 4, K == 5, T == 6)

found_options = []
for letter, constr in [("A", option_a), ("B", option_b), ("C", option_c), ("D", option_d), ("E", option_e)]:
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