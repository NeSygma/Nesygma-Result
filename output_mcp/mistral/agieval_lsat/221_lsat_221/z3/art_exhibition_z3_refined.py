from z3 import *

# Define painting constants
franz_oil = 0
franz_water = 1
greene_oil = 2
greene_water = 3
hidalgo_oil = 4
hidalgo_water = 5
isaacs_oil = 6
isaacs_water = 7

# Helper constants
franz_student = franz_oil // 2  # 0
isaacs_student = isaacs_oil // 2  # 3

# Declare solver
solver = Solver()

# Declare wall positions
wall1_upper = Int('wall1_upper')
wall1_lower = Int('wall1_lower')
wall2_upper = Int('wall2_upper')
wall2_lower = Int('wall2_lower')
wall3_upper = Int('wall3_upper')
wall3_lower = Int('wall3_lower')
wall4_upper = Int('wall4_upper')
wall4_lower = Int('wall4_lower')

# All paintings must be in 0-7
paintings = [wall1_upper, wall1_lower, wall2_upper, wall2_lower,
             wall3_upper, wall3_lower, wall4_upper, wall4_lower]
for p in paintings:
    solver.add(p >= 0, p <= 7)

# Constraint 5: Isaacs's oil is in the lower position of wall 4
solver.add(wall4_lower == isaacs_oil)

# Constraint 6: Hidalgo's oil is on wall 2
solver.add(Or(wall2_upper == hidalgo_oil, wall2_lower == hidalgo_oil))

# Constraint 1: No wall has only watercolors (at least one oil per wall)
for wall_upper, wall_lower in [(wall1_upper, wall1_lower),
                               (wall2_upper, wall2_lower),
                               (wall3_upper, wall3_lower),
                               (wall4_upper, wall4_lower)]:
    solver.add(Or(wall_upper % 2 == 0, wall_lower % 2 == 0))

# Constraint 2: No wall has only one student (paintings from different students)
for wall_upper, wall_lower in [(wall1_upper, wall1_lower),
                               (wall2_upper, wall2_lower),
                               (wall3_upper, wall3_lower),
                               (wall4_upper, wall4_lower)]:
    solver.add(wall_upper / 2 != wall_lower / 2)

# Constraint 3: No wall has both Franz and Isaacs
for wall_upper, wall_lower in [(wall1_upper, wall1_lower),
                               (wall2_upper, wall2_lower),
                               (wall3_upper, wall3_lower),
                               (wall4_upper, wall4_lower)]:
    solver.add(Not(Or(And(wall_upper / 2 == franz_student, wall_lower / 2 == isaacs_student),
                      And(wall_upper / 2 == isaacs_student, wall_lower / 2 == franz_student))))

# Constraint 4: Greene's watercolor is in the upper position of the wall on which Franz's oil is displayed
for wall_upper, wall_lower in [(wall1_upper, wall1_lower),
                               (wall2_upper, wall2_lower),
                               (wall3_upper, wall3_lower),
                               (wall4_upper, wall4_lower)]:
    solver.add(Implies(Or(wall_upper == franz_oil, wall_lower == franz_oil),
                       wall_upper == greene_water))

# Additional constraint: Each student's two paintings must be on different walls
# Franz's oil and watercolor must be on different walls
solver.add(Or(
    And(wall1_upper == franz_oil, Or(wall2_lower == franz_water, wall2_upper == franz_water,
                                     wall3_lower == franz_water, wall3_upper == franz_water,
                                     wall4_lower == franz_water, wall4_upper == franz_water)),
    And(wall1_lower == franz_oil, Or(wall2_lower == franz_water, wall2_upper == franz_water,
                                     wall3_lower == franz_water, wall3_upper == franz_water,
                                     wall4_lower == franz_water, wall4_upper == franz_water)),
    And(wall2_upper == franz_oil, Or(wall1_lower == franz_water, wall1_upper == franz_water,
                                     wall3_lower == franz_water, wall3_upper == franz_water,
                                     wall4_lower == franz_water, wall4_upper == franz_water)),
    And(wall2_lower == franz_oil, Or(wall1_lower == franz_water, wall1_upper == franz_water,
                                     wall3_lower == franz_water, wall3_upper == franz_water,
                                     wall4_lower == franz_water, wall4_upper == franz_water)),
    And(wall3_upper == franz_oil, Or(wall1_lower == franz_water, wall1_upper == franz_water,
                                     wall2_lower == franz_water, wall2_upper == franz_water,
                                     wall4_lower == franz_water, wall4_upper == franz_water)),
    And(wall3_lower == franz_oil, Or(wall1_lower == franz_water, wall1_upper == franz_water,
                                     wall2_lower == franz_water, wall2_upper == franz_water,
                                     wall4_lower == franz_water, wall4_upper == franz_water)),
    And(wall4_upper == franz_oil, Or(wall1_lower == franz_water, wall1_upper == franz_water,
                                     wall2_lower == franz_water, wall2_upper == franz_water,
                                     wall3_lower == franz_water, wall3_upper == franz_water)),
    And(wall4_lower == franz_oil, Or(wall1_lower == franz_water, wall1_upper == franz_water,
                                     wall2_lower == franz_water, wall2_upper == franz_water,
                                     wall3_lower == franz_water, wall3_upper == franz_water))
))

