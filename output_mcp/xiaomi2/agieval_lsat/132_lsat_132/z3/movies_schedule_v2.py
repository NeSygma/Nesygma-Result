from z3 import *

# 5 movies assigned to 5 slots:
# Slot 1: Screen 1, 7PM
# Slot 2: Screen 1, 9PM
# Slot 3: Screen 2, 7PM
# Slot 4: Screen 2, 9PM
# Slot 5: Screen 3, 8PM

H = Int('H')  # horror
M = Int('M')  # mystery
R = Int('R')  # romance
S = Int('S')  # sci-fi
W = Int('W')  # western

movies = [H, M, R, S, W]

def get_time(slot_var):
    return If(slot_var == 1, 7,
           If(slot_var == 2, 9,
           If(slot_var == 3, 7,
           If(slot_var == 4, 9,
           If(slot_var == 5, 8, 0)))))

def get_screen(slot_var):
    return If(slot_var == 1, 1,
           If(slot_var == 2, 1,
           If(slot_var == 3, 2,
           If(slot_var == 4, 2,
           If(slot_var == 5, 3, 0)))))

def base_constraints():
    cons = []
    for m in movies:
        cons.append(And(m >= 1, m <= 5))
    cons.append(Distinct(H, M, R, S, W))
    cons.append(get_time(W) < get_time(H))       # western before horror
    cons.append(get_screen(S) != 3)               # sci-fi not screen 3
    cons.append(get_screen(R) != 2)               # romance not screen 2
    cons.append(get_screen(H) != get_screen(M))   # horror & mystery different screens
    return cons

# Answer choices: which CANNOT be screen 1's list (7PM first, 9PM second)
# (A) sci-fi at 7PM, horror at 9PM on screen 1 => S=1, H=2
# (B) sci-fi at 7PM, mystery at 9PM on screen 1 => S=1, M=2
# (C) western at 7PM, horror at 9PM on screen 1 => W=1, H=2
# (D) western at 7PM, mystery at 9PM on screen 1 => W=1, M=2
# (E) western at 7PM, sci-fi at 9PM on screen 1 => W=1, S=2

options = [
    ("A", [S == 1, H == 2]),
    ("B", [S == 1, M == 2]),
    ("C", [W == 1, H == 2]),
    ("D", [W == 1, M == 2]),
    ("E", [W == 1, S == 2]),
]

# Find which option CANNOT work (is UNSAT)
impossible_options = []
for letter, opt_constr in options:
    solver = Solver()
    for c in base_constraints():
        solver.add(c)
    solver.add(opt_constr)
    result = solver.check()
    if result == unsat:
        impossible_options.append(letter)

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")