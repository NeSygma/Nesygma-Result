from z3 import *

# Declare variables for each person's zone (1, 2, or 3)
Kim = Int('Kim')
Mahr = Int('Mahr')
Parra = Int('Parra')
Quinn = Int('Quinn')
Stuckey = Int('Stuckey')
Tiao = Int('Tiao')
Udall = Int('Udall')

# Create solver
solver = Solver()

# Add domain constraints: each person works in zone 1, 2, or 3
people = [Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall]
for p in people:
    solver.add(Or(p == 1, p == 2, p == 3))

# Constraint 1: Either Parra or Tiao (but not both) works in Zone 1
solver.add(Or(Parra == 1, Tiao == 1))
solver.add(Not(And(Parra == 1, Tiao == 1)))

# Constraint 2: Either Tiao or Udall (but not both) works in Zone 2
solver.add(Or(Tiao == 2, Udall == 2))
solver.add(Not(And(Tiao == 2, Udall == 2)))

# Constraint 3: Parra and Quinn work in the same zone
solver.add(Parra == Quinn)

# Constraint 4: Stuckey and Udall work in the same zone
solver.add(Stuckey == Udall)

# Constraint 5: More reps in Zone 3 than in Zone 2
zone3_count = Sum([If(p == 3, 1, 0) for p in people])
zone2_count = Sum([If(p == 2, 1, 0) for p in people])
solver.add(zone3_count > zone2_count)

# Now test each option: check if adding the option makes the problem unsatisfiable
# If it does, then that option MUST be false
found_options = []

# Option A: Kim and Stuckey both work in Zone 1
opt_a_constr = And(Kim == 1, Stuckey == 1)

# Option B: Kim and Stuckey both work in Zone 3
opt_b_constr = And(Kim == 3, Stuckey == 3)

# Option C: Mahr and Stuckey both work in Zone 3
opt_c_constr = And(Mahr == 3, Stuckey == 3)

# Option D: Mahr and Udall both work in Zone 3
opt_d_constr = And(Mahr == 3, Udall == 3)

# Option E: Parra and Stuckey both work in Zone 1
opt_e_constr = And(Parra == 1, Stuckey == 1)

for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
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