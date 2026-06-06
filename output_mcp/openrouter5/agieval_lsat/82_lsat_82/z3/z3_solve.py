from z3 import *

# Seven sales representatives
reps = ["Kim", "Mahr", "Parra", "Quinn", "Stuckey", "Tiao", "Udall"]

# Zones: 1, 2, 3
# We'll assign each rep a zone number (1, 2, or 3)
zone = {r: Int(f"zone_{r}") for r in reps}

solver = Solver()

# Domain: each rep works in exactly one zone, zones are 1, 2, or 3
for r in reps:
    solver.add(Or(zone[r] == 1, zone[r] == 2, zone[r] == 3))

# Condition 1: Either Parra or Tiao (but not both) works in Zone 1.
solver.add(Or(
    And(zone["Parra"] == 1, zone["Tiao"] != 1),
    And(zone["Tiao"] == 1, zone["Parra"] != 1)
))

# Condition 2: Either Tiao or Udall (but not both) works in Zone 2.
solver.add(Or(
    And(zone["Tiao"] == 2, zone["Udall"] != 2),
    And(zone["Udall"] == 2, zone["Tiao"] != 2)
))

# Condition 3: Parra and Quinn work in the same sales zone as each other.
solver.add(zone["Parra"] == zone["Quinn"])

# Condition 4: Stuckey and Udall work in the same sales zone as each other.
solver.add(zone["Stuckey"] == zone["Udall"])

# Condition 5: There are more of the sales representatives working in Zone 3 than in Zone 2.
# Count reps in Zone 3 > count reps in Zone 2
count_zone3 = Sum([If(zone[r] == 3, 1, 0) for r in reps])
count_zone2 = Sum([If(zone[r] == 2, 1, 0) for r in reps])
solver.add(count_zone3 > count_zone2)

# Now evaluate each option
# Each option gives a mapping of reps to zones.
# We'll encode each option as a set of constraints.

def make_option_constr(zone1_list, zone2_list, zone3_list):
    """Return a constraint that matches the given assignment."""
    constrs = []
    for r in zone1_list:
        constrs.append(zone[r] == 1)
    for r in zone2_list:
        constrs.append(zone[r] == 2)
    for r in zone3_list:
        constrs.append(zone[r] == 3)
    return And(constrs)

# Option A: Zone 1: Kim, Parra | Zone 2: Stuckey, Udall | Zone 3: Mahr, Quinn, Tiao
opt_a = make_option_constr(["Kim", "Parra"], ["Stuckey", "Udall"], ["Mahr", "Quinn", "Tiao"])

# Option B: Zone 1: Kim, Tiao | Zone 2: Stuckey, Udall | Zone 3: Mahr, Parra, Quinn
opt_b = make_option_constr(["Kim", "Tiao"], ["Stuckey", "Udall"], ["Mahr", "Parra", "Quinn"])

# Option C: Zone 1: Parra, Quinn | Zone 2: Kim, Udall | Zone 3: Mahr, Stuckey, Tiao
opt_c = make_option_constr(["Parra", "Quinn"], ["Kim", "Udall"], ["Mahr", "Stuckey", "Tiao"])

# Option D: Zone 1: Stuckey, Udall | Zone 2: Kim, Tiao | Zone 3: Mahr, Parra, Quinn
opt_d = make_option_constr(["Stuckey", "Udall"], ["Kim", "Tiao"], ["Mahr", "Parra", "Quinn"])

# Option E: Zone 1: Tiao | Zone 2: Kim, Parra, Quinn | Zone 3: Stuckey, Udall
opt_e = make_option_constr(["Tiao"], ["Kim", "Parra", "Quinn"], ["Stuckey", "Udall"])

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