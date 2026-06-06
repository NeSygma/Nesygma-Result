from z3 import *

solver = Solver()

# Historians: Farley=0, Garcia=1, Holden=2, Jiang=3
# Topics: lithographs=0, oil_paintings=1, sculptures=2, watercolors=3
# Time slots: 1, 2, 3, 4

# Position of each topic's lecture (time slot 1-4)
pos_topic = [Int(f'pos_topic_{t}') for t in ['lithographs', 'oil_paintings', 'sculptures', 'watercolors']]
# pos_topic[0]=lithographs, [1]=oil_paintings, [2]=sculptures, [3]=watercolors

# Position of each historian's lecture
pos_hist = [Int(f'pos_hist_{h}') for h in ['Farley', 'Garcia', 'Holden', 'Jiang']]
# pos_hist[0]=Farley, [1]=Garcia, [2]=Holden, [3]=Jiang

# Topic assigned to each historian (0-3)
topic_hist = [Int(f'topic_hist_{h}') for h in ['Farley', 'Garcia', 'Holden', 'Jiang']]

# Domain constraints: positions 1-4
for p in pos_topic:
    solver.add(p >= 1, p <= 4)
for p in pos_hist:
    solver.add(p >= 1, p <= 4)

# Domain constraints: topics 0-3
for t in topic_hist:
    solver.add(t >= 0, t <= 3)

# All topic positions are distinct
solver.add(Distinct(pos_topic))

# All historian positions are distinct
solver.add(Distinct(pos_hist))

# All historians get different topics
solver.add(Distinct(topic_hist))

# Each historian's position equals their topic's position
for h in range(4):
    # topic_hist[h] maps to the topic, and pos_hist[h] must equal pos_topic[topic_hist[h]]
    solver.add(Or([
        And(topic_hist[h] == t, pos_hist[h] == pos_topic[t])
        for t in range(4)
    ]))

# Constraint 1: Oil paintings earlier than lithographs
solver.add(pos_topic[1] < pos_topic[0])

# Constraint 2: Watercolors earlier than lithographs
solver.add(pos_topic[3] < pos_topic[0])

# Constraint 3: Farley earlier than oil paintings
solver.add(pos_hist[0] < pos_topic[1])

# Constraint 4: Holden earlier than Garcia
solver.add(pos_hist[2] < pos_hist[1])

# Constraint 5: Holden earlier than Jiang
solver.add(pos_hist[2] < pos_hist[3])

# Additional condition: Garcia gives sculptures
solver.add(topic_hist[1] == 2)  # Garcia's topic is sculptures

# Now evaluate each option
# (A) The lithographs lecture is third.
opt_a = (pos_topic[0] == 3)
# (B) The oil paintings lecture is third.
opt_b = (pos_topic[1] == 3)
# (C) The sculptures lecture is first.
opt_c = (pos_topic[2] == 1)
# (D) The sculptures lecture is second.
opt_d = (pos_topic[2] == 2)
# (E) The watercolors lecture is second.
opt_e = (pos_topic[3] == 2)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        topic_names = ['lithographs', 'oil_paintings', 'sculptures', 'watercolors']
        hist_names = ['Farley', 'Garcia', 'Holden', 'Jiang']
        for h in range(4):
            t = m[topic_hist[h]].as_long()
            p = m[pos_hist[h]].as_long()
            print(f"  {hist_names[h]}: topic={topic_names[t]}, position={p}")
        for t in range(4):
            p = m[pos_topic[t]].as_long()
            print(f"  {topic_names[t]}: position={p}")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")