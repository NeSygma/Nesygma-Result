from z3 import *

# Base constraints solver (for reference, not used for option checking)
base_solver = Solver()

# Movies
movies = ["horror", "mystery", "romance", "sci-fi", "western"]

# For each movie, assign a screen and a time
movie_screen = {m: Int(f"screen_{m}") for m in movies}
movie_time = {m: Int(f"time_{m}") for m in movies}

# Domains
for m in movies:
    base_solver.add(movie_screen[m] >= 1, movie_screen[m] <= 3)
    base_solver.add(movie_time[m] >= 7, movie_time[m] <= 9)

# Screen 3 only shows at 8 PM, and exactly one movie is on screen 3 at 8 PM
count_screen3_time8 = Sum([If(And(movie_screen[m] == 3, movie_time[m] == 8), 1, 0) for m in movies])
base_solver.add(count_screen3_time8 == 1)

# Screens 1 and 2 each have one movie at 7 PM and one at 9 PM
for screen in [1, 2]:
    count_time7 = Sum([If(And(movie_screen[m] == screen, movie_time[m] == 7), 1, 0) for m in movies])
    count_time9 = Sum([If(And(movie_screen[m] == screen, movie_time[m] == 9), 1, 0) for m in movies])
    base_solver.add(count_time7 == 1)
    base_solver.add(count_time9 == 1)

# Western begins before horror
base_solver.add(movie_time["western"] < movie_time["horror"])

# Sci-fi not on screen 3
base_solver.add(movie_screen["sci-fi"] != 3)

# Romance not on screen 2
base_solver.add(movie_screen["romance"] != 2)

# Horror and mystery on different screens
base_solver.add(movie_screen["horror"] != movie_screen["mystery"])

# Now, evaluate each multiple-choice option for screen 2
# Each option specifies: (7 PM movie, 9 PM movie) for screen 2

option_results = {}

# Helper function to check if an option is possible
def check_option(opt_7pm, opt_9pm):
    s = Solver()
    # Copy base constraints
    for c in base_solver.assertions():
        s.add(c)
    # Screen 2 has opt_7pm at 7 and opt_9pm at 9
    s.add(movie_screen[opt_7pm] == 2)
    s.add(movie_time[opt_7pm] == 7)
    s.add(movie_screen[opt_9pm] == 2)
    s.add(movie_time[opt_9pm] == 9)
    # All other movies must not be on screen 2 at 7 or 9
    for m in movies:
        if m != opt_7pm:
            s.add(Not(And(movie_screen[m] == 2, movie_time[m] == 7)))
        if m != opt_9pm:
            s.add(Not(And(movie_screen[m] == 2, movie_time[m] == 9)))
    # Check satisfiability
    res = s.check()
    return res

# Option A: sci-fi (7 PM), horror (9 PM)
res_A = check_option("sci-fi", "horror")
option_results["A"] = res_A

# Option B: sci-fi (7 PM), mystery (9 PM)
res_B = check_option("sci-fi", "mystery")
option_results["B"] = res_B

# Option C: sci-fi (7 PM), western (9 PM)
res_C = check_option("sci-fi", "western")
option_results["C"] = res_C

# Option D: western (7 PM), horror (9 PM)
res_D = check_option("western", "horror")
option_results["D"] = res_D

# Option E: western (7 PM), mystery (9 PM)
res_E = check_option("western", "mystery")
option_results["E"] = res_E

# Determine which options are possible
possible_options = [k for k, v in option_results.items() if v == sat]

# Output result
if len(possible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{possible_options[0]}")
elif len(possible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {possible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")

# Print detailed results for debugging
print("\nDetailed results:")
for k, v in option_results.items():
    print(f"Option {k}: {v}")