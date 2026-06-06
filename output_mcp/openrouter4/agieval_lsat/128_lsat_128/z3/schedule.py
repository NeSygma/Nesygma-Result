from z3 import *

solver = Solver()

# Movies: 0=Horror, 1=Mystery, 2=Romance, 3=SciFi, 4=Western
# Slots: 0=(screen1,7PM), 1=(screen1,9PM), 2=(screen2,7PM), 3=(screen2,9PM), 4=(screen3,8PM)

slots = [Int(f'slot_{i}') for i in range(5)]  # slot_H, slot_M, slot_R, slot_S, slot_W

for s in slots:
    solver.add(s >= 0, s <= 4)

solver.add(Distinct(slots))

screen_of_slot = [1, 1, 2, 2, 3]
time_of_slot = [7, 9, 7, 9, 8]

# Constraint 1: Western (index 4) begins before Horror (index 0)
w_time_lt_h_time = Or([And(slots[4] == i, slots[0] == j, time_of_slot[i] < time_of_slot[j]) 
                       for i in range(5) for j in range(5)])
solver.add(w_time_lt_h_time)

# Constraint 2: Sci-fi (index 3) not on screen 3
s_not_screen3 = Or([And(slots[3] == i, screen_of_slot[i] != 3) for i in range(5)])
solver.add(s_not_screen3)

# Constraint 3: Romance (index 2) not on screen 2
r_not_screen2 = Or([And(slots[2] == i, screen_of_slot[i] != 2) for i in range(5)])
solver.add(r_not_screen2)

# Constraint 4: Horror (index 0) and Mystery (index 1) on different screens
diff_screens = Or([And(slots[0] == i, slots[1] == j, screen_of_slot[i] != screen_of_slot[j]) 
                   for i in range(5) for j in range(5)])
solver.add(diff_screens)

# Option A: Romance(slot0), Horror(slot1), Western(slot2), SciFi(slot3), Mystery(slot4)
opt_a = And(slots[2] == 0, slots[0] == 1, slots[4] == 2, slots[3] == 3, slots[1] == 4)

# Option B: Mystery(slot0), Romance(slot1), Horror(slot2), SciFi(slot3), Western(slot4)
opt_b = And(slots[1] == 0, slots[2] == 1, slots[0] == 2, slots[3] == 3, slots[4] == 4)

# Option C: Western(slot0), SciFi(slot1), Mystery(slot2), Horror(slot3), Romance(slot4)
opt_c = And(slots[4] == 0, slots[3] == 1, slots[1] == 2, slots[0] == 3, slots[2] == 4)

# Option D: Romance(slot0), Mystery(slot1), Western(slot2), Horror(slot3), SciFi(slot4)
opt_d = And(slots[2] == 0, slots[1] == 1, slots[4] == 2, slots[0] == 3, slots[3] == 4)

# Option E: Western(slot0), Mystery(slot1), SciFi(slot2), Romance(slot3), Horror(slot4)
opt_e = And(slots[4] == 0, slots[1] == 1, slots[3] == 2, slots[2] == 3, slots[0] == 4)

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