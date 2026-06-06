from z3 import *

solver = Solver()

# Variables: position (1-4) for each historian and each topic
# Historians: Farley, Garcia, Holden, Jiang
F, G, H, J = Ints('F G H J')
# Topics: lithographs, oil paintings, sculptures, watercolors
L, O, S, W = Ints('L O S W')

# All positions are 1-4
for v in [F, G, H, J, L, O, S, W]:
    solver.add(v >= 1, v <= 4)

# All historians in different positions
solver.add(Distinct(F, G, H, J))
# All topics in different positions
solver.add(Distinct(L, O, S, W))

# Each historian gives exactly one topic at their position
# We need to model the assignment: which topic each historian gives
# Let's use arrays to map position -> topic and position -> historian
# Actually, we need to know which historian gives which topic
# Let's define: topic_of[historian] = topic
# We'll use Int variables for the topic each historian gives
# Topics encoded as: 0=lithographs, 1=oil paintings, 2=sculptures, 3=watercolors
topic_F = Int('topic_F')
topic_G = Int('topic_G')
topic_H = Int('topic_H')
topic_J = Int('topic_J')

for t in [topic_F, topic_G, topic_H, topic_J]:
    solver.add(t >= 0, t <= 3)
solver.add(Distinct(topic_F, topic_G, topic_H, topic_J))

# Map topic numbers to positions
# If historian gives topic X, then their position equals the position of topic X
# topic 0 = lithographs -> position L
# topic 1 = oil paintings -> position O
# topic 2 = sculptures -> position S
# topic 3 = watercolors -> position W

solver.add(If(topic_F == 0, F == L, If(topic_F == 1, F == O, If(topic_F == 2, F == S, F == W))))
solver.add(If(topic_G == 0, G == L, If(topic_G == 1, G == O, If(topic_G == 2, G == S, G == W))))
solver.add(If(topic_H == 0, H == L, If(topic_H == 1, H == O, If(topic_H == 2, H == S, H == W))))
solver.add(If(topic_J == 0, J == L, If(topic_J == 1, J == O, If(topic_J == 2, J == S, J == W))))

# Constraints:
# 1. Oil paintings and watercolors both earlier than lithographs
solver.add(O < L)
solver.add(W < L)

# 2. Farley's lecture earlier than oil paintings
solver.add(F < O)

# 3. Holden's lecture earlier than both Garcia's and Jiang's
solver.add(H < G)
solver.add(H < J)

# 4. Watercolors lecture is third
solver.add(W == 3)

# Now evaluate each option
found_options = []

# Option A: Farley gives the watercolors lecture
opt_a = (topic_F == 3)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Garcia gives the oil paintings lecture
opt_b = (topic_G == 1)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Garcia gives the sculptures lecture
opt_c = (topic_G == 2)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Holden gives the sculptures lecture
opt_d = (topic_H == 2)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Jiang gives the lithographs lecture
opt_e = (topic_J == 0)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append("E")
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