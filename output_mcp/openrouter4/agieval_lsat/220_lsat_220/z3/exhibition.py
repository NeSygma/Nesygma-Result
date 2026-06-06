from z3 import *

solver = Solver()

# Paintings (0-7)
# 0: FO (Franz Oil)
# 1: FW (Franz Watercolor)
# 2: GO (Greene Oil)
# 3: GW (Greene Watercolor)
# 4: HO (Hidalgo Oil)
# 5: HW (Hidalgo Watercolor)
# 6: IO (Isaacs Oil)
# 7: IW (Isaacs Watercolor)

# Slots (0-7)
# i=0: wall 1 upper
# i=1: wall 1 lower
# i=2: wall 2 upper
# i=3: wall 2 lower
# i=4: wall 3 upper
# i=5: wall 3 lower
# i=6: wall 4 upper
# i=7: wall 4 lower

wall_of_slot = [1, 1, 2, 2, 3, 3, 4, 4]
pos_of_slot = [1, 0, 1, 0, 1, 0, 1, 0]  # 1=upper, 0=lower

# Properties of each painting
student_of = [0, 0, 1, 1, 2, 2, 3, 3]  # F=0, G=1, H=2, I=3
type_of = [0, 1, 0, 1, 0, 1, 0, 1]    # O=0, W=1

# Slot variables: which painting is in each slot
slot = [Int(f'slot_{i}') for i in range(8)]
for i in range(8):
    solver.add(slot[i] >= 0, slot[i] <= 7)

# Each painting is assigned to exactly one slot
solver.add(Distinct(slot))

# ========== CONSTRAINTS ==========

# Constraint 1: No wall has only watercolors -> each wall has at least one oil
for w in range(1, 5):
    slots_on_wall = [i for i in range(8) if wall_of_slot[i] == w]
    solver.add(Or([type_of[slot[i]] == 0 for i in slots_on_wall]))

# Constraint 2: No wall has the work of only one student -> each wall has at least 2 different students
for w in range(1, 5):
    slots_on_wall = [i for i in range(8) if wall_of_slot[i] == w]
    solver.add(Or([student_of[slot[slots_on_wall[0]]] != student_of[slot[slots_on_wall[1]]]]))

# Constraint 3: No wall has both Franz and Isaacs
for w in range(1, 5):
    slots_on_wall = [i for i in range(8) if wall_of_slot[i] == w]
    # Not (Franz on this wall AND Isaacs on this wall)
    solver.add(Not(And(
        Or([student_of[slot[i]] == 0 for i in slots_on_wall]),
        Or([student_of[slot[i]] == 3 for i in slots_on_wall])
    )))

# Constraint 4: Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed.
# GW (painting 3) is in upper position, and on the same wall as FO (painting 0)
# Find which slot GW is in and which slot FO is in
gw_slot = Int('gw_slot')
fo_slot = Int('fo_slot')
solver.add(gw_slot >= 0, gw_slot <= 7)
solver.add(fo_slot >= 0, fo_slot <= 7)
solver.add(slot[gw_slot] == 3)  # GW
solver.add(slot[fo_slot] == 0)  # FO
solver.add(pos_of_slot[gw_slot] == 1)  # upper position
solver.add(wall_of_slot[gw_slot] == wall_of_slot[fo_slot])  # same wall

# Constraint 5: Isaacs's oil is displayed in the lower position of wall 4
# IO (painting 6) is in lower position of wall 4
# wall 4 lower = slot 7
solver.add(slot[7] == 6)

# ========== GIVEN CONDITIONS (for this scenario) ==========
# Isaacs's watercolor (IW = 7) is displayed on wall 2
# wall 2 slots are 2 and 3
solver.add(Or([slot[2] == 7, slot[3] == 7]))

# Franz's oil (FO = 0) is displayed on wall 3
# wall 3 slots are 4 and 5
solver.add(Or([slot[4] == 0, slot[5] == 0]))

# From constraint 4: GW is on the same wall as FO (wall 3) in upper position
# So GW must be in slot 4 (wall 3 upper) and FO must be in slot 5 (wall 3 lower) or vice versa
# Actually, constraint 4 says GW is in upper position of the wall where FO is.
# So if FO is on wall 3, GW is in upper position of wall 3.
solver.add(slot[4] == 3)  # GW on wall 3 upper
# FO is on wall 3, and it's on the same wall as GW, so FO must be on wall 3 lower (slot 5)
solver.add(slot[5] == 0)  # FO on wall 3 lower

# ========== EVALUATE OPTIONS ==========
# We need to find which painting MUST be on wall 1
# Option A: Franz's watercolor (FW = 1) on wall 1
# Option B: Greene's oil (GO = 2) on wall 1
# Option C: Greene's watercolor (GW = 3) on wall 1
# Option D: Hidalgo's oil (HO = 4) on wall 1
# Option E: Hidalgo's watercolor (HW = 5) on wall 1

# For "must be" questions, we check: can the painting NOT be on wall 1?
# If unsat, then the painting MUST be on wall 1.

# wall 1 slots: 0 (upper), 1 (lower)

found_must = []
option_names = ["A", "B", "C", "D", "E"]
option_paintings = [1, 2, 3, 4, 5]  # FW, GO, GW, HO, HW

for letter, p in zip(option_names, option_paintings):
    solver.push()
    # Try to find a model where this painting is NOT on wall 1
    solver.add(And(slot[0] != p, slot[1] != p))
    result = solver.check()
    if result == unsat:
        found_must.append(letter)
    solver.pop()

if len(found_must) == 1:
    print("STATUS: sat")
    print(f"answer:{found_must[0]}")
elif len(found_must) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_must}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")