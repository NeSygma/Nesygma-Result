from z3 import *

solver = Solver()

# Historians: Farley=0, Garcia=1, Holden=2, Jiang=3
# Topics: lithographs=0, oil_paintings=1, sculptures=2, watercolors=3

# Time slot for each historian (1-4)
time = [Int(f'time_{h}') for h in range(4)]
hnames = ['Farley', 'Garcia', 'Holden', 'Jiang']

# Time slot for each topic (1-4)
topic_time = [Int(f'topic_time_{t}') for t in range(4)]
tnames = ['lithographs', 'oil_paintings', 'sculptures', 'watercolors']

# Domain constraints
for i in range(4):
    solver.add(And(time[i] >= 1, time[i] <= 4))
    solver.add(And(topic_time[i] >= 1, topic_time[i] <= 4))

# All distinct
solver.add(Distinct(time))
solver.add(Distinct(topic_time))

# Link: historian h gives topic t iff time[h] == topic_time[t]
# Each historian gives exactly one topic, each topic given by exactly one historian
# This is automatically enforced by: time and topic_time are both permutations of {1,2,3,4}
# So at each time slot, exactly one historian and exactly one topic coincide.

# Constraint 1: oil paintings earlier than lithographs
solver.add(topic_time[1] < topic_time[0])  # oil < lith

# Constraint 2: watercolors earlier than lithographs
solver.add(topic_time[3] < topic_time[0])  # water < lith

# Constraint 3: Farley's lecture earlier than oil paintings lecture
solver.add(time[0] < topic_time[1])  # Farley < oil

# Constraint 4: Holden earlier than Garcia
solver.add(time[2] < time[1])  # Holden < Garcia

# Constraint 5: Holden earlier than Jiang
solver.add(time[2] < time[3])  # Holden < Jiang

# Additional: watercolors is third
solver.add(topic_time[3] == 3)

# Answer choices:
# (A) Farley gives watercolors: time[Farley] == topic_time[watercolors]
opt_a = (time[0] == topic_time[3])
# (B) Garcia gives oil paintings: time[Garcia] == topic_time[oil]
opt_b = (time[1] == topic_time[1])
# (C) Garcia gives sculptures: time[Garcia] == topic_time[sculptures]
opt_c = (time[1] == topic_time[2])
# (D) Holden gives sculptures: time[Holden] == topic_time[sculptures]
opt_d = (time[2] == topic_time[2])
# (E) Jiang gives lithographs: time[Jiang] == topic_time[lithographs]
opt_e = (time[3] == topic_time[0])

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        m = solver.model()
        found_options.append(letter)
        print(f"Option {letter} is SAT:")
        for i in range(4):
            print(f"  {hnames[i]} at time {m[time[i]]}")
        for i in range(4):
            print(f"  {tnames[i]} at time {m[topic_time[i]]}")
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