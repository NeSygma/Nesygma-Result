from z3 import *

solver = Solver()

# Define slot indices for each movie
slot_h = Int('slot_h')  # horror
slot_m = Int('slot_m')  # mystery
slot_r = Int('slot_r')  # romance
slot_s = Int('slot_s')  # sci-fi
slot_w = Int('slot_w')  # western

# All slots are between 0 and 4 inclusive
solver.add(slot_h >= 0, slot_h <= 4)
solver.add(slot_m >= 0, slot_m <= 4)
solver.add(slot_r >= 0, slot_r <= 4)
solver.add(slot_s >= 0, slot_s <= 4)
solver.add(slot_w >= 0, slot_w <= 4)

# All slots must be distinct (each movie in a different slot)
solver.add(Distinct(slot_h, slot_m, slot_r, slot_s, slot_w))

# Mapping from slot index to screen and time
# slot 0: screen 1, time 7
# slot 1: screen 1, time 9
# slot 2: screen 2, time 7
# slot 3: screen 2, time 9
# slot 4: screen 3, time 8
slot_screen = [1, 1, 2, 2, 3]
slot_time = [7, 9, 7, 9, 8]

# Helper function to get screen from slot index (using If expressions)
def get_screen(slot):
    return If(slot == 0, 1,
           If(slot == 1, 1,
           If(slot == 2, 2,
           If(slot == 3, 2, 3))))

def get_time(slot):
    return If(slot == 0, 7,
           If(slot == 1, 9,
           If(slot == 2, 7,
           If(slot == 3, 9, 8))))

# Compute screen and time for each movie
screen_h = get_screen(slot_h)
time_h = get_time(slot_h)
screen_m = get_screen(slot_m)
time_m = get_time(slot_m)
screen_r = get_screen(slot_r)
time_r = get_time(slot_r)
screen_s = get_screen(slot_s)
time_s = get_time(slot_s)
screen_w = get_screen(slot_w)
time_w = get_time(slot_w)

# Condition 1: Western begins before horror
solver.add(time_w < time_h)

# Condition 2: Sci-fi not on screen 3
solver.add(screen_s != 3)

# Condition 3: Romance not on screen 2
solver.add(screen_r != 2)

# Condition 4: Horror and mystery on different screens
solver.add(screen_h != screen_m)

# Extra condition: Western and sci-fi on same screen
solver.add(screen_w == screen_s)

# Now evaluate each option
found_options = []

# Option A: horror film shown on screen 2
opt_a = (screen_h == 2)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: mystery begins at 9 P.M.
opt_b = (time_m == 9)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: romance shown on screen 3
opt_c = (screen_r == 3)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: sci-fi begins at 7 P.M.
opt_d = (time_s == 7)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: western begins at 8 P.M.
opt_e = (time_w == 8)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")