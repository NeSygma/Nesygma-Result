from z3 import *

solver = Solver()

# positions 0,1,2,3 (0=earliest, 3=latest)
# historians: 0=Farley, 1=Garcia, 2=Holden, 3=Jiang
# topics: 0=Lithographs, 1=Oil, 2=Sculptures, 3=Watercolors

hist = [Int(f"hist_{i}") for i in range(4)]
topic = [Int(f"topic_{i}") for i in range(4)]

# Domain constraints
for i in range(4):
    solver.add(hist[i] >= 0, hist[i] <= 3)
    solver.add(topic[i] >= 0, topic[i] <= 3)

# All distinct
solver.add(Distinct(hist))
solver.add(Distinct(topic))

# Constraint 1: Oil (topic=1) < Litho (topic=0) and Water (topic=3) < Litho (topic=0)
# Set positions for each topic
oil_pos = Int('oil_pos')
litho_pos = Int('litho_pos')
water_pos = Int('water_pos')

solver.add(Or([And(topic[i] == 1, oil_pos == i) for i in range(4)]))
solver.add(Or([And(topic[i] == 0, litho_pos == i) for i in range(4)]))
solver.add(Or([And(topic[i] == 3, water_pos == i) for i in range(4)]))

solver.add(oil_pos < litho_pos)
solver.add(water_pos < litho_pos)

# Constraint 2: Farley (hist=0) < Oil (topic=1)
farley_pos = Int('farley_pos')
solver.add(Or([And(hist[i] == 0, farley_pos == i) for i in range(4)]))
solver.add(farley_pos < oil_pos)

# Constraint 3: Holden (hist=2) < Garcia (hist=1) and Holden < Jiang (hist=3)
holden_pos = Int('holden_pos')
garcia_pos = Int('garcia_pos')
jiang_pos = Int('jiang_pos')

solver.add(Or([And(hist[i] == 2, holden_pos == i) for i in range(4)]))
solver.add(Or([And(hist[i] == 1, garcia_pos == i) for i in range(4)]))
solver.add(Or([And(hist[i] == 3, jiang_pos == i) for i in range(4)]))

solver.add(holden_pos < garcia_pos)
solver.add(holden_pos < jiang_pos)

# Sculptures position
sculpt_pos = Int('sculpt_pos')
solver.add(Or([And(topic[i] == 2, sculpt_pos == i) for i in range(4)]))

# Evaluate each option: check if NOT(option) is UNSAT
# If so, the option MUST be true
found_options = []
for letter, constr in [
    ("A", farley_pos < sculpt_pos),
    ("B", holden_pos < litho_pos),
    ("C", sculpt_pos < garcia_pos),
    ("D", sculpt_pos < jiang_pos),
    ("E", water_pos < garcia_pos)
]:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
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