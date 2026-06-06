from z3 import *

solver = Solver()

# Variables: f_L, f_M, f_S, g_L, g_M, g_S, h_L, h_M, h_S
f_L, f_M, f_S = Int('f_L'), Int('f_M'), Int('f_S')
g_L, g_M, g_S = Int('g_L'), Int('g_M'), Int('g_S')
h_L, h_M, h_S = Int('h_L'), Int('h_M'), Int('h_S')

vars_list = [f_L, f_M, f_S, g_L, g_M, g_S, h_L, h_M, h_S]

# Non-negative
for v in vars_list:
    solver.add(v >= 0)

# Total photos per section
solver.add(f_L + g_L + h_L == 2)
solver.add(f_M + g_M + h_M == 2)
solver.add(f_S + g_S + h_S == 2)

# Total photos per photographer (1 to 3)
solver.add(f_L + f_M + f_S >= 1, f_L + f_M + f_S <= 3)
solver.add(g_L + g_M + g_S >= 1, g_L + g_M + g_S <= 3)
solver.add(h_L + h_M + h_S >= 1, h_L + h_M + h_S <= 3)

# At least one photo in L must be by a photographer who has at least one photo in M
# (f_L >= 1 and f_M >= 1) or (g_L >= 1 and g_M >= 1) or (h_L >= 1 and h_M >= 1)
solver.add(Or(
    And(f_L >= 1, f_M >= 1),
    And(g_L >= 1, g_M >= 1),
    And(h_L >= 1, h_M >= 1)
))

# h_L = f_S
solver.add(h_L == f_S)

# g_S = 0
solver.add(g_S == 0)

# Options
options = [
    ("A", And(f_L == 1, f_M == 1, f_S == 1)),
    ("B", And(f_L == 1, f_M == 0, f_S == 2)),
    ("C", And(f_L == 2, f_M == 0, f_S == 1)),
    ("D", And(f_L == 0, f_M == 1, f_S == 2)),
    ("E", And(f_L == 0, f_M == 2, f_S == 1))
]

found_options = []
for letter, constr in options:
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