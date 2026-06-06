from z3 import *

solver = Solver()
# Variables
W_I = Int('W_I')
V_I = Int('V_I')
W_S = Int('W_S')
V_S = Int('V_S')
W_T = Int('W_T')
V_T = Int('V_T')
vars = [W_I, V_I, W_S, V_S, W_T, V_T]
# Domain constraints 1..3
for v in vars:
    solver.add(v >= 1, v <= 3)
# Website <= voicemail for each client
solver.add(W_I <= V_I)
solver.add(W_S <= V_S)
solver.add(W_T <= V_T)
# Image voicemail shorter than others
solver.add(V_I < V_S)
solver.add(V_I < V_T)
# Solide website shorter than Truvest website
solver.add(W_S < W_T)
# Additional condition: Truvest website shorter than its voicemail
solver.add(W_T < V_T)

# Option constraints
opt_a = V_I == 2
opt_b = W_I == 2
opt_c = W_I == 1
opt_d = W_S == 2
opt_e = W_S == 1

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