from z3 import *

# Declare movies and screens
movies = ["horror", "mystery", "romance", "sci-fi", "western"]
screens = [1, 2, 3]
times = [7, 8, 9]  # 7 and 9 for screens 1 and 2; 8 for screen 3

# Decision variables:
# screen[m] = screen assigned to movie m
# time[m] = time assigned to movie m
screen = {m: Int(f"screen_{m}") for m in movies}
time = {m: Int(f"time_{m}") for m in movies}

solver = Solver()

# Helper: Screen 3 only has time 8
for m in movies:
    solver.add(Implies(screen[m] == 3, time[m] == 8))

# Each movie is assigned to exactly one screen and one time
for m in movies:
    solver.add(screen[m] >= 1, screen[m] <= 3)
    solver.add(time[m] >= 7, time[m] <= 9)
    solver.add(Or(time[m] == 7, time[m] == 9, time[m] == 8))  # 7 or 9 for screens 1 and 2, 8 for screen 3

# Screens 1 and 2 have exactly two movies each (one at 7, one at 9)
for s in [1, 2]:
    solver.add(Sum([If(And(screen[m] == s, time[m] == 7), 1, 0) for m in movies]) == 1)
    solver.add(Sum([If(And(screen[m] == s, time[m] == 9), 1, 0) for m in movies]) == 1)

# Screen 3 has exactly one movie at 8
solver.add(Sum([If(And(screen[m] == 3, time[m] == 8), 1, 0) for m in movies]) == 1)

# Constraints:
# 1. Western begins before horror
solver.add(Implies(screen["western"] == screen["horror"], time["western"] < time["horror"]))
solver.add(Implies(screen["western"] != screen["horror"], time["western"] < time["horror"]))

# 2. Sci-fi not on screen 3
solver.add(screen["sci-fi"] != 3)

# 3. Romance not on screen 2
solver.add(screen["romance"] != 2)

# 4. Horror and mystery on different screens
solver.add(screen["horror"] != screen["mystery"])

# Additional condition: Sci-fi and romance on the same screen
solver.add(screen["sci-fi"] == screen["romance"])

# Now evaluate each option to see which must be true
found_options = []

# Option A: The western begins at 7 P.M.
opt_a_constr = (time["western"] == 7)
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: The sci-fi film begins at 9 P.M.
opt_b_constr = (time["sci-fi"] == 9)
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: The mystery begins at 8 P.M.
opt_c_constr = (time["mystery"] == 8)
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: The romance begins at 9 P.M.
opt_d_constr = (time["romance"] == 9)
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: The horror film begins at 8 P.M.
opt_e_constr = (time["horror"] == 8)
solver.push()
solver.add(opt_e_constr)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")