# Hidalgo's oil and watercolor must be on different walls
solver.add(Or(
    And(wall1_upper == hidalgo_oil, Or(wall2_lower == hidalgo_water, wall2_upper == hidalgo_water,
                                     wall3_lower == hidalgo_water, wall3_upper == hidalgo_water,
                                     wall4_lower == hidalgo_water, wall4_upper == hidalgo_water)),
    And(wall1_lower == hidalgo_oil, Or(wall2_lower == hidalgo_water, wall2_upper == hidalgo_water,
                                     wall3_lower == hidalgo_water, wall3_upper == hidalgo_water,
                                     wall4_lower == hidalgo_water, wall4_upper == hidalgo_water)),
    And(wall2_upper == hidalgo_oil, Or(wall1_lower == hidalgo_water, wall1_upper == hidalgo_water,
                                     wall3_lower == hidalgo_water, wall3_upper == hidalgo_water,
                                     wall4_lower == hidalgo_water, wall4_upper == hidalgo_water)),
    And(wall2_lower == hidalgo_oil, Or(wall1_lower == hidalgo_water, wall1_upper == hidalgo_water,
                                     wall3_lower == hidalgo_water, wall3_upper == hidalgo_water,
                                     wall4_lower == hidalgo_water, wall4_upper == hidalgo_water)),
    And(wall3_upper == hidalgo_oil, Or(wall1_lower == hidalgo_water, wall1_upper == hidalgo_water,
                                     wall2_lower == hidalgo_water, wall2_upper == hidalgo_water,
                                     wall4_lower == hidalgo_water, wall4_upper == hidalgo_water)),
    And(wall3_lower == hidalgo_oil, Or(wall1_lower == hidalgo_water, wall1_upper == hidalgo_water,
                                     wall2_lower == hidalgo_water, wall2_upper == hidalgo_water,
                                     wall4_lower == hidalgo_water, wall4_upper == hidalgo_water)),
    And(wall4_upper == hidalgo_oil, Or(wall1_lower == hidalgo_water, wall1_upper == hidalgo_water,
                                     wall2_lower == hidalgo_water, wall2_upper == hidalgo_water,
                                     wall3_lower == hidalgo_water, wall3_upper == hidalgo_water)),
    And(wall4_lower == hidalgo_oil, Or(wall1_lower == hidalgo_water, wall1_upper == hidalgo_water,
                                     wall2_lower == hidalgo_water, wall2_upper == hidalgo_water,
                                     wall3_lower == hidalgo_water, wall3_upper == hidalgo_water))
))

# Greene's oil and watercolor must be on different walls
solver.add(Or(
    And(wall1_upper == greene_oil, Or(wall2_lower == greene_water, wall2_upper == greene_water,
                                     wall3_lower == greene_water, wall3_upper == greene_water,
                                     wall4_lower == greene_water, wall4_upper == greene_water)),
    And(wall1_lower == greene_oil, Or(wall2_lower == greene_water, wall2_upper == greene_water,
                                     wall3_lower == greene_water, wall3_upper == greene_water,
                                     wall4_lower == greene_water, wall4_upper == greene_water)),
    And(wall2_upper == greene_oil, Or(wall1_lower == greene_water, wall1_upper == greene_water,
                                     wall3_lower == greene_water, wall3_upper == greene_water,
                                     wall4_lower == greene_water, wall4_upper == greene_water)),
    And(wall2_lower == greene_oil, Or(wall1_lower == greene_water, wall1_upper == greene_water,
                                     wall3_lower == greene_water, wall3_upper == greene_water,
                                     wall4_lower == greene_water, wall4_upper == greene_water)),
    And(wall3_upper == greene_oil, Or(wall1_lower == greene_water, wall1_upper == greene_water,
                                     wall2_lower == greene_water, wall2_upper == greene_water,
                                     wall4_lower == greene_water, wall4_upper == greene_water)),
    And(wall3_lower == greene_oil, Or(wall1_lower == greene_water, wall1_upper == greene_water,
                                     wall2_lower == greene_water, wall2_upper == greene_water,
                                     wall4_lower == greene_water, wall4_upper == greene_water)),
    And(wall4_upper == greene_oil, Or(wall1_lower == greene_water, wall1_upper == greene_water,
                                     wall2_lower == greene_water, wall2_upper == greene_water,
                                     wall3_lower == greene_water, wall3_upper == greene_water)),
    And(wall4_lower == greene_oil, Or(wall1_lower == greene_water, wall1_upper == greene_water,
                                     wall2_lower == greene_water, wall2_upper == greene_water,
                                     wall3_lower == greene_water, wall3_upper == greene_water))
))

