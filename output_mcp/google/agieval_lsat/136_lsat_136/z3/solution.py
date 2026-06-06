from z3 import *

solver = Solver()

# Birds: 0:O, 1:P, 2:R, 3:S, 4:T
# Halls: 0:G, 1:H
birds = [Int(f'bird_{i}') for i in range(5)]
halls = [Int(f'hall_{i}') for i in range(5)]

# Each lecture is a different bird
solver.add(Distinct(birds))
for i in range(5):
    solver.add(birds[i] >= 0, birds[i] <= 4)
    solver.add(halls[i] >= 0, halls[i] <= 1)

# C1: The first lecture is in Gladwyn Hall (G=0)
solver.add(halls[0] == 0)
# C2: The fourth lecture is in Howard Auditorium (H=1)
solver.add(halls[3] == 1)
# C3: Exactly three of the lectures are in Gladwyn Hall
solver.add(Sum([If(halls[i] == 0, 1, 0) for i in range(5)]) == 3)

# C4: The lecture on sandpipers (S=3) is in Howard Auditorium (H=1)
# C5: The lecture on sandpipers (S=3) is earlier than the lecture on oystercatchers (O=0)
# C6: The lecture on terns (T=4) is earlier than the lecture on petrels (P=1)
# C7: The lecture on petrels (P=1) is in Gladwyn Hall (G=0)

# Helper to find index of a bird
def get_idx(bird_val):
    return Sum([If(birds[i] == bird_val, i, 0) for i in range(5)])

# C4: S is in H
for i in range(5):
    solver.add(Implies(birds[i] == 3, halls[i] == 1))

# C5: S < O
s_idx = Int('s_idx')
o_idx = Int('o_idx')
solver.add(Or([And(birds[i] == 3, s_idx == i) for i in range(5)]))
solver.add(Or([And(birds[i] == 0, o_idx == i) for i in range(5)]))
solver.add(s_idx < o_idx)

# C6: T < P
t_idx = Int('t_idx')
p_idx = Int('p_idx')
solver.add(Or([And(birds[i] == 4, t_idx == i) for i in range(5)]))
solver.add(Or([And(birds[i] == 1, p_idx == i) for i in range(5)]))
solver.add(t_idx < p_idx)

# C7: P is in G
for i in range(5):
    solver.add(Implies(birds[i] == 1, halls[i] == 0))

# Q: If the lecture on terns is given in Howard Auditorium
t_in_h = Or([And(birds[i] == 4, halls[i] == 1) for i in range(5)])
solver.add(t_in_h)

# Options for 3rd lecture (index 2)
# (A) O and G
opt_a = And(birds[2] == 0, halls[2] == 0)
# (B) R and H
opt_b = And(birds[2] == 2, halls[2] == 1)
# (C) R and G
opt_c = And(birds[2] == 2, halls[2] == 0)
# (D) S and H
opt_d = And(birds[2] == 3, halls[2] == 1)
# (E) T and H
opt_e = And(birds[2] == 4, halls[2] == 1)

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