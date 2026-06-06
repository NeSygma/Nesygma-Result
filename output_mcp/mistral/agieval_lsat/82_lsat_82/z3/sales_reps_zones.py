from z3 import *

# Base constraints solver
solver = Solver()

# Declare variables for each sales representative's zone
# 1 = Zone 1, 2 = Zone 2, 3 = Zone 3
Kim = Int('Kim')
Mahr = Int('Mahr')
Parra = Int('Parra')
Quinn = Int('Quinn')
Stuckey = Int('Stuckey')
Tiao = Int('Tiao')
Udall = Int('Udall')

# Each representative is assigned to exactly one zone (1, 2, or 3)
solver.add(Kim >= 1, Kim <= 3)
solver.add(Mahr >= 1, Mahr <= 3)
solver.add(Parra >= 1, Parra <= 3)
solver.add(Quinn >= 1, Quinn <= 3)
solver.add(Stuckey >= 1, Stuckey <= 3)
solver.add(Tiao >= 1, Tiao <= 3)
solver.add(Udall >= 1, Udall <= 3)

# Constraint 1: Either Parra or Tiao (but not both) works in Zone 1
solver.add(Or(And(Parra == 1, Tiao != 1), And(Tiao == 1, Parra != 1)))

# Constraint 2: Either Tiao or Udall (but not both) works in Zone 2
solver.add(Or(And(Tiao == 2, Udall != 2), And(Udall == 2, Tiao != 2)))

# Constraint 3: Parra and Quinn work in the same sales zone
solver.add(Parra == Quinn)

# Constraint 4: Stuckey and Udall work in the same sales zone
solver.add(Stuckey == Udall)

# Constraint 5: There are more representatives in Zone 3 than in Zone 2
# We'll enforce this in the option constraints since it depends on the specific assignments

# Helper function to count representatives in a zone
def count_in_zone(zone):
    return Sum([
        If(Kim == zone, 1, 0),
        If(Mahr == zone, 1, 0),
        If(Parra == zone, 1, 0),
        If(Quinn == zone, 1, 0),
        If(Stuckey == zone, 1, 0),
        If(Tiao == zone, 1, 0),
        If(Udall == zone, 1, 0)
    ])

# Base constraint: Zone 3 count > Zone 2 count (will be enforced per option)

# Now evaluate each multiple-choice option
found_options = []

# Option A: Zone 1: Kim, Parra; Zone 2: Stuckey, Udall; Zone 3: Mahr, Quinn, Tiao
solver.push()
solver.add(Kim == 1)
solver.add(Parra == 1)
solver.add(Stuckey == 2)
solver.add(Udall == 2)
solver.add(Mahr == 3)
solver.add(Quinn == 3)
solver.add(Tiao == 3)
# Enforce Zone 3 > Zone 2
solver.add(count_in_zone(3) > count_in_zone(2))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Zone 1: Kim, Tiao; Zone 2: Stuckey, Udall; Zone 3: Mahr, Parra, Quinn
solver.push()
solver.add(Kim == 1)
solver.add(Tiao == 1)
solver.add(Stuckey == 2)
solver.add(Udall == 2)
solver.add(Mahr == 3)
solver.add(Parra == 3)
solver.add(Quinn == 3)
# Enforce Zone 3 > Zone 2
solver.add(count_in_zone(3) > count_in_zone(2))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Zone 1: Parra, Quinn; Zone 2: Kim, Udall; Zone 3: Mahr, Stuckey, Tiao
solver.push()
solver.add(Parra == 1)
solver.add(Quinn == 1)
solver.add(Kim == 2)
solver.add(Udall == 2)
solver.add(Mahr == 3)
solver.add(Stuckey == 3)
solver.add(Tiao == 3)
# Enforce Zone 3 > Zone 2
solver.add(count_in_zone(3) > count_in_zone(2))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Zone 1: Stuckey, Udall; Zone 2: Kim, Tiao; Zone 3: Mahr, Parra, Quinn
solver.push()
solver.add(Stuckey == 1)
solver.add(Udall == 1)
solver.add(Kim == 2)
solver.add(Tiao == 2)
solver.add(Mahr == 3)
solver.add(Parra == 3)
solver.add(Quinn == 3)
# Enforce Zone 3 > Zone 2
solver.add(count_in_zone(3) > count_in_zone(2))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Zone 1: Tiao; Zone 2: Kim, Parra, Quinn; Zone 3: Stuckey, Udall
solver.push()
solver.add(Tiao == 1)
solver.add(Kim == 2)
solver.add(Parra == 2)
solver.add(Quinn == 2)
solver.add(Stuckey == 3)
solver.add(Udall == 3)
# Enforce Zone 3 > Zone 2
solver.add(count_in_zone(3) > count_in_zone(2))
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")