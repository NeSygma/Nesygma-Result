from z3 import *

# Historians: 0:Farley, 1:Garcia, 2:Holden, 3:Jiang
# Topics: 0:Lithographs, 1:Oil paintings, 2:Sculptures, 3:Watercolors
# Time slots: 0, 1, 2, 3

solver = Solver()

hist_at = [Int(f'hist_at_{t}') for t in range(4)]
topic_at = [Int(f'topic_at_{t}') for t in range(4)]

for t in range(4):
    solver.add(hist_at[t] >= 0, hist_at[t] <= 3)
    solver.add(topic_at[t] >= 0, topic_at[t] <= 3)

solver.add(Distinct(hist_at))
solver.add(Distinct(topic_at))

def get_time_of_hist(h):
    return Sum([If(hist_at[t] == h, t, 0) for t in range(4)])

def get_time_of_topic(top):
    return Sum([If(topic_at[t] == top, t, 0) for t in range(4)])

# Constraints
solver.add(get_time_of_topic(1) < get_time_of_topic(0))
solver.add(get_time_of_topic(3) < get_time_of_topic(0))
solver.add(get_time_of_hist(0) < get_time_of_topic(1))
solver.add(get_time_of_hist(2) < get_time_of_hist(1))
solver.add(get_time_of_hist(2) < get_time_of_hist(3))
solver.add(get_time_of_topic(3) == 2)

# Helper to check if historian h gives topic top
def hist_gives_topic(h, top):
    return Or([And(hist_at[t] == h, topic_at[t] == top) for t in range(4)])

options = [
    ("A", hist_gives_topic(0, 3)),
    ("B", hist_gives_topic(1, 1)),
    ("C", hist_gives_topic(1, 2)),
    ("D", hist_gives_topic(2, 2)),
    ("E", hist_gives_topic(3, 0))
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