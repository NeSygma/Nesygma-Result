from z3 import *

# Define members
G = Int('G')  # guitarist
K = Int('K')  # keyboard
P = Int('P')  # percussionist
S = Int('S')  # saxophonist
T = Int('T')  # trumpeter
V = Int('V')  # violinist

solver = Solver()
# Domain constraints: positions 1..6
members = [G, K, P, S, T, V]
for m in members:
    solver.add(m >= 1, m <= 6)
# All distinct
solver.add(Distinct(members))
# Base constraints
# 1. Guitarist not at position 4
solver.add(G != 4)
# 2. Percussionist before Keyboard
solver.add(P < K)
# 3. Keyboard after Violinist and before Guitarist
solver.add(V < K, K < G)
# 4. Saxophonist after either Percussionist or Trumpeter, but not both (XOR)
cond1 = S > P
cond2 = S > T
solver.add(Xor(cond1, cond2))

# Define option constraints based on ordering strings
# Helper to create constraints from a list of members in order
def ordering_constraint(order_list):
    # order_list is list of symbols in order positions 1..6
    mapping = {
        'guitarist': G,
        'keyboard': K,
        'percussionist': P,
        'saxophonist': S,
        'trumpeter': T,
        'violinist': V
    }
    cons = []
    for pos, name in enumerate(order_list, start=1):
        cons.append(mapping[name] == pos)
    return And(cons)

# Options
opt_a_constr = ordering_constraint(['violinist','percussionist','saxophonist','guitarist','trumpeter','keyboard'])
opt_b_constr = ordering_constraint(['percussionist','violinist','keyboard','trumpeter','saxophonist','guitarist'])
opt_c_constr = ordering_constraint(['violinist','trumpeter','saxophonist','percussionist','keyboard','guitarist'])
opt_d_constr = ordering_constraint(['keyboard','trumpeter','violinist','saxophonist','guitarist','percussionist'])
opt_e_constr = ordering_constraint(['guitarist','violinist','keyboard','percussionist','saxophonist','trumpeter'])

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