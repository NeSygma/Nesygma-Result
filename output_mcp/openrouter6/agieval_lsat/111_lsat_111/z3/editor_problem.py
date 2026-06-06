from z3 import *

# Article IDs
G_id, H_id, J_id, Q_id, R_id, S_id, Y_id = 0, 1, 2, 3, 4, 5, 6

# Topic mapping: 0=finance, 1=nutrition, 2=wildlife
def topic_of(article):
    """Return Z3 expression for topic of article ID"""
    return If(article <= 2, 0, If(article <= 5, 1, 2))

def same_topic(a, b):
    """Return True if articles a and b have the same topic"""
    return Or(
        And(a <= 2, b <= 2),  # both finance
        And(a >= 3, a <= 5, b >= 3, b <= 5),  # both nutrition
        And(a == 6, b == 6)  # both wildlife
    )

# Create solver
solver = Solver()

# Slot array: slot[i] = article ID at position i (0-indexed, positions 1-7)
slot = [Int(f"slot_{i}") for i in range(7)]

# Each slot must be between 0 and 6
for i in range(7):
    solver.add(slot[i] >= 0, slot[i] <= 6)

# All slots must be distinct (permutation constraint)
solver.add(Distinct(slot))

# Index variables for each article (0-indexed position)
idx_G = Int('idx_G')
idx_H = Int('idx_H')
idx_J = Int('idx_J')
idx_Q = Int('idx_Q')
idx_R = Int('idx_R')
idx_S = Int('idx_S')
idx_Y = Int('idx_Y')

# Each index must be between 0 and 6
for idx in [idx_G, idx_H, idx_J, idx_Q, idx_R, idx_S, idx_Y]:
    solver.add(idx >= 0, idx <= 6)

# Relate index variables to slot array using Or-loop pattern
for i in range(7):
    solver.add(Or(
        And(slot[i] == G_id, idx_G == i),
        And(slot[i] == H_id, idx_H == i),
        And(slot[i] == J_id, idx_J == i),
        And(slot[i] == Q_id, idx_Q == i),
        And(slot[i] == R_id, idx_R == i),
        And(slot[i] == S_id, idx_S == i),
        And(slot[i] == Y_id, idx_Y == i)
    ))

# Base constraints from problem statement
# 1. G is fourth (position 4 => index 3)
solver.add(idx_G == 3)

# 2. J must be earlier than G
solver.add(idx_J < idx_G)

# 3. G must be earlier than R
solver.add(idx_G < idx_R)

# 4. S must be earlier than Y
solver.add(idx_S < idx_Y)

# 5. S can be earlier than Q only if Q is third (position 3 => index 2)
# Equivalent: If S < Q then Q must be at index 2
solver.add(Implies(idx_S < idx_Q, idx_Q == 2))
# Alternative formulation: Or(Q is third, S is after Q)
# solver.add(Or(idx_Q == 2, idx_S > idx_Q))

# 6. Consecutive articles cannot cover the same topic
for i in range(6):
    solver.add(Not(same_topic(slot[i], slot[i+1])))

# Now evaluate multiple choice options
BENCHMARK_MODE = True

found_options = []

# Option A: H is fifth (position 5 => index 4)
opt_a_constr = (idx_H == 4)

# Option B: J is first (position 1 => index 0)
opt_b_constr = (idx_J == 0)

# Option C: Q is second (position 2 => index 1)
opt_c_constr = (idx_Q == 1)

# Option D: S is fifth (position 5 => index 4)
opt_d_constr = (idx_S == 4)

# Option E: Y is sixth (position 6 => index 5)
opt_e_constr = (idx_Y == 5)

for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), 
                       ("C", opt_c_constr), ("D", opt_d_constr), 
                       ("E", opt_e_constr)]:
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