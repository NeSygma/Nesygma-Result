from z3 import *

solver = Solver()

# Let's use a different modeling approach.
# We have 4 positions (0=earliest, 3=latest).
# Each position has a historian and a topic.
# historian_at[pos] = historian (0=F, 1=G, 2=H, 3=J)
# topic_at[pos] = topic (0=L, 1=O, 2=S, 3=W)

hist = [Int(f'hist_{i}') for i in range(4)]
topic = [Int(f'topic_{i}') for i in range(4)]

for i in range(4):
    solver.add(hist[i] >= 0, hist[i] <= 3)
    solver.add(topic[i] >= 0, topic[i] <= 3)

solver.add(Distinct(hist))
solver.add(Distinct(topic))

# Constraints:
# Oil paintings (1) and watercolors (3) must both be earlier than lithographs (0)
# i.e., position of O < position of L, position of W < position of L
# topic[pos] == O means topic_at_that_position == 1
# So we need: for all positions i, j: if topic[i]==O and topic[j]==L then i < j
# Better: use Or-loop to express ordering constraints

# O < L: there exists i,j such that topic[i]==O, topic[j]==L, i<j
# Actually we need: for all i,j: if topic[i]==O and topic[j]==L then i<j
# Equivalent: the position of O is less than the position of L
# We can encode: Sum(If(topic[i]==O, i, 0)) < Sum(If(topic[i]==L, i, 0))
# Since each topic appears exactly once, the sum of i where topic[i]==O is just the position of O.

pos_O = Sum([If(topic[i]==1, i, 0) for i in range(4)])
pos_L = Sum([If(topic[i]==0, i, 0) for i in range(4)])
pos_W = Sum([If(topic[i]==3, i, 0) for i in range(4)])

solver.add(pos_O < pos_L)
solver.add(pos_W < pos_L)

# Farley's lecture must be earlier than the oil paintings lecture
# pos_F < pos_O
pos_F = Sum([If(hist[i]==0, i, 0) for i in range(4)])
solver.add(pos_F < pos_O)

# Holden's lecture must be earlier than both Garcia's and Jiang's
pos_H = Sum([If(hist[i]==2, i, 0) for i in range(4)])
pos_G = Sum([If(hist[i]==1, i, 0) for i in range(4)])
pos_J = Sum([If(hist[i]==3, i, 0) for i in range(4)])

solver.add(pos_H < pos_G)
solver.add(pos_H < pos_J)

# Now evaluate options
# Option A: Farley gives lithographs => hist[pos] == 0 and topic[pos] == 0 for same pos
# i.e., there exists i such that hist[i]==0 and topic[i]==0
opt_a = Or([And(hist[i]==0, topic[i]==0) for i in range(4)])

# Option B: Garcia gives sculptures => hist[i]==1 and topic[i]==2 for some i
opt_b = Or([And(hist[i]==1, topic[i]==2) for i in range(4)])

# Option C: Garcia gives watercolors => hist[i]==1 and topic[i]==3 for some i
opt_c = Or([And(hist[i]==1, topic[i]==3) for i in range(4)])

# Option D: Holden gives oil paintings => hist[i]==2 and topic[i]==1 for some i
opt_d = Or([And(hist[i]==2, topic[i]==1) for i in range(4)])

# Option E: Jiang gives watercolors => hist[i]==3 and topic[i]==3 for some i
opt_e = Or([And(hist[i]==3, topic[i]==3) for i in range(4)])

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