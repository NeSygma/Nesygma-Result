from z3 import *

solver = Solver()

# Historians
hist_names = ['Farley', 'Garcia', 'Holden', 'Jiang']
# Position variables 1..4
pos = {h: Int(f'pos_{h}') for h in hist_names}
for h in hist_names:
    solver.add(pos[h] >= 1, pos[h] <= 4)
# All positions distinct
solver.add(Distinct([pos[h] for h in hist_names]))

# Topic indices: 0 lithographs, 1 oil, 2 sculptures, 3 watercolors
topic = {h: Int(f'topic_{h}') for h in hist_names}
for h in hist_names:
    solver.add(topic[h] >= 0, topic[h] <= 3)
solver.add(Distinct([topic[h] for h in hist_names]))

# Garcia gives sculptures (topic 2)
solver.add(topic['Garcia'] == 2)

# Position variables for each topic
lith_pos = Int('lith_pos')
oil_pos = Int('oil_pos')
scul_pos = Int('scul_pos')
water_pos = Int('water_pos')
# Each topic position between 1 and 4
for tp in [lith_pos, oil_pos, scul_pos, water_pos]:
    solver.add(tp >= 1, tp <= 4)
# All topic positions distinct (since each historian distinct topic)
solver.add(Distinct(lith_pos, oil_pos, scul_pos, water_pos))

# Link topic positions to historian positions using Or-Loop pattern
for h in hist_names:
    # lithographs = 0
    solver.add(Implies(topic[h] == 0, lith_pos == pos[h]))
    solver.add(Implies(topic[h] == 1, oil_pos == pos[h]))
    solver.add(Implies(topic[h] == 2, scul_pos == pos[h]))
    solver.add(Implies(topic[h] == 3, water_pos == pos[h]))

# Base constraints
solver.add(oil_pos < lith_pos)
solver.add(water_pos < lith_pos)
solver.add(pos['Farley'] < oil_pos)
solver.add(pos['Holden'] < pos['Garcia'])
solver.add(pos['Holden'] < pos['Jiang'])

# Define option constraints
opt_a = lith_pos == 3  # A: lithographs lecture is third
opt_b = oil_pos == 3   # B: oil paintings lecture is third
opt_c = scul_pos == 1  # C: sculptures lecture is first
opt_d = scul_pos == 2  # D: sculptures lecture is second
opt_e = water_pos == 2 # E: watercolors lecture is second

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