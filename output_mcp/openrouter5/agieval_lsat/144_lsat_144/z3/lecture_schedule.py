from z3 import *

# We have 4 positions (1st, 2nd, 3rd, 4th) and 4 historians and 4 topics.
# Let's model this as: for each historian, assign a position (1-4) and a topic.
# But the answer choices give specific assignments of historian:topic in order.
# So we can model positions 1-4, and for each position assign a historian and a topic.

# Positions: 1=first, 2=second, 3=third, 4=fourth
positions = [1, 2, 3, 4]

# Historians
Farley, Garcia, Holden, Jiang = Ints('Farley Garcia Holden Jiang')
historians = [Farley, Garcia, Holden, Jiang]

# Topics: 0=lithographs, 1=oil paintings, 2=sculptures, 3=watercolors
# We'll use Ints for topics assigned to each position
topics = [Int(f'topic_{i}') for i in range(1, 5)]  # topic_1 through topic_4

solver = Solver()

# Each historian gets a unique position 1-4
solver.add(Distinct(historians))
for h in historians:
    solver.add(h >= 1, h <= 4)

# Each topic appears exactly once across the 4 positions
solver.add(Distinct(topics))
for t in topics:
    solver.add(t >= 0, t <= 3)

# Constraint 1: oil paintings (1) and watercolors (3) must both be earlier than lithographs (0)
# oil position < lithograph position
oil_pos = Int('oil_pos')
water_pos = Int('water_pos')
litho_pos = Int('litho_pos')

# Link topic to position
for i in range(1, 5):
    solver.add(Implies(topics[i-1] == 1, oil_pos == i))
    solver.add(Implies(topics[i-1] == 3, water_pos == i))
    solver.add(Implies(topics[i-1] == 0, litho_pos == i))

solver.add(oil_pos < litho_pos)
solver.add(water_pos < litho_pos)

# Constraint 2: Farley's lecture must be earlier than the oil paintings lecture
solver.add(Farley < oil_pos)

# Constraint 3: Holden's lecture must be earlier than both Garcia's and Jiang's lectures
solver.add(Holden < Garcia)
solver.add(Holden < Jiang)

# Now evaluate each answer choice
# Each choice gives an ordering from 1st to 4th: (historian: topic)

# Helper: for a given ordering list of (historian, topic) pairs for positions 1..4,
# create a constraint that matches that ordering.

def make_choice_constraint(order):
    """order is a list of (historian_var, topic_val) for positions 1,2,3,4"""
    constr = True
    for pos_idx, (hist_var, topic_val) in enumerate(order):
        pos = pos_idx + 1
        # historian must be at this position
        constr = And(constr, hist_var == pos)
        # topic at this position must be the given topic
        constr = And(constr, topics[pos_idx] == topic_val)
    return constr

# Topic encoding: 0=lithographs, 1=oil paintings, 2=sculptures, 3=watercolors
# Choice A: Farley: sculptures(2); Holden: lithographs(0); Garcia: oil paintings(1); Jiang: watercolors(3)
opt_a = make_choice_constraint([
    (Farley, 2), (Holden, 0), (Garcia, 1), (Jiang, 3)
])

# Choice B: Farley: watercolors(3); Jiang: oil paintings(1); Holden: sculptures(2); Garcia: lithographs(0)
opt_b = make_choice_constraint([
    (Farley, 3), (Jiang, 1), (Holden, 2), (Garcia, 0)
])

# Choice C: Garcia: sculptures(2); Farley: watercolors(3); Holden: oil paintings(1); Jiang: lithographs(0)
opt_c = make_choice_constraint([
    (Garcia, 2), (Farley, 3), (Holden, 1), (Jiang, 0)
])

# Choice D: Holden: oil paintings(1); Jiang: watercolors(3); Farley: lithographs(0); Garcia: sculptures(2)
opt_d = make_choice_constraint([
    (Holden, 1), (Jiang, 3), (Farley, 0), (Garcia, 2)
])

# Choice E: Holden: sculptures(2); Farley: watercolors(3); Jiang: oil paintings(1); Garcia: lithographs(0)
opt_e = make_choice_constraint([
    (Holden, 2), (Farley, 3), (Jiang, 1), (Garcia, 0)
])

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