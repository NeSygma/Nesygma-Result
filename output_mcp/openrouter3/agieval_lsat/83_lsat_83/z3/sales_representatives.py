from z3 import *

# Create solver
solver = Solver()

# Define the seven sales representatives
reps = ["Kim", "Mahr", "Parra", "Quinn", "Stuckey", "Tiao", "Udall"]

# Create a mapping from rep name to index
rep_index = {name: i for i, name in enumerate(reps)}

# Create variables: zone[i] = zone assignment for rep i (0=Zone1, 1=Zone2, 2=Zone3)
zone = [Int(f"zone_{i}") for i in range(7)]

# Add domain constraints: each zone must be 0, 1, or 2
for i in range(7):
    solver.add(Or(zone[i] == 0, zone[i] == 1, zone[i] == 2))

# Condition 1: Either Parra or Tiao (but not both) works in Zone 1
# Parra is index 2, Tiao is index 5
parra_zone1 = (zone[2] == 0)
tiao_zone1 = (zone[5] == 0)
solver.add(Or(parra_zone1, tiao_zone1))  # At least one
solver.add(Not(And(parra_zone1, tiao_zone1)))  # Not both

# Condition 2: Either Tiao or Udall (but not both) works in Zone 2
# Tiao is index 5, Udall is index 6
tiao_zone2 = (zone[5] == 1)
udall_zone2 = (zone[6] == 1)
solver.add(Or(tiao_zone2, udall_zone2))  # At least one
solver.add(Not(And(tiao_zone2, udall_zone2)))  # Not both

# Condition 3: Parra and Quinn work in the same sales zone as each other
# Parra is index 2, Quinn is index 3
solver.add(zone[2] == zone[3])

# Condition 4: Stuckey and Udall work in the same sales zone as each other
# Stuckey is index 4, Udall is index 6
solver.add(zone[4] == zone[6])

# Condition 5: There are more of the sales representatives working in Zone 3 than in Zone 2
# Count reps in each zone
zone1_count = Sum([If(zone[i] == 0, 1, 0) for i in range(7)])
zone2_count = Sum([If(zone[i] == 1, 1, 0) for i in range(7)])
zone3_count = Sum([If(zone[i] == 2, 1, 0) for i in range(7)])
solver.add(zone3_count > zone2_count)

# Additional constraint from the question: "If more sales representatives work in Zone 1 than in Zone 3"
# This is the premise we need to assume for evaluating the answer choices
premise = (zone1_count > zone3_count)
solver.add(premise)

# Now evaluate each answer choice
# Answer choices:
# (A) Kim works in Zone 2
# (B) Mahr works in Zone 2
# (C) Parra works in Zone 3
# (D) Tiao works in Zone 1
# (E) Udall works in Zone 3

# Define constraints for each option
opt_a_constr = (zone[0] == 1)  # Kim (index 0) in Zone 2
opt_b_constr = (zone[1] == 1)  # Mahr (index 1) in Zone 2
opt_c_constr = (zone[2] == 2)  # Parra (index 2) in Zone 3
opt_d_constr = (zone[5] == 0)  # Tiao (index 5) in Zone 1
opt_e_constr = (zone[6] == 2)  # Udall (index 6) in Zone 3

# Test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
    # Also print the model for verification
    solver.check()
    m = solver.model()
    print("\nModel verification:")
    for i, name in enumerate(reps):
        zone_val = m[zone[i]]
        zone_name = ["Zone 1", "Zone 2", "Zone 3"][zone_val.as_long()]
        print(f"{name}: {zone_name}")
    print(f"\nZone counts:")
    print(f"Zone 1: {zone1_count}")
    print(f"Zone 2: {zone2_count}")
    print(f"Zone 3: {zone3_count}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")