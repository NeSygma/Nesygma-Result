from z3 import *

# Create solver
solver = Solver()

# Define singers
singers = ["Kammer", "Lugo", "Trillo", "Waite", "Yoshida", "Zinn"]
# Map singer names to indices for easier handling
singer_to_idx = {name: i for i, name in enumerate(singers)}

# Position variables: position[i] = position of singer i (1-6)
position = [Int(f"pos_{i}") for i in range(6)]

# Recording status: recorded[i] = True if singer i is recorded
recorded = [Bool(f"rec_{i}") for i in range(6)]

# Base constraints: each position 1-6 is used exactly once
for i in range(6):
    solver.add(position[i] >= 1)
    solver.add(position[i] <= 6)
solver.add(Distinct(position))

# Recording constraints: exactly Kammer and Lugo are recorded
kammer_idx = singer_to_idx["Kammer"]
lugo_idx = singer_to_idx["Lugo"]
solver.add(recorded[kammer_idx] == True)
solver.add(recorded[lugo_idx] == True)
for i in range(6):
    if i != kammer_idx and i != lugo_idx:
        solver.add(recorded[i] == False)

# Constraint 1: Fourth audition cannot be recorded
# Find which singer is at position 4, and ensure they are not recorded
for i in range(6):
    solver.add(Implies(position[i] == 4, Not(recorded[i])))

# Constraint 2: Fifth audition must be recorded
for i in range(6):
    solver.add(Implies(position[i] == 5, recorded[i]))

# Constraint 3: Waite's audition must take place earlier than the two recorded auditions
waite_idx = singer_to_idx["Waite"]
# Waite must be before both Kammer and Lugo
solver.add(position[waite_idx] < position[kammer_idx])
solver.add(position[waite_idx] < position[lugo_idx])

# Constraint 4: Kammer's audition must take place earlier than Trillo's audition
trillo_idx = singer_to_idx["Trillo"]
solver.add(position[kammer_idx] < position[trillo_idx])

# Constraint 5: Zinn's audition must take place earlier than Yoshida's audition
zinn_idx = singer_to_idx["Zinn"]
yoshida_idx = singer_to_idx["Yoshida"]
solver.add(position[zinn_idx] < position[yoshida_idx])

# Now test each answer choice for the sixth audition
# We'll use the exact skeleton provided
found_options = []

# Option A: Kammer's audition is sixth
opt_a_constr = (position[kammer_idx] == 6)
# Option B: Lugo's audition is sixth
opt_b_constr = (position[lugo_idx] == 6)
# Option C: Trillo's audition is sixth
opt_c_constr = (position[trillo_idx] == 6)
# Option D: Waite's audition is sixth
opt_d_constr = (position[waite_idx] == 6)
# Option E: Zinn's audition is sixth
opt_e_constr = (position[zinn_idx] == 6)

for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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