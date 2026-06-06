from z3 import *

# Variables: position (1-6) for each instrument
G = Int('G')  # guitarist
K = Int('K')  # keyboard player
P = Int('P')  # percussionist
S = Int('S')  # saxophonist
T = Int('T')  # trumpeter
V = Int('V')  # violinist

instruments = [G, K, P, S, T, V]

solver = Solver()

# Each performs exactly one solo, positions 1-6, all distinct
for inst in instruments:
    solver.add(inst >= 1, inst <= 6)
solver.add(Distinct(instruments))

# Constraint 1: The guitarist does not perform the fourth solo
solver.add(G != 4)

# Constraint 2: The percussionist performs a solo at some time before the keyboard player does
solver.add(P < K)

# Constraint 3: The keyboard player performs a solo at some time after the violinist does
# and at some time before the guitarist does
solver.add(V < K)
solver.add(K < G)

# Constraint 4: The saxophonist performs a solo at some time after either the percussionist
# does or the trumpeter does, but not both
# "after P or after T, but not both" means:
# (S > P XOR S > T)
solver.add(Xor(S > P, S > T))

# Now test each option: which CANNOT perform the third solo?
# We check if each instrument CAN be at position 3. If sat, it CAN. If unsat, it CANNOT.

found_options = []

# Option A: guitarist performs third
opt_a_constr = (G == 3)
# Option B: keyboard player performs third
opt_b_constr = (K == 3)
# Option C: saxophonist performs third
opt_c_constr = (S == 3)
# Option D: trumpeter performs third
opt_d_constr = (T == 3)
# Option E: violinist performs third
opt_e_constr = (V == 3)

for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} (position 3) is SAT: G={m[G]}, K={m[K]}, P={m[P]}, S={m[S]}, T={m[T]}, V={m[V]}")
    else:
        print(f"Option {letter} (position 3) is UNSAT - CANNOT perform third")
    solver.pop()

print()
print(f"Options that CAN perform third: {found_options}")
print(f"Options that CANNOT perform third: {[l for l in ['A','B','C','D','E'] if l not in found_options]}")

# The question asks which CANNOT perform the third solo
# We need exactly one option that CANNOT
cannot_options = [l for l in ['A','B','C','D','E'] if l not in found_options]

if len(cannot_options) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_options[0]}")
elif len(cannot_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple CANNOT options found {cannot_options}")
else:
    print("STATUS: unsat")
    print("Refine: No CANNOT options found - all can perform third")