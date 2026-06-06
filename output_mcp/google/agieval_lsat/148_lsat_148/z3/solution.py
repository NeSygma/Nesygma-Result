from z3 import *

# Historians: 0:Farley, 1:Garcia, 2:Holden, 3:Jiang
# Topics: 0:Lithographs, 1:Oil, 2:Sculptures, 3:Watercolors

solver = Solver()

# time_h[h] is the time slot (1-4) for historian h
time_h = [Int(f'time_h_{i}') for i in range(4)]
# time_t[t] is the time slot (1-4) for topic t
time_t = [Int(f'time_t_{i}') for i in range(4)]
# topic_h[h] is the topic (0-3) for historian h
topic_h = [Int(f'topic_h_{i}') for i in range(4)]

# Domains
for i in range(4):
    solver.add(time_h[i] >= 1, time_h[i] <= 4)
    solver.add(time_t[i] >= 1, time_t[i] <= 4)
    solver.add(topic_h[i] >= 0, topic_h[i] <= 3)

# All distinct
solver.add(Distinct(time_h))
solver.add(Distinct(time_t))
solver.add(Distinct(topic_h))

# Linking historian and topic
# If historian h gives topic t, then time_h[h] == time_t[t]
for h in range(4):
    for t in range(4):
        solver.add(Implies(topic_h[h] == t, time_h[h] == time_t[t]))

# Constraints
# 1. Oil (1) and Watercolors (3) earlier than Lithographs (0)
solver.add(time_t[1] < time_t[0])
solver.add(time_t[3] < time_t[0])

# 2. Farley (0) earlier than Oil (1)
solver.add(time_h[0] < time_t[1])

# 3. Holden (2) earlier than Garcia (1) and Jiang (3)
solver.add(time_h[2] < time_h[1])
solver.add(time_h[2] < time_h[3])

# 4. Garcia (1) gives Sculptures (2)
solver.add(topic_h[1] == 2)

# Options
# (A) Lithographs (0) is third (time_t[0] == 3)
# (B) Oil (1) is third (time_t[1] == 3)
# (C) Sculptures (2) is first (time_t[2] == 1)
# (D) Sculptures (2) is second (time_t[2] == 2)
# (E) Watercolors (3) is second (time_t[3] == 2)

options = [
    ("A", time_t[0] == 3),
    ("B", time_t[1] == 3),
    ("C", time_t[2] == 1),
    ("D", time_t[2] == 2),
    ("E", time_t[3] == 2)
]

found_options = []
for letter, constr in options:
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