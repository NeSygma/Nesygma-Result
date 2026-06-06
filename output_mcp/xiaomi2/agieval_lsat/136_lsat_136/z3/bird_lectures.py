from z3 import *

solver = Solver()

# Birds: 0=oystercatchers, 1=petrels, 2=rails, 3=sandpipers, 4=terns
# Halls: 0=Gladwyn, 1=Howard
# Positions: 0,1,2,3,4 (representing lectures 1-5)

bird_at = [Int(f'bird_at_{i}') for i in range(5)]
hall_at = [Int(f'hall_at_{i}') for i in range(5)]

# Each position has a valid bird (0-4) and hall (0-1)
for i in range(5):
    solver.add(bird_at[i] >= 0, bird_at[i] <= 4)
    solver.add(hall_at[i] >= 0, hall_at[i] <= 1)

# All birds are different
solver.add(Distinct(bird_at))

# Constraint 1: First lecture is in Gladwyn Hall
solver.add(hall_at[0] == 0)

# Constraint 2: Fourth lecture is in Howard Auditorium
solver.add(hall_at[3] == 1)

# Constraint 3: Exactly three lectures in Gladwyn Hall (so exactly 2 in Howard)
solver.add(Sum([If(hall_at[i] == 1, 1, 0) for i in range(5)]) == 2)

# Helper: position of a given bird
def pos_of(bird_id):
    """Returns an Int expression for the position of the given bird."""
    return Sum([If(bird_at[i] == bird_id, i, 0) for i in range(5)])

pos_sandpipers = pos_of(3)  # sandpipers = 3
pos_oystercatchers = pos_of(0)  # oystercatchers = 0
pos_terns = pos_of(4)  # terns = 4
pos_petrels = pos_of(1)  # petrels = 1

# Constraint 4: Sandpipers in Howard and earlier than oystercatchers
# hall of sandpipers == 1 (Howard)
solver.add(Or([And(bird_at[i] == 3, hall_at[i] == 1) for i in range(5)]))
solver.add(pos_sandpipers < pos_oystercatchers)

# Constraint 5: Terns earlier than petrels, petrels in Gladwyn
solver.add(pos_terns < pos_petrels)
solver.add(Or([And(bird_at[i] == 1, hall_at[i] == 0) for i in range(5)]))

# Constraint 6 (question condition): Terns in Howard Auditorium
solver.add(Or([And(bird_at[i] == 4, hall_at[i] == 1) for i in range(5)]))

# Now evaluate each option for the third lecture (position index 2)
# (A) It is on oystercatchers and is in Gladwyn Hall.
opt_a = And(bird_at[2] == 0, hall_at[2] == 0)
# (B) It is on rails and is in Howard Auditorium.
opt_b = And(bird_at[2] == 2, hall_at[2] == 1)
# (C) It is on rails and is in Gladwyn Hall.
opt_c = And(bird_at[2] == 2, hall_at[2] == 0)
# (D) It is on sandpipers and is in Howard Auditorium.
opt_d = And(bird_at[2] == 3, hall_at[2] == 1)
# (E) It is on terns and is in Howard Auditorium.
opt_e = And(bird_at[2] == 4, hall_at[2] == 1)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        m = solver.model()
        found_options.append(letter)
        print(f"Option {letter}: SAT")
        for i in range(5):
            bird_names = {0: "oystercatchers", 1: "petrels", 2: "rails", 3: "sandpipers", 4: "terns"}
            hall_names = {0: "Gladwyn", 1: "Howard"}
            bv = m[bird_at[i]].as_long()
            hv = m[hall_at[i]].as_long()
            print(f"  Position {i+1}: {bird_names[bv]} in {hall_names[hv]}")
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