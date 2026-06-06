from z3 import *

solver = Solver()

# Declare topic indices (0: lithographs, 1: oil_paintings, 2: watercolors, 3: sculptures)
farley_topic = Int('farley_topic')
garcia_topic = Int('garcia_topic')
holden_topic = Int('holden_topic')
jiang_topic = Int('jiang_topic')

# All-different topics
solver.add(Distinct([farley_topic, garcia_topic, holden_topic, jiang_topic]))

# Position variables for each topic (1..4)
pos_lith = Int('pos_lith')
pos_oil = Int('pos_oil')
pos_water = Int('pos_water')
pos_sculpt = Int('pos_sculpt')

# Domain constraints
for p in [pos_lith, pos_oil, pos_water, pos_sculpt]:
    solver.add(p >= 1, p <= 4)
# All-different positions
solver.add(Distinct([pos_lith, pos_oil, pos_water, pos_sculpt]))

# Ordering constraints: oil and water before lith
solver.add(pos_oil < pos_lith)
solver.add(pos_water < pos_lith)

# Farley earlier than oil
farley_pos = If(farley_topic == 0, pos_lith,
                If(farley_topic == 1, pos_oil,
                   If(farley_topic == 2, pos_water,
                      pos_sculpt)))
solver.add(farley_pos < pos_oil)

# Holden earlier than Garcia and Jiang
holden_pos = If(holden_topic == 0, pos_lith,
                If(holden_topic == 1, pos_oil,
                   If(holden_topic == 2, pos_water,
                      pos_sculpt)))
garcia_pos = If(garcia_topic == 0, pos_lith,
                If(garcia_topic == 1, pos_oil,
                   If(garcia_topic == 2, pos_water,
                      pos_sculpt)))
jiang_pos = If(jiang_topic == 0, pos_lith,
                If(jiang_topic == 1, pos_oil,
                   If(jiang_topic == 2, pos_water,
                      pos_sculpt)))
solver.add(holden_pos < garcia_pos)
solver.add(holden_pos < jiang_pos)

# Define options
opt_a_constr = farley_topic == 0  # A: Farley gives lithographs
opt_b_constr = garcia_topic == 3  # B: Garcia gives sculptures
opt_c_constr = garcia_topic == 2  # C: Garcia gives watercolors
opt_d_constr = holden_topic == 1  # D: Holden gives oil paintings
opt_e_constr = jiang_topic == 2   # E: Jiang gives watercolors

# Evaluate each option
found_options = []
for letter, constr in [('A', opt_a_constr), ('B', opt_b_constr), ('C', opt_c_constr), ('D', opt_d_constr), ('E', opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Skeleton block (exact copy)
if len(found_options) == 1:
    print('STATUS: sat')
    print(f'answer:{found_options[0]}')
elif len(found_options) > 1:
    print('STATUS: unsat')
    print(f'Refine: Multiple options found {found_options}')
else:
    print('STATUS: unsat')
    print('Refine: No options found')