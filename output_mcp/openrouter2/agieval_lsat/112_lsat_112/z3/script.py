from z3 import *

solver = Solver()

# Positions for each article
pos_G = Int('pos_G')
pos_H = Int('pos_H')
pos_J = Int('pos_J')
pos_Q = Int('pos_Q')
pos_R = Int('pos_R')
pos_S = Int('pos_S')
pos_Y = Int('pos_Y')

articles = [pos_G, pos_H, pos_J, pos_Q, pos_R, pos_S, pos_Y]

# Domain constraints
for p in articles:
    solver.add(p >= 1, p <= 7)

# All positions distinct
solver.add(Distinct(articles))

# Ensure every position 1..7 is used by some article
for k in range(1, 8):
    solver.add(Or(pos_G == k, pos_H == k, pos_J == k, pos_Q == k,
                  pos_R == k, pos_S == k, pos_Y == k))

# Topic mapping: 1=finance, 2=nutrition, 3=wildlife
topic_G = 1
topic_H = 1
topic_J = 1
topic_Q = 2
topic_R = 2
topic_S = 2
topic_Y = 3

# Consecutive articles cannot cover the same topic
pos_topic_pairs = [
    (pos_G, topic_G),
    (pos_H, topic_H),
    (pos_J, topic_J),
    (pos_Q, topic_Q),
    (pos_R, topic_R),
    (pos_S, topic_S),
    (pos_Y, topic_Y)
]

for i in range(len(pos_topic_pairs)):
    for j in range(i+1, len(pos_topic_pairs)):
        pi, ti = pos_topic_pairs[i]
        pj, tj = pos_topic_pairs[j]
        solver.add(Implies(Or(pi == pj + 1, pj == pi + 1), ti != tj))

# S earlier than Q only if Q is third
solver.add(Implies(pos_S < pos_Q, pos_Q == 3))

# S earlier than Y
solver.add(pos_S < pos_Y)

# J earlier than G
solver.add(pos_J < pos_G)

# G earlier than R
solver.add(pos_G < pos_R)

# Option constraints
opt_a_constr = pos_G == 2
opt_b_constr = pos_H == 2
opt_c_constr = pos_S == 2
opt_d_constr = pos_R == 3
opt_e_constr = pos_Y == 3

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