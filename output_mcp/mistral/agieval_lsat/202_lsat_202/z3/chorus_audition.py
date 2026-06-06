from z3 import *

# Define singers as symbolic constants for clarity
Kammer = 0
Lugo = 1
Trillo = 2
Waite = 3
Yoshida = 4
Zinn = 5

# Base constraints for all options
solver = Solver()

# Positions are 0 to 5 (0-based for Z3 simplicity)
positions = [Int(f'pos_{i}') for i in range(6)]

# Each position must be assigned a unique singer from 0 to 5
solver.add(Distinct(positions))
solver.add([And(pos >= 0, pos <= 5) for pos in positions])

# Constraint: Only Kammer (0) and Lugo (1) are recorded
# So any position assigned to 0 or 1 is recorded; others are not

# Constraint: The fourth audition (index 3) cannot be recorded
# So position 3 cannot be 0 (Kammer) or 1 (Lugo)
solver.add(positions[3] != Kammer)
solver.add(positions[3] != Lugo)

# Constraint: The fifth audition (index 4) must be recorded
# So position 4 must be 0 (Kammer) or 1 (Lugo)
solver.add(Or(positions[4] == Kammer, positions[4] == Lugo))

# Constraint: Waite's audition must take place earlier than the two recorded auditions
# So Waite (3) must come before both Kammer (0) and Lugo (1)
# We need to find the index of Waite, Kammer, and Lugo in the positions list
# Use Or-loop to find the position of Waite, Kammer, and Lugo
waite_pos = Int('waite_pos')
kammer_pos = Int('kammer_pos')
lugo_pos = Int('lugo_pos')

# Find the position of Waite (3)
solver.add(Or(
    And(positions[0] == Waite, waite_pos == 0),
    And(positions[1] == Waite, waite_pos == 1),
    And(positions[2] == Waite, waite_pos == 2),
    And(positions[3] == Waite, waite_pos == 3),
    And(positions[4] == Waite, waite_pos == 4),
    And(positions[5] == Waite, waite_pos == 5)
))

# Find the position of Kammer (0)
solver.add(Or(
    And(positions[0] == Kammer, kammer_pos == 0),
    And(positions[1] == Kammer, kammer_pos == 1),
    And(positions[2] == Kammer, kammer_pos == 2),
    And(positions[3] == Kammer, kammer_pos == 3),
    And(positions[4] == Kammer, kammer_pos == 4),
    And(positions[5] == Kammer, kammer_pos == 5)
))

# Find the position of Lugo (1)
solver.add(Or(
    And(positions[0] == Lugo, lugo_pos == 0),
    And(positions[1] == Lugo, lugo_pos == 1),
    And(positions[2] == Lugo, lugo_pos == 2),
    And(positions[3] == Lugo, lugo_pos == 3),
    And(positions[4] == Lugo, lugo_pos == 4),
    And(positions[5] == Lugo, lugo_pos == 5)
))

solver.add(waite_pos < kammer_pos)
solver.add(waite_pos < lugo_pos)

# Constraint: Kammer's audition must take place earlier than Trillo's audition
trillo_pos = Int('trillo_pos')

# Find the position of Trillo (2)
solver.add(Or(
    And(positions[0] == Trillo, trillo_pos == 0),
    And(positions[1] == Trillo, trillo_pos == 1),
    And(positions[2] == Trillo, trillo_pos == 2),
    And(positions[3] == Trillo, trillo_pos == 3),
    And(positions[4] == Trillo, trillo_pos == 4),
    And(positions[5] == Trillo, trillo_pos == 5)
))

solver.add(kammer_pos < trillo_pos)

# Constraint: Zinn's audition must take place earlier than Yoshida's audition
zinn_pos = Int('zinn_pos')
yoshida_pos = Int('yoshida_pos')

# Find the position of Zinn (5)
solver.add(Or(
    And(positions[0] == Zinn, zinn_pos == 0),
    And(positions[1] == Zinn, zinn_pos == 1),
    And(positions[2] == Zinn, zinn_pos == 2),
    And(positions[3] == Zinn, zinn_pos == 3),
    And(positions[4] == Zinn, zinn_pos == 4),
    And(positions[5] == Zinn, zinn_pos == 5)
))

# Find the position of Yoshida (4)
solver.add(Or(
    And(positions[0] == Yoshida, yoshida_pos == 0),
    And(positions[1] == Yoshida, yoshida_pos == 1),
    And(positions[2] == Yoshida, yoshida_pos == 2),
    And(positions[3] == Yoshida, yoshida_pos == 3),
    And(positions[4] == Yoshida, yoshida_pos == 4),
    And(positions[5] == Yoshida, yoshida_pos == 5)
))

solver.add(zinn_pos < yoshida_pos)

# Now test each option
found_options = []

# Option A: Kammer, Trillo, Zinn, Waite, Lugo, Yoshida
opt_a_constr = And(
    positions[0] == Kammer,
    positions[1] == Trillo,
    positions[2] == Zinn,
    positions[3] == Waite,
    positions[4] == Lugo,
    positions[5] == Yoshida
)

# Option B: Waite, Kammer, Yoshida, Zinn, Lugo, Trillo
opt_b_constr = And(
    positions[0] == Waite,
    positions[1] == Kammer,
    positions[2] == Yoshida,
    positions[3] == Zinn,
    positions[4] == Lugo,
    positions[5] == Trillo
)

# Option C: Waite, Lugo, Kammer, Trillo, Zinn, Yoshida
opt_c_constr = And(
    positions[0] == Waite,
    positions[1] == Lugo,
    positions[2] == Kammer,
    positions[3] == Trillo,
    positions[4] == Zinn,
    positions[5] == Yoshida
)

# Option D: Waite, Zinn, Kammer, Trillo, Lugo, Yoshida
opt_d_constr = And(
    positions[0] == Waite,
    positions[1] == Zinn,
    positions[2] == Kammer,
    positions[3] == Trillo,
    positions[4] == Lugo,
    positions[5] == Yoshida
)

# Option E: Zinn, Yoshida, Waite, Lugo, Kammer, Trillo
opt_e_constr = And(
    positions[0] == Zinn,
    positions[1] == Yoshida,
    positions[2] == Waite,
    positions[3] == Lugo,
    positions[4] == Kammer,
    positions[5] == Trillo
)

# Evaluate each option
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