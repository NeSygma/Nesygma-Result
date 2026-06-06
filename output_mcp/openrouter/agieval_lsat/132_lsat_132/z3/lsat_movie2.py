from z3 import *

# Movie indices
H, M, R, S, W = range(5)

# Slot variables
s1_7 = Int('s1_7')
s1_9 = Int('s1_9')
s2_7 = Int('s2_7')
s2_9 = Int('s2_9')
s3_8 = Int('s3_8')
slots = [s1_7, s1_9, s2_7, s2_9, s3_8]

solver = Solver()
# All slots distinct and each in 0..4
for v in slots:
    solver.add(v >= 0, v <= 4)
solver.add(Distinct(slots))

# Times for each slot
time_map = {s1_7:7, s1_9:9, s2_7:7, s2_9:9, s3_8:8}

def time_of(movie):
    return Sum([If(v == movie, time_map[v], 0) for v in slots])

def screen_of(movie):
    # screen 1 if in s1_7 or s1_9, screen 2 if in s2_7 or s2_9, else 3
    return Sum([If(v == movie, 1, 0) for v in [s1_7, s1_9]]) + \
           Sum([If(v == movie, 2, 0) for v in [s2_7, s2_9]]) + \
           Sum([If(v == movie, 3, 0) for v in [s3_8]])

# Base constraints
solver.add(time_of(W) < time_of(H))          # western before horror
solver.add(s3_8 != S)                        # sci-fi not on screen3
solver.add(s2_7 != R, s2_9 != R)             # romance not on screen2
solver.add(screen_of(H) != screen_of(M))     # horror and mystery different screens

# Options: each is a pair (first at 7pm, second at 9pm) on screen1
options = {
    "A": (S, H),
    "B": (S, M),
    "C": (W, H),
    "D": (W, M),
    "E": (W, S)
}

cannot_options = []
for letter, (first, second) in options.items():
    solver.push()
    solver.add(s1_7 == first)
    solver.add(s1_9 == second)
    if solver.check() == unsat:
        cannot_options.append(letter)
    solver.pop()

if len(cannot_options) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_options[0]}")
elif len(cannot_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple cannot options {cannot_options}")
else:
    print("STATUS: unsat")
    print("Refine: No cannot options found")