from z3 import *

# Constants
G, H = 0, 1
O, P, R, S, T = 0, 1, 2, 3, 4
birds = [O, P, R, S, T]

solver = Solver()

# Variables
# bird_at[i] is the bird at position i (0-4)
bird_at = [Int(f'bird_at_{i}') for i in range(5)]
# hall_at[i] is the hall at position i (0-4)
hall_at = [Int(f'hall_at_{i}') for i in range(5)]

# Constraints
# 1. Each bird is used exactly once
solver.add(Distinct(bird_at))
for b in birds:
    solver.add(Or([bird_at[i] == b for i in range(5)]))

# 2. Halls are G or H
for i in range(5):
    solver.add(Or(hall_at[i] == G, hall_at[i] == H))

# 3. The first lecture is in Gladwyn Hall (G)
solver.add(hall_at[0] == G)
# 4. The fourth lecture is in Howard Auditorium (H)
solver.add(hall_at[3] == H)
# 5. Exactly three of the lectures are in Gladwyn Hall
solver.add(Sum([If(hall_at[i] == G, 1, 0) for i in range(5)]) == 3)

# Helper to get position of a bird
def get_pos(b):
    return Sum([If(bird_at[i] == b, i, 0) for i in range(5)])

# Helper to get hall of a bird
def get_hall(b):
    return Sum([If(bird_at[i] == b, hall_at[i], 0) for i in range(5)])

# 6. The lecture on sandpipers is in Howard Auditorium
solver.add(get_hall(S) == H)
# 7. Sandpipers is earlier than oystercatchers
solver.add(get_pos(S) < get_pos(O))
# 8. Terns is earlier than petrels
solver.add(get_pos(T) < get_pos(P))
# 9. Petrels is in Gladwyn Hall
solver.add(get_hall(P) == G)

# Question: If the third lecture is on sandpipers
solver.add(bird_at[2] == S)

# Options
# (A) The second lecture is on oystercatchers and is in Gladwyn Hall.
opt_a = And(bird_at[1] == O, hall_at[1] == G)
# (B) The fifth lecture is on oystercatchers and is in Howard Auditorium.
opt_b = And(bird_at[4] == O, hall_at[4] == H)
# (C) The second lecture is on rails and is in Howard Auditorium.
opt_c = And(bird_at[1] == R, hall_at[1] == H)
# (D) The second lecture is on terns and is in Gladwyn Hall.
opt_d = And(bird_at[1] == T, hall_at[1] == G)
# (E) The fourth lecture is on terns and is in Howard Auditorium.
opt_e = And(bird_at[3] == T, hall_at[3] == H)

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