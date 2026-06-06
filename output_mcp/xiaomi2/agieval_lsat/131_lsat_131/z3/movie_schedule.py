from z3 import *

solver = Solver()

# Movies: H=0, M=1, R=2, S=3, W=4
movies = 5
H, M, R, S, W = 0, 1, 2, 3, 4

# Each movie assigned to a slot (0-4)
# Slot 0: Screen 1, 7PM
# Slot 1: Screen 1, 9PM
# Slot 2: Screen 2, 7PM
# Slot 3: Screen 2, 9PM
# Slot 4: Screen 3, 8PM
slot = [Int(f'slot_{i}') for i in range(movies)]

# Each slot is 0-4, all distinct
for i in range(movies):
    solver.add(slot[i] >= 0, slot[i] <= 4)
solver.add(Distinct(slot))

# Screen from slot
def screen(s):
    return If(s == 0, 1, If(s == 1, 1, If(s == 2, 2, If(s == 3, 2, 3))))

# Time from slot
def time_val(s):
    return If(s == 0, 7, If(s == 1, 9, If(s == 2, 7, If(s == 3, 9, 8))))

# Condition 1: Western begins before Horror
solver.add(time_val(slot[W]) < time_val(slot[H]))

# Condition 2: Sci-fi not on screen 3
solver.add(screen(slot[S]) != 3)

# Condition 3: Romance not on screen 2
solver.add(screen(slot[R]) != 2)

# Condition 4: Horror and Mystery on different screens
solver.add(screen(slot[H]) != screen(slot[M]))

# Additional condition: Romance begins before Western
solver.add(time_val(slot[R]) < time_val(slot[W]))

# Define answer options
# (A) Horror is shown on screen 1
opt_a = screen(slot[H]) == 1
# (B) Mystery begins at 7 PM
opt_b = time_val(slot[M]) == 7
# (C) Mystery is shown on screen 2
opt_c = screen(slot[M]) == 2
# (D) Sci-fi film begins at 9 PM
opt_d = time_val(slot[S]) == 9
# (E) Sci-fi film is shown on screen 2
opt_e = screen(slot[S]) == 2

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

# For "must be true": check if NOT(option) is unsatisfiable given all constraints
must_be_true = []
for letter, opt in options:
    s = Solver()
    for c in solver.assertions():
        s.add(c)
    s.add(Not(opt))
    res = s.check()
    if res == unsat:
        must_be_true.append(letter)
        print(f"Option {letter}: MUST BE TRUE (negation is unsat)")
    elif res == sat:
        print(f"Option {letter}: NOT necessarily true (counterexample exists)")
        # Show counterexample
        m = s.model()
        for i in range(movies):
            sv = m[slot[i]]
            print(f"  Movie {i} -> slot {sv} (screen {m.evaluate(screen(slot[i]))}, time {m.evaluate(time_val(slot[i]))})")
    else:
        print(f"Option {letter}: UNKNOWN")

print()
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true options found")