from z3 import *

solver = Solver()

# Use integer encoding:
# Historians: 0=Farley, 1=Garcia, 2=Holden, 3=Jiang
# Topics: 0=lithographs, 1=oil_paintings, 2=sculptures, 3=watercolors

hist = [Int(f'hist_{i}') for i in range(4)]  # hist[i] = historian at position i (0-indexed)
topic = [Int(f'topic_{i}') for i in range(4)]  # topic[i] = topic at position i (0-indexed)

for i in range(4):
    solver.add(hist[i] >= 0, hist[i] <= 3)
    solver.add(topic[i] >= 0, topic[i] <= 3)

solver.add(Distinct(hist))
solver.add(Distinct(topic))

# Constraint: Garcia gives the sculptures lecture
# Garcia is historian 1, sculptures is topic 2
for i in range(4):
    solver.add(Implies(hist[i] == 1, topic[i] == 2))

# Helper: position of a topic (0-indexed position)
def pos_of_topic(t):
    return Sum([If(topic[i] == t, i, 0) for i in range(4)])

# Helper: position of a historian (0-indexed position)
def pos_of_hist(h):
    return Sum([If(hist[i] == h, i, 0) for i in range(4)])

# Oil paintings (1) and watercolors (3) must both be earlier than lithographs (0)
solver.add(pos_of_topic(1) < pos_of_topic(0))
solver.add(pos_of_topic(3) < pos_of_topic(0))

# Farley (0) must be earlier than oil paintings (1)
solver.add(pos_of_hist(0) < pos_of_topic(1))

# Holden (2) must be earlier than both Garcia (1) and Jiang (3)
solver.add(pos_of_hist(2) < pos_of_hist(1))
solver.add(pos_of_hist(2) < pos_of_hist(3))

# Now evaluate each option
# (A) The lithographs lecture is third. (position index 2)
opt_a = (pos_of_topic(0) == 2)

# (B) The oil paintings lecture is third. (position index 2)
opt_b = (pos_of_topic(1) == 2)

# (C) The sculptures lecture is first. (position index 0)
opt_c = (pos_of_topic(2) == 0)

# (D) The sculptures lecture is second. (position index 1)
opt_d = (pos_of_topic(2) == 1)

# (E) The watercolors lecture is second. (position index 1)
opt_e = (pos_of_topic(3) == 1)

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