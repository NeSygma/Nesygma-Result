from z3 import *

solver = Solver()

# Declare variables for each person
Kim = Int('Kim')
Mahr = Int('Mahr')
Parra = Int('Parra')
Quinn = Int('Quinn')
Stuckey = Int('Stuckey')
Tiao = Int('Tiao')
Udall = Int('Udall')

# Domain constraints: each person works in zone 1, 2, or 3
solver.add(Kim >= 1, Kim <= 3)
solver.add(Mahr >= 1, Mahr <= 3)
solver.add(Parra >= 1, Parra <= 3)
solver.add(Quinn >= 1, Quinn <= 3)
solver.add(Stuckey >= 1, Stuckey <= 3)
solver.add(Tiao >= 1, Tiao <= 3)
solver.add(Udall >= 1, Udall <= 3)

# Constraint 1: Either Parra or Tiao (but not both) works in Zone 1.
solver.add(Or(And(Parra == 1, Tiao != 1), And(Parra != 1, Tiao == 1)))

# Constraint 2: Either Tiao or Udall (but not both) works in Zone 2.
solver.add(Or(And(Tiao == 2, Udall != 2), And(Tiao != 2, Udall == 2)))

# Constraint 3: Parra and Quinn work in the same sales zone as each other.
solver.add(Parra == Quinn)

# Constraint 4: Stuckey and Udall work in the same sales zone as each other.
solver.add(Stuckey == Udall)

# Constraint 5: There are more of the sales representatives working in Zone 3 than in Zone 2.
# Count how many are in zone 3 and zone 2
count_zone3 = Sum([If(Kim == 3, 1, 0),
                   If(Mahr == 3, 1, 0),
                   If(Parra == 3, 1, 0),
                   If(Quinn == 3, 1, 0),
                   If(Stuckey == 3, 1, 0),
                   If(Tiao == 3, 1, 0),
                   If(Udall == 3, 1, 0)])

count_zone2 = Sum([If(Kim == 2, 1, 0),
                   If(Mahr == 2, 1, 0),
                   If(Parra == 2, 1, 0),
                   If(Quinn == 2, 1, 0),
                   If(Stuckey == 2, 1, 0),
                   If(Tiao == 2, 1, 0),
                   If(Udall == 2, 1, 0)])

solver.add(count_zone3 > count_zone2)

# Now evaluate each answer choice
found_options = []

# Option A: Zone 1: Kim, Parra; Zone 2: Stuckey, Udall; Zone 3: Mahr, Quinn, Tiao
opt_a = And(Kim == 1, Parra == 1,
            Stuckey == 2, Udall == 2,
            Mahr == 3, Quinn == 3, Tiao == 3)

# Option B: Zone 1: Kim, Tiao; Zone 2: Stuckey, Udall; Zone 3: Mahr, Parra, Quinn
opt_b = And(Kim == 1, Tiao == 1,
            Stuckey == 2, Udall == 2,
            Mahr == 3, Parra == 3, Quinn == 3)

# Option C: Zone 1: Parra, Quinn; Zone 2: Kim, Udall; Zone 3: Mahr, Stuckey, Tiao
opt_c = And(Parra == 1, Quinn == 1,
            Kim == 2, Udall == 2,
            Mahr == 3, Stuckey == 3, Tiao == 3)

# Option D: Zone 1: Stuckey, Udall; Zone 2: Kim, Tiao; Zone 3: Mahr, Parra, Quinn
opt_d = And(Stuckey == 1, Udall == 1,
            Kim == 2, Tiao == 2,
            Mahr == 3, Parra == 3, Quinn == 3)

# Option E: Zone 1: Tiao; Zone 2: Kim, Parra, Quinn; Zone 3: Stuckey, Udall
opt_e = And(Tiao == 1,
            Kim == 2, Parra == 2, Quinn == 2,
            Stuckey == 3, Udall == 3)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

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