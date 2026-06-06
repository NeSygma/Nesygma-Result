from z3 import *

solver = Solver()

# Define variables for positions of each singer
K = Int('K')  # Kammer
L = Int('L')  # Lugo
T = Int('T')  # Trillo
W = Int('W')  # Waite
Y = Int('Y')  # Yoshida
Z = Int('Z')  # Zinn

# Domain constraints: positions from 1 to 6
solver.add(K >= 1, K <= 6)
solver.add(L >= 1, L <= 6)
solver.add(T >= 1, T <= 6)
solver.add(W >= 1, W <= 6)
solver.add(Y >= 1, Y <= 6)
solver.add(Z >= 1, Z <= 6)

# All positions distinct
solver.add(Distinct([K, L, T, W, Y, Z]))

# Base constraints from problem statement
# 1. The fourth audition cannot be recorded (recorded are K and L)
solver.add(K != 4)
solver.add(L != 4)

# 2. The fifth audition must be recorded (so either K or L at position 5)
solver.add(Or(K == 5, L == 5))

# 3. Waite's audition must take place earlier than the two recorded auditions (K and L)
solver.add(W < K)
solver.add(W < L)

# 4. Kammer's audition must take place earlier than Trillo's audition
solver.add(K < T)

# 5. Zinn's audition must take place earlier than Yoshida's audition
solver.add(Z < Y)

# Now define the options as specific orderings
# Option A: Kammer, Trillo, Zinn, Waite, Lugo, Yoshida
opt_a = And(K == 1, T == 2, Z == 3, W == 4, L == 5, Y == 6)

# Option B: Waite, Kammer, Yoshida, Zinn, Lugo, Trillo
opt_b = And(W == 1, K == 2, Y == 3, Z == 4, L == 5, T == 6)

# Option C: Waite, Lugo, Kammer, Trillo, Zinn, Yoshida
opt_c = And(W == 1, L == 2, K == 3, T == 4, Z == 5, Y == 6)

# Option D: Waite, Zinn, Kammer, Trillo, Lugo, Yoshida
opt_d = And(W == 1, Z == 2, K == 3, T == 4, L == 5, Y == 6)

# Option E: Zinn, Yoshida, Waite, Lugo, Kammer, Trillo
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