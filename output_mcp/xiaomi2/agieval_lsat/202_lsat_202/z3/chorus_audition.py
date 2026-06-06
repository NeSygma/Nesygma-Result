from z3 import *

solver = Solver()

# Six singers, positions 1-6
K = Int('K')  # Kammer
L = Int('L')  # Lugo
T = Int('T')  # Trillo
W = Int('W')  # Waite
Y = Int('Y')  # Yoshida
Z = Int('Z')  # Zinn

singers = [K, L, T, W, Y, Z]
names = ['Kammer', 'Lugo', 'Trillo', 'Waite', 'Yoshida', 'Zinn']

# All positions 1-6, all distinct
for s in singers:
    solver.add(s >= 1, s <= 6)
solver.add(Distinct(singers))

# Recorded singers: Kammer and Lugo
# Not recorded: Trillo, Waite, Yoshida, Zinn

# Condition 1: Fourth audition cannot be recorded
# So position 4 is NOT Kammer and NOT Lugo
solver.add(K != 4)
solver.add(L != 4)

# Condition 2: Fifth audition must be recorded
# So position 5 IS Kammer OR Lugo
solver.add(Or(K == 5, L == 5))

# Condition 3: Waite earlier than both recorded auditions (Kammer and Lugo)
solver.add(W < K)
solver.add(W < L)

# Condition 4: Kammer earlier than Trillo
solver.add(K < T)

# Condition 5: Zinn earlier than Yoshida
solver.add(Z < Y)

# Now check each answer choice
# (A) Kammer, Trillo, Zinn, Waite, Lugo, Yoshida
opt_a = And(K == 1, T == 2, Z == 3, W == 4, L == 5, Y == 6)
# (B) Waite, Kammer, Yoshida, Zinn, Lugo, Trillo
opt_b = And(W == 1, K == 2, Y == 3, Z == 4, L == 5, T == 6)
# (C) Waite, Lugo, Kammer, Trillo, Zinn, Yoshida
opt_c = And(W == 1, L == 2, K == 3, T == 4, Z == 5, Y == 6)
# (D) Waite, Zinn, Kammer, Trillo, Lugo, Yoshida
opt_d = And(W == 1, Z == 2, K == 3, T == 4, L == 5, Y == 6)
# (E) Zinn, Yoshida, Waite, Lugo, Kammer, Trillo
opt_e = And(Z == 1, Y == 2, W == 3, L == 4, K == 5, T == 6)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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