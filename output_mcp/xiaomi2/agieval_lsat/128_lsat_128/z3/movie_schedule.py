from z3 import *

solver = Solver()

# Movies: horror=0, mystery=1, romance=2, sci-fi=3, western=4
# Screens: 1, 2, 3
# Times: 7=7, 8=8, 9=9

# Define base constraints that any valid schedule must satisfy
# We'll encode each option as constraints on screen and time per movie

# For each option, define screen[movie] and time[movie]
def make_option_constraints(option_data):
    """option_data: dict mapping movie name -> (screen, time)"""
    constraints = []
    screens = {}
    times = {}
    for movie, (scr, tm) in option_data.items():
        screens[movie] = scr
        times[movie] = tm
    
    # Constraint 1: Western begins before horror
    constraints.append(times['western'] < times['horror'])
    
    # Constraint 2: Sci-fi not on screen 3
    constraints.append(screens['sci-fi'] != 3)
    
    # Constraint 3: Romance not on screen 2
    constraints.append(screens['romance'] != 2)
    
    # Constraint 4: Horror and mystery on different screens
    constraints.append(screens['horror'] != screens['mystery'])
    
    return And(constraints)

# Option A: screen 1: romance@7, horror@9; screen 2: western@7, sci-fi@9; screen 3: mystery@8
opt_a = make_option_constraints({
    'horror': (1, 9), 'mystery': (3, 8), 'romance': (1, 7),
    'sci-fi': (2, 9), 'western': (2, 7)
})

# Option B: screen 1: mystery@7, romance@9; screen 2: horror@7, sci-fi@9; screen 3: western@8
opt_b = make_option_constraints({
    'horror': (2, 7), 'mystery': (1, 7), 'romance': (1, 9),
    'sci-fi': (2, 9), 'western': (3, 8)
})

# Option C: screen 1: western@7, sci-fi@9; screen 2: mystery@7, horror@9; screen 3: romance@8
opt_c = make_option_constraints({
    'horror': (2, 9), 'mystery': (2, 7), 'romance': (3, 8),
    'sci-fi': (1, 9), 'western': (1, 7)
})

# Option D: screen 1: romance@7, mystery@9; screen 2: western@7, horror@9; screen 3: sci-fi@8
opt_d = make_option_constraints({
    'horror': (2, 9), 'mystery': (1, 9), 'romance': (1, 7),
    'sci-fi': (3, 8), 'western': (2, 7)
})

# Option E: screen 1: western@7, mystery@9; screen 2: sci-fi@7, romance@9; screen 3: horror@8
opt_e = make_option_constraints({
    'horror': (3, 8), 'mystery': (1, 9), 'romance': (2, 9),
    'sci-fi': (2, 7), 'western': (1, 7)
})

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