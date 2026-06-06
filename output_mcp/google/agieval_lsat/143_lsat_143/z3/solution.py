from z3 import *

# Members: G, K, P, S, T, V
# Positions: 1, 2, 3, 4, 5, 6
# Each member has a unique position.

members = ['G', 'K', 'P', 'S', 'T', 'V']
pos = {m: Int(m) for m in members}

solver = Solver()

# Each member performs exactly one solo (1-6)
for m in members:
    solver.add(pos[m] >= 1, pos[m] <= 6)
solver.add(Distinct([pos[m] for m in members]))

# Constraints:
# 1. The guitarist does not perform the fourth solo.
solver.add(pos['G'] != 4)
# 2. The percussionist performs a solo at some time before the keyboard player does.
solver.add(pos['P'] < pos['K'])
# 3. The keyboard player performs a solo at some time after the violinist does and at some time before the guitarist does.
solver.add(pos['V'] < pos['K'])
solver.add(pos['K'] < pos['G'])
# 4. The saxophonist performs a solo at some time after either the percussionist does or the trumpeter does, but not both.
# (S > P XOR S > T)
# This is equivalent to (S > P and S <= T) OR (S <= P and S > T)
solver.add(Or(
    And(pos['S'] > pos['P'], pos['S'] <= pos['T']),
    And(pos['S'] <= pos['P'], pos['S'] > pos['T'])
))

# Condition: The violinist performs the fourth solo.
solver.add(pos['V'] == 4)

# Options:
# (A) The percussionist performs a solo at some time before the violinist does. (P < V)
# (B) The trumpeter performs a solo at some time before the violinist does. (T < V)
# (C) The trumpeter performs a solo at some time before the guitarist does. (T < G)
# (D) The saxophonist performs a solo at some time before the violinist does. (S < V)
# (E) The trumpeter performs a solo at some time before the saxophonist does. (T < S)

# We want to find the option that is NOT necessarily true.
# An option O is necessarily true if Not(O) is unsatisfiable.
# We are looking for an option O such that Not(O) is satisfiable.

options = {
    "A": pos['P'] < pos['V'],
    "B": pos['T'] < pos['V'],
    "C": pos['T'] < pos['G'],
    "D": pos['S'] < pos['V'],
    "E": pos['T'] < pos['S']
}

found_options = []
for letter, constr in options.items():
    solver.push()
    # We want to check if the option is NOT necessarily true.
    # This means there exists a case where the option is false.
    solver.add(Not(constr))
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