from z3 import *

solver = Solver()

# Historians: F=0, G=1, H=2, J=3
# Topics: lith=0, oil=1, sculp=2, water=3
# Time slots: 1, 2, 3, 4

# slot[h] = time slot assigned to historian h
slot = [Int(f'slot_{h}') for h in range(4)]
# topic[h] = topic assigned to historian h
topic = [Int(f'topic_{h}') for h in range(4)]

# Domain constraints
for h in range(4):
    solver.add(And(slot[h] >= 1, slot[h] <= 4))
    solver.add(And(topic[h] >= 0, topic[h] <= 3))

# All slots distinct, all topics distinct
solver.add(Distinct(slot))
solver.add(Distinct(topic))

# Helper: position of a given topic (symbolic lookup)
def topic_pos(t):
    """Returns the time slot of whichever historian has topic t."""
    p = Int(f'pos_topic_{t}')
    solver.add(Or([And(topic[h] == t, p == slot[h]) for h in range(4)]))
    return p

oil_pos = topic_pos(1)   # oil paintings
lith_pos = topic_pos(0)   # lithographs
water_pos = topic_pos(3)  # watercolors

# Constraint 1: oil paintings earlier than lithographs
solver.add(oil_pos < lith_pos)

# Constraint 2: watercolors earlier than lithographs
solver.add(water_pos < lith_pos)

# Constraint 3: Farley's lecture earlier than oil paintings lecture
solver.add(slot[0] < oil_pos)

# Constraint 4: Holden earlier than Garcia
solver.add(slot[2] < slot[1])

# Constraint 5: Holden earlier than Jiang
solver.add(slot[2] < slot[3])

# Now check each option: which CANNOT be true?
# (A) Farley gives lithographs → topic[0] == 0
# (B) Garcia gives sculptures → topic[1] == 2
# (C) Garcia gives watercolors → topic[1] == 3
# (D) Holden gives oil paintings → topic[2] == 1
# (E) Jiang gives watercolors → topic[3] == 3

options = [
    ("A", topic[0] == 0),
    ("B", topic[1] == 2),
    ("C", topic[1] == 3),
    ("D", topic[2] == 1),
    ("E", topic[3] == 3),
]

found_cannot = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        found_cannot.append(letter)
        print(f"Option {letter}: UNSAT (CANNOT be true)")
    elif result == sat:
        m = solver.model()
        print(f"Option {letter}: SAT (CAN be true) - slots: {[m[slot[i]] for i in range(4)]}, topics: {[m[topic[i]] for i in range(4)]}")
    else:
        print(f"Option {letter}: unknown")
    solver.pop()

print()
if len(found_cannot) == 1:
    print("STATUS: sat")
    print(f"answer:{found_cannot[0]}")
elif len(found_cannot) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options CANNOT be true: {found_cannot}")
else:
    print("STATUS: unsat")
    print("Refine: No options found as impossible")