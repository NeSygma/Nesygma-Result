from z3 import *

solver = Solver()

# Movies: horror=0, mystery=1, romance=2, sci-fi=3, western=4
movies = ['horror', 'mystery', 'romance', 'sci-fi', 'western']
HORROR, MYSTERY, ROMANCE, SCIFI, WESTERN = range(5)

# Valid slots: (screen, time)
# 0: (1,7), 1: (1,9), 2: (2,7), 3: (2,9), 4: (3,8)
# screen_of and time_of for each slot index
slot_screen = [1, 1, 2, 2, 3]
slot_time = [7, 9, 7, 9, 8]

# Each movie assigned to a slot (0-4)
assign = [Int(f'assign_{m}') for m in movies]

# Each movie must be in a valid slot
for m in range(5):
    solver.add(assign[m] >= 0, assign[m] <= 4)

# All movies in distinct slots
solver.add(Distinct(assign))

# Helper: get screen and time for a movie using Or-loop pattern
def get_screen(movie_idx):
    """Returns Z3 expression for the screen of a movie"""
    return If(assign[movie_idx] == 0, 1,
           If(assign[movie_idx] == 1, 1,
           If(assign[movie_idx] == 2, 2,
           If(assign[movie_idx] == 3, 2,
           3))))

def get_time(movie_idx):
    """Returns Z3 expression for the time of a movie"""
    return If(assign[movie_idx] == 0, 7,
           If(assign[movie_idx] == 1, 9,
           If(assign[movie_idx] == 2, 7,
           If(assign[movie_idx] == 3, 9,
           8))))

screen = [get_screen(i) for i in range(5)]
time = [get_time(i) for i in range(5)]

# Constraint 1: Western begins before horror
solver.add(time[WESTERN] < time[HORROR])

# Constraint 2: Sci-fi not on screen 3
solver.add(screen[SCIFI] != 3)

# Constraint 3: Romance not on screen 2
solver.add(screen[ROMANCE] != 2)

# Constraint 4: Horror and mystery on different screens
solver.add(screen[HORROR] != screen[MYSTERY])

# Additional condition: Sci-fi and romance on the same screen
solver.add(screen[SCIFI] == screen[ROMANCE])

# Define answer choice constraints
opt_a = (time[WESTERN] == 7)
opt_b = (time[SCIFI] == 9)
opt_c = (time[MYSTERY] == 8)
opt_d = (time[ROMANCE] == 9)
opt_e = (time[HORROR] == 8)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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