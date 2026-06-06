from z3 import *

solver = Solver()
# Variables for positions 1..7
pos_J = Int('pos_J')
pos_K = Int('pos_K')
pos_L = Int('pos_L')
pos_M = Int('pos_M')
pos_N = Int('pos_N')
pos_O = Int('pos_O')
pos_P = Int('pos_P')
positions = [pos_J, pos_K, pos_L, pos_M, pos_N, pos_O, pos_P]
# Domain constraints
for v in positions:
    solver.add(v >= 1, v <= 7)
# All distinct
solver.add(Distinct(positions))
# Base constraints
solver.add(Or(pos_J == 6, pos_J == 7))  # J in evening
solver.add(Not(Or(pos_K == 1, pos_K == 2)))  # K not in morning
solver.add(pos_K < pos_L, pos_L < pos_M)  # L after K before M

# Helper to create constraints for an option sequence
def option_constraints(seq):
    # seq is list of house letters in order positions 1..7
    mapping = {
        'J': pos_J,
        'K': pos_K,
        'L': pos_L,
        'M': pos_M,
        'N': pos_N,
        'O': pos_O,
        'P': pos_P,
        '0': pos_O  # treat '0' as O
    }
    cons = []
    for idx, house in enumerate(seq, start=1):
        cons.append(mapping[house] == idx)
    return And(cons)

# Define each option
opt_A = option_constraints(['K','O','L','M','N','J','P'])
opt_B = option_constraints(['N','L','P','K','M','O','J'])
opt_C = option_constraints(['O','P','K','L','N','M','J'])
opt_D = option_constraints(['O','P','M','N','K','L','J'])
opt_E = option_constraints(['P','O','K','J','L','N','M'])

found_options = []
for letter, constr in [("A", opt_A), ("B", opt_B), ("C", opt_C), ("D", opt_D), ("E", opt_E)]:
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