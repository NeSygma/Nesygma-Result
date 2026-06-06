from z3 import *

# Define historian indices
Farley, Garcia, Holden, Jiang = 0, 1, 2, 3
historians = [Farley, Garcia, Holden, Jiang]

# Define topic indices
lithographs, oil_paintings, sculptures, watercolors = 0, 1, 2, 3

# Variables: assign_historian[h] = topic given by historian h
assign_historian = [Int(f'assign_{h}') for h in historians]
# Variables: time[h] = time slot of historian h (0..3)
time = [Int(f'time_{h}') for h in historians]

# Auxiliary variables for topic times
oil_time = Int('oil_time')
litho_time = Int('litho_time')
water_time = Int('water_time')

solver = Solver()

# Domain constraints for assign_historian: each topic 0..3
for h in historians:
    solver.add(assign_historian[h] >= 0, assign_historian[h] <= 3)

# All historians give different topics
solver.add(Distinct(assign_historian))

# Domain constraints for time: 0..3
for h in historians:
    solver.add(time[h] >= 0, time[h] <= 3)

# All times distinct
solver.add(Distinct(time))

# Define oil_time, litho_time, water_time
# oil_time is the time of the historian who gives oil paintings (topic 1)
solver.add(Or([And(assign_historian[h] == oil_paintings, oil_time == time[h]) for h in historians]))
# litho_time is the time of the historian who gives lithographs (topic 0)
solver.add(Or([And(assign_historian[h] == lithographs, litho_time == time[h]) for h in historians]))
# water_time is the time of the historian who gives watercolors (topic 3)
solver.add(Or([And(assign_historian[h] == watercolors, water_time == time[h]) for h in historians]))

# Constraint: oil paintings and watercolors earlier than lithographs
solver.add(oil_time < litho_time)
solver.add(water_time < litho_time)

# Constraint: Farley's lecture earlier than oil paintings
solver.add(time[Farley] < oil_time)

# Constraint: Holden earlier than Garcia and Jiang
solver.add(time[Holden] < time[Garcia])
solver.add(time[Holden] < time[Jiang])

# Now define option constraints
opt_a_constr = (assign_historian[Farley] == lithographs)
opt_b_constr = (assign_historian[Garcia] == sculptures)
opt_c_constr = (assign_historian[Garcia] == watercolors)
opt_d_constr = (assign_historian[Holden] == oil_paintings)
opt_e_constr = (assign_historian[Jiang] == watercolors)

# Use the exact skeleton
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:  # Changed to unsat because we want the option that cannot be true
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