from z3 import *

solver = Solver()

# Variables for days (1..6)
H, L, M, S, T, V = Ints('H L M S T V')

# Domain constraints: each day between 1 and 6
solver.add(1 <= H, H <= 6)
solver.add(1 <= L, L <= 6)
solver.add(1 <= M, M <= 6)
solver.add(1 <= S, S <= 6)
solver.add(1 <= T, T <= 6)
solver.add(1 <= V, V <= 6)

# All different
solver.add(Distinct([H, L, M, S, T, V]))

# Base constraints from problem
# 1. Sundial not on June 1st
solver.add(S != 1)

# 2. If harmonica earlier than lamp, then mirror earlier than lamp
solver.add(Implies(H < L, M < L))

# 3. Sundial earlier than mirror and vase
solver.add(S < M)
solver.add(S < V)

# 4. Table earlier than harmonica XOR vase (exclusive or)
solver.add(Xor(T < H, T < V))

# Additional condition from the question: table later than both mirror and vase
solver.add(T > M)
solver.add(T > V)

# Answer choices as constraints
opt_a_constr = (H < T)          # (A) harmonica earlier than table
opt_b_constr = (T < L)          # (B) table earlier than lamp
opt_c_constr = (T < S)          # (C) table earlier than sundial
opt_d_constr = (M < V)          # (D) mirror earlier than vase
opt_e_constr = (S < L)          # (E) sundial earlier than lamp

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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