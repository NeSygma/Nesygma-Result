from z3 import *

solver = Solver()

# Historians: Farley=0, Garcia=1, Holden=2, Jiang=3
# Topics: lithographs=0, oil_paintings=1, sculptures=2, watercolors=3
# Positions: 1, 2, 3, 4

# Each historian has a position (1-4) and a topic (0-3)
pos = [Int(f'pos_{h}') for h in ['Farley', 'Garcia', 'Holden', 'Jiang']]
topic = [Int(f'topic_{h}') for h in ['Farley', 'Garcia', 'Holden', 'Jiang']]

# Domain constraints
for i in range(4):
    solver.add(pos[i] >= 1, pos[i] <= 4)
    solver.add(topic[i] >= 0, topic[i] <= 3)

# All positions distinct, all topics distinct
solver.add(Distinct(pos))
solver.add(Distinct(topic))

# Helper: position of whoever gives a specific topic
def pos_of_topic(t):
    return If(topic[0] == t, pos[0],
           If(topic[1] == t, pos[1],
           If(topic[2] == t, pos[2],
              pos[3])))

# Constraint 1: oil paintings and watercolors both earlier than lithographs
solver.add(pos_of_topic(1) < pos_of_topic(0))  # oil < lithographs
solver.add(pos_of_topic(3) < pos_of_topic(0))  # watercolors < lithographs

# Constraint 2: Farley's lecture earlier than oil paintings lecture
solver.add(pos[0] < pos_of_topic(1))  # Farley < oil paintings

# Constraint 3: Holden earlier than both Garcia and Jiang
solver.add(pos[2] < pos[1])  # Holden < Garcia
solver.add(pos[2] < pos[3])  # Holden < Jiang

# Now define each option as constraints
# Option A: Farley: sculptures(2); Holden: lithographs(0); Garcia: oil_paintings(1); Jiang: watercolors(3)
# Order: 1st=Farley, 2nd=Holden, 3rd=Garcia, 4th=Jiang
opt_a = And(
    pos[0] == 1, topic[0] == 2,  # Farley: sculptures, 1st
    pos[2] == 2, topic[2] == 0,  # Holden: lithographs, 2nd
    pos[1] == 3, topic[1] == 1,  # Garcia: oil paintings, 3rd
    pos[3] == 4, topic[3] == 3   # Jiang: watercolors, 4th
)

# Option B: Farley: watercolors(3); Jiang: oil_paintings(1); Holden: sculptures(2); Garcia: lithographs(0)
# Order: 1st=Farley, 2nd=Jiang, 3rd=Holden, 4th=Garcia
opt_b = And(
    pos[0] == 1, topic[0] == 3,  # Farley: watercolors, 1st
    pos[3] == 2, topic[3] == 1,  # Jiang: oil paintings, 2nd
    pos[2] == 3, topic[2] == 2,  # Holden: sculptures, 3rd
    pos[1] == 4, topic[1] == 0   # Garcia: lithographs, 4th
)

# Option C: Garcia: sculptures(2); Farley: watercolors(3); Holden: oil_paintings(1); Jiang: lithographs(0)
# Order: 1st=Garcia, 2nd=Farley, 3rd=Holden, 4th=Jiang
opt_c = And(
    pos[1] == 1, topic[1] == 2,  # Garcia: sculptures, 1st
    pos[0] == 2, topic[0] == 3,  # Farley: watercolors, 2nd
    pos[2] == 3, topic[2] == 1,  # Holden: oil paintings, 3rd
    pos[3] == 4, topic[3] == 0   # Jiang: lithographs, 4th
)

# Option D: Holden: oil_paintings(1); Jiang: watercolors(3); Farley: lithographs(0); Garcia: sculptures(2)
# Order: 1st=Holden, 2nd=Jiang, 3rd=Farley, 4th=Garcia
opt_d = And(
    pos[2] == 1, topic[2] == 1,  # Holden: oil paintings, 1st
    pos[3] == 2, topic[3] == 3,  # Jiang: watercolors, 2nd
    pos[0] == 3, topic[0] == 0,  # Farley: lithographs, 3rd
    pos[1] == 4, topic[1] == 2   # Garcia: sculptures, 4th
)

# Option E: Holden: sculptures(2); Farley: watercolors(3); Jiang: oil_paintings(1); Garcia: lithographs(0)
# Order: 1st=Holden, 2nd=Farley, 3rd=Jiang, 4th=Garcia
opt_e = And(
    pos[2] == 1, topic[2] == 2,  # Holden: sculptures, 1st
    pos[0] == 2, topic[0] == 3,  # Farley: watercolors, 2nd
    pos[3] == 3, topic[3] == 1,  # Jiang: oil paintings, 3rd
    pos[1] == 4, topic[1] == 0   # Garcia: lithographs, 4th
)

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