# Isaacs's oil and watercolor must be on different walls
solver.add(Or(
    And(wall1_upper == isaacs_oil, Or(wall2_lower == isaacs_water, wall2_upper == isaacs_water,
                                     wall3_lower == isaacs_water, wall3_upper == isaacs_water,
                                     wall4_lower == isaacs_water, wall4_upper == isaacs_water)),
    And(wall1_lower == isaacs_oil, Or(wall2_lower == isaacs_water, wall2_upper == isaacs_water,
                                     wall3_lower == isaacs_water, wall3_upper == isaacs_water,
                                     wall4_lower == isaacs_water, wall4_upper == isaacs_water)),
    And(wall2_upper == isaacs_oil, Or(wall1_lower == isaacs_water, wall1_upper == isaacs_water,
                                     wall3_lower == isaacs_water, wall3_upper == isaacs_water,
                                     wall4_lower == isaacs_water, wall4_upper == isaacs_water)),
    And(wall2_lower == isaacs_oil, Or(wall1_lower == isaacs_water, wall1_upper == isaacs_water,
                                     wall3_lower == isaacs_water, wall3_upper == isaacs_water,
                                     wall4_lower == isaacs_water, wall4_upper == isaacs_water)),
    And(wall3_upper == isaacs_oil, Or(wall1_lower == isaacs_water, wall1_upper == isaacs_water,
                                     wall2_lower == isaacs_water, wall2_upper == isaacs_water,
                                     wall4_lower == isaacs_water, wall4_upper == isaacs_water)),
    And(wall3_lower == isaacs_oil, Or(wall1_lower == isaacs_water, wall1_upper == isaacs_water,
                                     wall2_lower == isaacs_water, wall2_upper == isaacs_water,
                                     wall4_lower == isaacs_water, wall4_upper == isaacs_water)),
    And(wall4_upper == isaacs_oil, Or(wall1_lower == isaacs_water, wall1_upper == isaacs_water,
                                     wall2_lower == isaacs_water, wall2_upper == isaacs_water,
                                     wall3_lower == isaacs_water, wall3_upper == isaacs_water)),
    And(wall4_lower == isaacs_oil, Or(wall1_lower == isaacs_water, wall1_upper == isaacs_water,
                                     wall2_lower == isaacs_water, wall2_upper == isaacs_water,
                                     wall3_lower == isaacs_water, wall3_upper == isaacs_water))
))

# Now check each option for wall 2
found_options = []

# Option A: Franz's oil (0) could be on wall 2
opt_a_constr = Or(And(wall2_upper == hidalgo_oil, wall2_lower == franz_oil),
                  And(wall2_upper == franz_oil, wall2_lower == hidalgo_oil))
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Greene's watercolor (3) could be on wall 2
opt_b_constr = Or(And(wall2_upper == hidalgo_oil, wall2_lower == greene_water),
                  And(wall2_upper == greene_water, wall2_lower == hidalgo_oil))
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Greene's oil (2) could be on wall 2
opt_c_constr = Or(And(wall2_upper == hidalgo_oil, wall2_lower == greene_oil),
                  And(wall2_upper == greene_oil, wall2_lower == hidalgo_oil))
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Hidalgo's watercolor (5) could be on wall 2
opt_d_constr = Or(And(wall2_upper == hidalgo_oil, wall2_lower == hidalgo_water),
                  And(wall2_upper == hidalgo_water, wall2_lower == hidalgo_oil))
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Isaacs's watercolor (7) could be on wall 2
opt_e_constr = Or(And(wall2_upper == hidalgo_oil, wall2_lower == isaacs_water),
                  And(wall2_upper == isaacs_water, wall2_lower == hidalgo_oil))
solver.push()
solver.add(opt_e_constr)
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