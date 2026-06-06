from z3 import *

solver = Solver()

# Variables
H, L, M, S, T, V = Ints('H L M S T V')

# Base constraints
solver.add(Distinct([H, L, M, S, T, V]))
solver.add(H >= 0, H <= 5)
solver.add(L >= 0, L <= 5)
solver.add(M >= 0, M <= 5)
solver.add(S >= 0, S <= 5)
solver.add(T >= 0, T <= 5)
solver.add(V >= 0, V <= 5)

# Condition: sundial not on June 1st (S != 0)
solver.add(S != 0)

# If harmonica earlier than lamp then mirror earlier than lamp
solver.add(Implies(H < L, M < L))

# Sundial earlier than mirror and earlier than vase
solver.add(S < M)
solver.add(S < V)

# Table earlier than harmonica OR earlier than vase, but not both
solver.add(Or(T < H, T < V))
solver.add(Not(And(T < H, T < V)))

# Define option constraints
opt_a_constr = And(T == 1, L == 2)  # Table June 2 (1), Lamp June 3 (2)
opt_b_constr = And(S == 1, V == 2)  # Sundial June 2 (1), Vase June 3 (2)
opt_c_constr = And(M == 2, S == 3)  # Mirror June 3 (2), Sundial June 4 (3)
opt_d_constr = And(V == 3, S == 4)  # Vase June 4 (3), Sundial June 5 (4)
opt_e_constr = And(S == 3, T == 4)  # Sundial June 4 (3), Table June 5 (4)

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