from z3 import *

solver = Solver()

# Movies: 0=horror, 1=mystery, 2=romance, 3=sci-fi, 4=western
movies = ['horror', 'mystery', 'romance', 'sci-fi', 'western']
slots = [Int(f'slot_{m}') for m in movies]

# Each movie assigned to slot 0-4, all distinct
# Slot 0: Screen 1, 7PM
# Slot 1: Screen 1, 9PM
# Slot 2: Screen 2, 7PM
# Slot 3: Screen 2, 9PM
# Slot 4: Screen 3, 8PM
for s in slots:
    solver.add(s >= 0, s <= 4)
solver.add(Distinct(slots))

# Helper: screen from slot
def screen(slot):
    return If(slot == 0, 1, If(slot == 1, 1, If(slot == 2, 2, If(slot == 3, 2, 3))))

# Helper: time from slot
def time_val(slot):
    return If(slot == 0, 7, If(slot == 1, 9, If(slot == 2, 7, If(slot == 3, 9, 8))))

horror_slot = slots[0]
mystery_slot = slots[1]
romance_slot = slots[2]
scifi_slot = slots[3]
western_slot = slots[4]

# Constraint 1: Western begins before horror
solver.add(time_val(western_slot) < time_val(horror_slot))

# Constraint 2: Sci-fi not on screen 3
solver.add(screen(scifi_slot) != 3)

# Constraint 3: Romance not on screen 2
solver.add(screen(romance_slot) != 2)

# Constraint 4: Horror and mystery on different screens
solver.add(screen(horror_slot) != screen(mystery_slot))

# Additional condition: Western and sci-fi on the same screen
solver.add(screen(western_slot) == screen(scifi_slot))

# Define each answer option
# (A) Horror is shown on screen 2
opt_a = screen(horror_slot) == 2

# (B) Mystery begins at 9 PM
opt_b = time_val(mystery_slot) == 9

# (C) Romance is shown on screen 3
opt_c = screen(romance_slot) == 3

# (D) Sci-fi begins at 7 PM
opt_d = time_val(scifi_slot) == 7

# (E) Western begins at 8 PM
opt_e = time_val(western_slot) == 8

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        m = solver.model()
        found_options.append(letter)
        print(f"Option {letter}: SAT")
        for i, name in enumerate(movies):
            s_val = m[slots[i]].as_long()
            scr = [1,1,2,2,3][s_val]
            t = [7,9,7,9,8][s_val]
            print(f"  {name}: slot {s_val} -> Screen {scr}, {t}PM")
    else:
        print(f"Option {letter}: {result}")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")