from z3 import *

solver = Solver()

# Birds: 0:O, 1:P, 2:R, 3:S, 4:T
# Halls: 0:G, 1:H
birds = [Int(f'bird_{i}') for i in range(5)]
halls = [Int(f'hall_{i}') for i in range(5)]

# Each lecture is a different bird
solver.add(Distinct(birds))
for b in birds:
    solver.add(b >= 0, b <= 4)

# Each hall is G or H
for h in halls:
    solver.add(Or(h == 0, h == 1))

# C1: First lecture is in Gladwyn Hall (G=0)
solver.add(halls[0] == 0)

# C2: Fourth lecture is in Howard Auditorium (H=1)
solver.add(halls[3] == 1)

# C3: Exactly three lectures are in Gladwyn Hall (G=0)
solver.add(Sum([If(halls[i] == 0, 1, 0) for i in range(5)]) == 3)

# Helper to find time of a bird
def get_time(bird_val):
    t = Int(f'time_of_{bird_val}')
    solver.add(Or([And(birds[i] == bird_val, t == i) for i in range(5)]))
    return t

t_S = get_time(3)
t_O = get_time(0)
t_T = get_time(4)
t_P = get_time(1)

# C4: Sandpipers (S=3) is in Howard Auditorium (H=1)
solver.add(Or([And(t_S == i, halls[i] == 1) for i in range(5)]))

# C5: Sandpipers (S=3) is earlier than Oystercatchers (O=0)
solver.add(t_S < t_O)

# C6: Terns (T=4) is earlier than Petrels (P=1)
solver.add(t_T < t_P)

# C7: Petrels (P=1) is in Gladwyn Hall (G=0)
solver.add(Or([And(t_P == i, halls[i] == 0) for i in range(5)]))

# Options
# (A) 5th is O, G
# (B) 5th is P, H
# (C) 5th is R, H
# (D) 5th is S, H
# (E) 5th is T, G

opt_a_constr = And(birds[4] == 0, halls[4] == 0)
opt_b_constr = And(birds[4] == 1, halls[4] == 1)
opt_c_constr = And(birds[4] == 2, halls[4] == 1)
opt_d_constr = And(birds[4] == 3, halls[4] == 1)
opt_e_constr = And(birds[4] == 4, halls[4] == 0)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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