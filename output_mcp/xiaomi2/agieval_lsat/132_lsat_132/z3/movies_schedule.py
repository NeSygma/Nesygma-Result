from z3 import *

# 5 movies: horror(H), mystery(M), romance(R), sci-fi(S), western(W)
# Each assigned to one of 5 slots:
# Slot 1: Screen 1, 7PM  (time=7, screen=1)
# Slot 2: Screen 1, 9PM  (time=9, screen=1)
# Slot 3: Screen 2, 7PM  (time=7, screen=2)
# Slot 4: Screen 2, 9PM  (time=9, screen=2)
# Slot 5: Screen 3, 8PM  (time=8, screen=3)

H = Int('H')  # horror
M = Int('M')  # mystery
R = Int('R')  # romance
S = Int('S')  # sci-fi
W = Int('W')  # western

movies = [H, M, R, S, W]

# Time and screen lookup helpers using Or-loop pattern
def get_time(slot_var):
    """Returns a Z3 expression for the time given a slot variable"""
    return If(slot_var == 1, 7,
           If(slot_var == 2, 9,
           If(slot_var == 3, 7,
           If(slot_var == 4, 9,
           If(slot_var == 5, 8, 0)))))

def get_screen(slot_var):
    """Returns a Z3 expression for the screen given a slot variable"""
    return If(slot_var == 1, 1,
           If(slot_var == 2, 1,
           If(slot_var == 3, 2,
           If(slot_var == 4, 2,
           If(slot_var == 5, 3, 0)))))

def base_constraints():
    """Return list of base constraints"""
    cons = []
    # Each movie in a valid slot
    for m in movies:
        cons.append(And(m >= 1, m <= 5))
    # All movies in different slots
    cons.append(Distinct(H, M, R, S, W))
    
    # Constraint 1: Western begins before horror
    cons.append(get_time(W) < get_time(H))
    
    # Constraint 2: Sci-fi not on screen 3
    cons.append(get_screen(S) != 3)
    
    # Constraint 3: Romance not on screen 2
    cons.append(get_screen(R) != 2)
    
    # Constraint 4: Horror and mystery on different screens
    cons.append(get_screen(H) != get_screen(M))
    
    return cons

# Define option constraints: what it means for each answer choice
# Screen 1 has slots 1 (7PM) and 2 (9PM)
# (A) sci-fi at 7PM on screen 1, horror at 9PM on screen 1 => S=1, H=2
# (B) sci-fi at 7PM on screen 1, mystery at 9PM on screen 1 => S=1, M=2
# (C) western at 7PM on screen 1, horror at 9PM on screen 1 => W=1, H=2
# (D) western at 7PM on screen 1, mystery at 9PM on screen 1 => W=1, M=2
# (E) western at 7PM on screen 1, sci-fi at 9PM on screen 1 => W=1, S=2

options = [
    ("A", [S == 1, H == 2]),
    ("B", [S == 1, M == 2]),
    ("C", [W == 1, H == 2]),
    ("D", [W == 1, M == 2]),
    ("E", [W == 1, S == 2]),
]

found_options = []
for letter, opt_constr in options:
    solver = Solver()
    for c in base_constraints():
        solver.add(c)
    solver.add(opt_constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter}: SAT - H={m[H]}, M={m[M]}, R={m[R]}, S={m[S]}, W={m[W]}")
    elif result == unsat:
        print(f"Option {letter}: UNSAT - CANNOT be scheduled")
    else:
        print(f"Option {letter}: UNKNOWN")

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")