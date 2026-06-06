from z3 import *

# Movies: horror=0, mystery=1, romance=2, sci-fi=3, western=4
movies = ['horror', 'mystery', 'romance', 'sci-fi', 'western']
HORROR, MYSTERY, ROMANCE, SCIFI, WESTERN = range(5)

# Valid slots: (screen, time)
# 0: (1,7), 1: (1,9), 2: (2,7), 3: (2,9), 4: (3,8)
slot_screen = [1, 1, 2, 2, 3]
slot_time = [7, 9, 7, 9, 8]

def build_base_solver():
    solver = Solver()
    assign = [Int(f'assign_{m}') for m in movies]
    
    for m in range(5):
        solver.add(assign[m] >= 0, assign[m] <= 4)
    solver.add(Distinct(assign))
    
    def get_screen(movie_idx):
        return If(assign[movie_idx] == 0, 1,
               If(assign[movie_idx] == 1, 1,
               If(assign[movie_idx] == 2, 2,
               If(assign[movie_idx] == 3, 2,
               3))))
    
    def get_time(movie_idx):
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
    # Additional: Sci-fi and romance on the same screen
    solver.add(screen[SCIFI] == screen[ROMANCE])
    
    return solver, assign, screen, time

# First, let's enumerate all valid schedules to understand the solution space
solver, assign, screen, time = build_base_solver()

all_solutions = []
decision_vars = assign
while solver.check() == sat:
    m = solver.model()
    sol = {str(v): m.eval(v, model_completion=True).as_long() for v in decision_vars}
    all_solutions.append(sol)
    solver.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))

print(f"Total valid schedules: {len(all_solutions)}")
for i, sol in enumerate(all_solutions):
    print(f"\nSchedule {i+1}:")
    for j, name in enumerate(movies):
        s = slot_screen[sol[f'assign_{name}']]
        t = slot_time[sol[f'assign_{name}']]
        print(f"  {name}: Screen {s} at {t}:00")

# Now check which options MUST be true (negation is unsat)
opt_a = (time[WESTERN] == 7)
opt_b = (time[SCIFI] == 9)
opt_c = (time[MYSTERY] == 8)
opt_d = (time[ROMANCE] == 9)
opt_e = (time[HORROR] == 8)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

must_be_true = []
for letter, constr in options:
    s = Solver()
    # Re-add all base constraints
    assign2 = [Int(f'assign_{m}') for m in movies]
    for m in range(5):
        s.add(assign2[m] >= 0, assign2[m] <= 4)
    s.add(Distinct(assign2))
    
    def get_screen2(movie_idx):
        return If(assign2[movie_idx] == 0, 1,
               If(assign2[movie_idx] == 1, 1,
               If(assign2[movie_idx] == 2, 2,
               If(assign2[movie_idx] == 3, 2,
               3))))
    def get_time2(movie_idx):
        return If(assign2[movie_idx] == 0, 7,
               If(assign2[movie_idx] == 1, 9,
               If(assign2[movie_idx] == 2, 7,
               If(assign2[movie_idx] == 3, 9,
               8))))
    
    screen2 = [get_screen2(i) for i in range(5)]
    time2 = [get_time2(i) for i in range(5)]
    
    s.add(time2[WESTERN] < time2[HORROR])
    s.add(screen2[SCIFI] != 3)
    s.add(screen2[ROMANCE] != 2)
    s.add(screen2[HORROR] != screen2[MYSTERY])
    s.add(screen2[SCIFI] == screen2[ROMANCE])
    
    # Add NEGATION of the option
    s.add(Not(constr))
    
    result = s.check()
    if result == unsat:
        must_be_true.append(letter)
        print(f"\nOption {letter}: MUST be true (negation is unsat)")
    else:
        print(f"\nOption {letter}: NOT necessarily true (negation is sat)")

if len(must_be_true) == 1:
    print(f"\nSTATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print(f"\nSTATUS: sat")
    print(f"Multiple must-be-true: {must_be_true}")
else:
    print(f"\nSTATUS: unsat")
    print("Refine: No option must be true")