from z3 import *

solver = Solver()

# 5 lecture positions (1-5)
# Birds: oystercatchers, petrels, rails, sandpipers, terns
# Halls: G (Gladwyn), H (Howard)

# Position variables: which position each bird is assigned to
pos_o = Int('pos_o')  # oystercatchers
pos_p = Int('pos_p')  # petrels
pos_r = Int('pos_r')  # rails
pos_s = Int('pos_s')  # sandpipers
pos_t = Int('pos_t')  # terns

positions = [pos_o, pos_p, pos_r, pos_s, pos_t]

# All positions are 1-5 and distinct
for p in positions:
    solver.add(p >= 1, p <= 5)
solver.add(Distinct(positions))

# Hall assignment: G=0, H=1
hall = [Int(f'hall_{i}') for i in range(1, 6)]
for h in hall:
    solver.add(Or(h == 0, h == 1))

# Condition 1: First lecture is in Gladwyn Hall
solver.add(hall[0] == 0)

# Condition 2: Fourth lecture is in Howard Auditorium
solver.add(hall[3] == 1)

# Condition 3: Exactly three lectures in Gladwyn Hall
solver.add(Sum([If(h == 0, 1, 0) for h in hall]) == 3)

# Condition 4: Sandpipers in Howard, earlier than oystercatchers
# hall[pos_s - 1] == 1 and pos_s < pos_o
solver.add(Or([And(pos_s == i+1, hall[i] == 1) for i in range(5)]))
solver.add(pos_s < pos_o)

# Condition 5: Terns earlier than petrels, petrels in Gladwyn
solver.add(pos_t < pos_p)
solver.add(Or([And(pos_p == i+1, hall[i] == 0) for i in range(5)]))

# Now evaluate each option - which one MUST be false?
# An option "must be false" means it's inconsistent with the constraints (unsat when added)

# Option A: First and second lectures both in Gladwyn Hall
opt_a = And(hall[0] == 0, hall[1] == 0)

# Option B: Second and third lectures both in Howard Auditorium
opt_b = And(hall[1] == 1, hall[2] == 1)

# Option C: Second and fifth lectures both in Gladwyn Hall
opt_c = And(hall[1] == 0, hall[4] == 0)

# Option D: Third and fourth lectures both in Howard Auditorium
opt_d = And(hall[2] == 1, hall[3] == 1)

# Option E: Third and fifth lectures both in Gladwyn Hall
opt_e = And(hall[2] == 0, hall[4] == 0)

# For "must be false", we check if adding the option makes it unsat
# If unsat with option added, the option MUST be false
must_be_false = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        must_be_false.append(letter)
    solver.pop()

print(f"Must be false options: {must_be_false}")

if len(must_be_false) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_false[0]}")
elif len(must_be_false) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-false options found {must_be_false}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-false options found")