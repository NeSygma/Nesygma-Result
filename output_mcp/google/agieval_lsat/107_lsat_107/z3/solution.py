from z3 import *

# Variables
# I_W, I_V, S_W, S_V, T_W, T_V
I_W, I_V = Int('I_W'), Int('I_V')
S_W, S_V = Int('S_W'), Int('S_V')
T_W, T_V = Int('T_W'), Int('T_V')

vars = [I_W, I_V, S_W, S_V, T_W, T_V]

solver = Solver()

# Constraints
for v in vars:
    solver.add(v >= 1, v <= 3)

solver.add(I_W <= I_V)
solver.add(S_W <= S_V)
solver.add(T_W <= T_V)
solver.add(I_V < S_V)
solver.add(I_V < T_V)
solver.add(S_W < T_W)

# Options:
# (A) 1-day website target: Can two clients have W=1?
# (B) 2-day voicemail target: Can two clients have V=2?
# (C) 2-day website target: Can two clients have W=2?
# (D) 3-day voicemail target: Can two clients have V=3?
# (E) 3-day website target: Can two clients have W=3?

def can_two_have_target(target_type, target_val):
    # target_type: 'W' or 'V'
    # target_val: 1, 2, or 3
    s = Solver()
    s.add(solver.assertions())
    
    # Define the condition: at least two clients have the target
    # Clients: I, S, T
    if target_type == 'W':
        c1 = (I_W == target_val)
        c2 = (S_W == target_val)
        c3 = (T_W == target_val)
    else:
        c1 = (I_V == target_val)
        c2 = (S_V == target_val)
        c3 = (T_V == target_val)
        
    s.add(Or(And(c1, c2), And(c1, c3), And(c2, c3)))
    return s.check() == sat

options = [
    ("A", 'W', 1),
    ("B", 'V', 2),
    ("C", 'W', 2),
    ("D", 'V', 3),
    ("E", 'W', 3)
]

results = []
for label, t_type, t_val in options:
    if not can_two_have_target(t_type, t_val):
        results.append(label)

if len(results) == 1:
    print("STATUS: sat")
    print(f"answer:{results[0]}")
elif len(results) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {results}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")