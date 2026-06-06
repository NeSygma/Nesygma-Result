from z3 import *

# Movies: horror (H), mystery (M), romance (R), sci-fi (S), western (W)
# Screens: 1, 2, 3
# Times: 7PM, 8PM, 9PM
# Screen 1: two movies at 7PM and 9PM
# Screen 2: two movies at 7PM and 9PM
# Screen 3: one movie at 8PM

H_screen = Int('H_screen')
H_time = Int('H_time')
M_screen = Int('M_screen')
M_time = Int('M_time')
R_screen = Int('R_screen')
R_time = Int('R_time')
S_screen = Int('S_screen')
S_time = Int('S_time')
W_screen = Int('W_screen')
W_time = Int('W_time')

solver = Solver()

# Domain constraints
for scr in [H_screen, M_screen, R_screen, S_screen, W_screen]:
    solver.add(scr >= 1, scr <= 3)
for t in [H_time, M_time, R_time, S_time, W_time]:
    solver.add(t >= 7, t <= 9)
    solver.add(Or(t == 7, t == 8, t == 9))

# Each movie has a unique screen-time combination (no two movies share same screen+time)
# We'll enforce this via: each screen-time slot has exactly the right number of movies.

# Screen 1: exactly 2 movies, one at 7 and one at 9
solver.add(Sum([If(s == 1, 1, 0) for s in [H_screen, M_screen, R_screen, S_screen, W_screen]]) == 2)
solver.add(Sum([If(And(s == 1, t == 7), 1, 0) for s, t in [(H_screen, H_time), (M_screen, M_time), (R_screen, R_time), (S_screen, S_time), (W_screen, W_time)]]) == 1)
solver.add(Sum([If(And(s == 1, t == 9), 1, 0) for s, t in [(H_screen, H_time), (M_screen, M_time), (R_screen, R_time), (S_screen, S_time), (W_screen, W_time)]]) == 1)

# Screen 2: exactly 2 movies, one at 7 and one at 9
solver.add(Sum([If(s == 2, 1, 0) for s in [H_screen, M_screen, R_screen, S_screen, W_screen]]) == 2)
solver.add(Sum([If(And(s == 2, t == 7), 1, 0) for s, t in [(H_screen, H_time), (M_screen, M_time), (R_screen, R_time), (S_screen, S_time), (W_screen, W_time)]]) == 1)
solver.add(Sum([If(And(s == 2, t == 9), 1, 0) for s, t in [(H_screen, H_time), (M_screen, M_time), (R_screen, R_time), (S_screen, S_time), (W_screen, W_time)]]) == 1)

# Screen 3: exactly 1 movie at 8
solver.add(Sum([If(s == 3, 1, 0) for s in [H_screen, M_screen, R_screen, S_screen, W_screen]]) == 1)
solver.add(Sum([If(And(s == 3, t == 8), 1, 0) for s, t in [(H_screen, H_time), (M_screen, M_time), (R_screen, R_time), (S_screen, S_time), (W_screen, W_time)]]) == 1)

# No movie at screen 3 at 7 or 9
solver.add(Sum([If(And(s == 3, t == 7), 1, 0) for s, t in [(H_screen, H_time), (M_screen, M_time), (R_screen, R_time), (S_screen, S_time), (W_screen, W_time)]]) == 0)
solver.add(Sum([If(And(s == 3, t == 9), 1, 0) for s, t in [(H_screen, H_time), (M_screen, M_time), (R_screen, R_time), (S_screen, S_time), (W_screen, W_time)]]) == 0)

# No movie at screen 1 or 2 at 8
solver.add(Sum([If(And(s == 1, t == 8), 1, 0) for s, t in [(H_screen, H_time), (M_screen, M_time), (R_screen, R_time), (S_screen, S_time), (W_screen, W_time)]]) == 0)
solver.add(Sum([If(And(s == 2, t == 8), 1, 0) for s, t in [(H_screen, H_time), (M_screen, M_time), (R_screen, R_time), (S_screen, S_time), (W_screen, W_time)]]) == 0)

# Constraint: The western begins at some time before the horror film does.
solver.add(W_time < H_time)

# Constraint: The sci-fi film is not shown on screen 3.
solver.add(S_screen != 3)

# Constraint: The romance is not shown on screen 2.
solver.add(R_screen != 2)

# Constraint: The horror film and the mystery are shown on different screens.
solver.add(H_screen != M_screen)

# Let's first check if the base constraints are satisfiable
print("Base check:", solver.check())
if solver.check() == sat:
    m = solver.model()
    print("H:", m[H_screen], m[H_time])
    print("M:", m[M_screen], m[M_time])
    print("R:", m[R_screen], m[R_time])
    print("S:", m[S_screen], m[S_time])
    print("W:", m[W_screen], m[W_time])

# Now evaluate each option.
# Each option lists two movies for screen 1, 7PM first then 9PM.

# Option A: sci-fi (S) at 7, horror (H) at 9
opt_a = [And(S_screen == 1, S_time == 7, H_screen == 1, H_time == 9)]

# Option B: sci-fi (S) at 7, mystery (M) at 9
opt_b = [And(S_screen == 1, S_time == 7, M_screen == 1, M_time == 9)]

# Option C: western (W) at 7, horror (H) at 9
opt_c = [And(W_screen == 1, W_time == 7, H_screen == 1, H_time == 9)]

# Option D: western (W) at 7, mystery (M) at 9
opt_d = [And(W_screen == 1, W_time == 7, M_screen == 1, M_time == 9)]

# Option E: western (W) at 7, sci-fi (S) at 9
opt_e = [And(W_screen == 1, W_time == 7, S_screen == 1, S_time == 9)]

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    print(f"Option {letter}: {result}")
    if result == sat:
        found_options.append(letter)
    solver.pop()

print("Found options:", found_options)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")