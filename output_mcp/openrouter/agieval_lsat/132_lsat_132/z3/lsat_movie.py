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
# Helper to get time of a given movie

def time_of(movie):
    # sum of time_i * If(slot_i == movie, 1, 0)
    return Sum([If(v == movie, time_map[v], 0) for v in slots])

def screen_of(movie):
    # screen numbers: 1 for s1_7,s1_9; 2 for s2_7,s2_9; 3 for s3_8
    return Sum([If(v == movie, 1, 0) for v in [s1_7, s1_9]]) + \
           Sum([If(v == movie, 2, 0) for v in [s2_7, s2_9]]) + \
           Sum([If(v == movie, 3, 0) for v in [s3_8]])

# Constraints
# Western before horror
solver.add(time_of(W) < time_of(H))
# Sci-fi not on screen3
solver.add(s3_8 != S)
# Romance not on screen2
solver.add(s2_7 != R)
solver.add(s2_9 != R)
# Horror and mystery on different screens
solver.add(screen_of(H) != screen_of(M))

# Options definitions
options = {
    "A": (S, H),  # sci-fi, horror
    "B": (S, M),  # sci-fi, mystery
    "C": (W, H),  # western, horror
    "D": (W, M),  # western, mystery
    "E": (W, S)   # western, sci-fi
}

found_options = []
for letter, (first, second) in options.items():
    solver.push()
    solver.add(s1_7 == first)
    solver.add(s1_9 == second)
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