from z3 import *

# Representatives: Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall
# Zone values: 1, 2, 3

# Create Z3 integer variables for each person
Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall = Ints('Kim Mahr Parra Quinn Stuckey Tiao Udall')
persons = [Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall]

solver = Solver()

# Domain constraints: each person works in exactly one zone (1, 2, or 3)
for p in persons:
    solver.add(Or(p == 1, p == 2, p == 3))

# Condition 1: Either Parra or Tiao (but not both) works in Zone 1.
solver.add(Or(Parra == 1, Tiao == 1))
solver.add(Not(And(Parra == 1, Tiao == 1)))

# Condition 2: Either Tiao or Udall (but not both) works in Zone 2.
solver.add(Or(Tiao == 2, Udall == 2))
solver.add(Not(And(Tiao == 2, Udall == 2)))

# Condition 3: Parra and Quinn work in the same sales zone as each other.
solver.add(Parra == Quinn)

# Condition 4: Stuckey and Udall work in the same sales zone as each other.
solver.add(Stuckey == Udall)

# Condition 5: There are more sales representatives working in Zone 3 than in Zone 2.
# Count how many are in Zone 3, count how many are in Zone 2, and ensure zone3_count > zone2_count.
zone3_count = Sum([If(p == 3, 1, 0) for p in persons])
zone2_count = Sum([If(p == 2, 1, 0) for p in persons])
solver.add(zone3_count > zone2_count)

# Now test each option
# Options are given as mappings of person -> zone

options = {
    "A": {
        Kim: 1, Parra: 1,
        Stuckey: 2, Udall: 2,
        Mahr: 3, Quinn: 3, Tiao: 3
    },
    "B": {
        Kim: 1, Tiao: 1,
        Stuckey: 2, Udall: 2,
        Mahr: 3, Parra: 3, Quinn: 3
    },
    "C": {
        Parra: 1, Quinn: 1,
        Kim: 2, Udall: 2,
        Mahr: 3, Stuckey: 3, Tiao: 3
    },
    "D": {
        Stuckey: 1, Udall: 1,
        Kim: 2, Tiao: 2,
        Mahr: 3, Parra: 3, Quinn: 3
    },
    "E": {
        Tiao: 1,
        Kim: 2, Parra: 2, Quinn: 2,
        Stuckey: 3, Udall: 3
    }
}

found_options = []

for letter, assignments in options.items():
    solver.push()
    # Add the specific assignments from this option
    for var, zone in assignments.items():
        solver.add(var == zone)
    
    # Check if this option is satisfiable given all constraints
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