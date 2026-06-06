from z3 import *

# Movies
movies = ['H', 'M', 'R', 'S', 'W']
# Slots: 0:S1_7, 1:S1_9, 2:S2_7, 3:S2_9, 4:S3_8
# Times: 0:7, 1:9, 2:7, 3:9, 4:8
# Screens: 0:1, 1:1, 2:2, 3:2, 4:3

slot_time = [7, 9, 7, 9, 8]
slot_screen = [1, 1, 2, 2, 3]

# Variables: pos[movie] = slot index
pos = {m: Int(f'pos_{m}') for m in movies}

solver = Solver()

# Each movie in exactly one slot
solver.add(Distinct([pos[m] for m in movies]))
for m in movies:
    solver.add(pos[m] >= 0, pos[m] <= 4)

# Conditions
# 1. Western begins before Horror
# W_time < H_time
# We need to map pos to time
def get_time(p):
    return If(p == 0, 7, If(p == 1, 9, If(p == 2, 7, If(p == 3, 9, 8))))

def get_screen(p):
    return If(p == 0, 1, If(p == 1, 1, If(p == 2, 2, If(p == 3, 2, 3))))

solver.add(get_time(pos['W']) < get_time(pos['H']))

# 2. Sci-Fi not on screen 3
solver.add(get_screen(pos['S']) != 3)

# 3. Romance not on screen 2
solver.add(get_screen(pos['R']) != 2)

# 4. Horror and Mystery on different screens
solver.add(get_screen(pos['H']) != get_screen(pos['M']))

# Options: Screen 2 is slots 2 (7 PM) and 3 (9 PM)
# Option A: (S, H) -> pos[S]=2, pos[H]=3
# Option B: (S, M) -> pos[S]=2, pos[M]=3
# Option C: (S, W) -> pos[S]=2, pos[W]=3
# Option D: (W, H) -> pos[W]=2, pos[H]=3
# Option E: (W, M) -> pos[W]=2, pos[M]=3

options = [
    ("A", And(pos['S'] == 2, pos['H'] == 3)),
    ("B", And(pos['S'] == 2, pos['M'] == 3)),
    ("C", And(pos['S'] == 2, pos['W'] == 3)),
    ("D", And(pos['W'] == 2, pos['H'] == 3)),
    ("E", And(pos['W'] == 2, pos['M'] == 3))
]

# We want to find which one CANNOT be true.
# So we check which options are SAT. The one that is UNSAT is the answer.
# Wait, the prompt asks for the one that CANNOT be true.
# So I should look for the option that is UNSAT.

possible_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        possible_options.append(letter)
    solver.pop()

# The question asks for the one that CANNOT be true.
# So we are looking for the option that is NOT in possible_options.
# Let's list all options and see which one is missing.
all_options = ["A", "B", "C", "D", "E"]
cannot_be_true = [opt for opt in all_options if opt not in possible_options]

print(f"Possible options: {possible_options}")
print(f"Cannot be true: {cannot_be_true}")

if len(cannot_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_be_true[0]}")
else:
    print("STATUS: unsat")