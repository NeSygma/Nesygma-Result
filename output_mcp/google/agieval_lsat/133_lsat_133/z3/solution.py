from z3 import *

# Movies: H, M, R, S, W
# Slots: 0:(1,7), 1:(1,9), 2:(2,7), 3:(2,9), 4:(3,8)
# slot_screen = [1, 1, 2, 2, 3]
# slot_time = [7, 9, 7, 9, 8]

# Use Or-loop pattern for symbolic indexing
def get_slot_screen(slot_var):
    return If(slot_var == 0, 1,
           If(slot_var == 1, 1,
           If(slot_var == 2, 2,
           If(slot_var == 3, 2, 3))))

def get_slot_time(slot_var):
    return If(slot_var == 0, 7,
           If(slot_var == 1, 9,
           If(slot_var == 2, 7,
           If(slot_var == 3, 9, 8))))

movies = ['H', 'M', 'R', 'S', 'W']
movie_slot = {m: Int(f'slot_{m}') for m in movies}

solver = Solver()

# Each movie in a unique slot
solver.add(Distinct([movie_slot[m] for m in movies]))
for m in movies:
    solver.add(movie_slot[m] >= 0, movie_slot[m] <= 4)

# Constraints
# 1. W time < H time
solver.add(get_slot_time(movie_slot['W']) < get_slot_time(movie_slot['H']))
# 2. S not on screen 3
solver.add(get_slot_screen(movie_slot['S']) != 3)
# 3. R not on screen 2
solver.add(get_slot_screen(movie_slot['R']) != 2)
# 4. H and M on different screens
solver.add(get_slot_screen(movie_slot['H']) != get_slot_screen(movie_slot['M']))

# Condition: S and R on same screen
solver.add(get_slot_screen(movie_slot['S']) == get_slot_screen(movie_slot['R']))

# Options
options = {
    "A": get_slot_time(movie_slot['W']) == 7,
    "B": get_slot_time(movie_slot['S']) == 9,
    "C": get_slot_time(movie_slot['M']) == 8,
    "D": get_slot_time(movie_slot['R']) == 9,
    "E": get_slot_time(movie_slot['H']) == 8
}

# Check which MUST be true (negation is unsat)
must_be_true = []
for letter, constr in options.items():
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        must_be_true.append(letter)
    solver.pop()

print(f"Must be true options: {must_be_true}")