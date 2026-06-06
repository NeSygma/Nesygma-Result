from z3 import *

solver = Solver()

# Students: Franz (F), Greene (G), Hidalgo (H), Isaacs (I)
students = ["F", "G", "H", "I"]

# Walls: 1, 2, 3, 4
walls = [1, 2, 3, 4]

# Positions: 0 = upper, 1 = lower

# For each student, we have two paintings: oil and watercolor.
# We'll model each painting's wall and position.

# Declare wall variables
wall_F_O = Int('wall_F_O')
wall_F_W = Int('wall_F_W')
wall_G_O = Int('wall_G_O')
wall_G_W = Int('wall_G_W')
wall_H_O = Int('wall_H_O')
wall_H_W = Int('wall_H_W')
wall_I_O = Int('wall_I_O')
wall_I_W = Int('wall_I_W')

# Declare position variables (0=upper, 1=lower)
pos_F_O = Int('pos_F_O')
pos_F_W = Int('pos_F_W')
pos_G_O = Int('pos_G_O')
pos_G_W = Int('pos_G_W')
pos_H_O = Int('pos_H_O')
pos_H_W = Int('pos_H_W')
pos_I_O = Int('pos_I_O')
pos_I_W = Int('pos_I_W')

# Domain constraints: walls are 1-4, positions are 0-1
all_wall_vars = [wall_F_O, wall_F_W, wall_G_O, wall_G_W, wall_H_O, wall_H_W, wall_I_O, wall_I_W]
all_pos_vars = [pos_F_O, pos_F_W, pos_G_O, pos_G_W, pos_H_O, pos_H_W, pos_I_O, pos_I_W]

for v in all_wall_vars:
    solver.add(v >= 1, v <= 4)
for v in all_pos_vars:
    solver.add(v >= 0, v <= 1)

# Exactly two paintings per wall (one upper, one lower)
for w in walls:
    paintings_on_wall = Sum([If(v == w, 1, 0) for v in all_wall_vars])
    solver.add(paintings_on_wall == 2)
    
    upper_on_wall = Sum([If(And(v == w, p == 0), 1, 0) for v, p in zip(all_wall_vars, all_pos_vars)])
    solver.add(upper_on_wall == 1)
    
    lower_on_wall = Sum([If(And(v == w, p == 1), 1, 0) for v, p in zip(all_wall_vars, all_pos_vars)])
    solver.add(lower_on_wall == 1)

# Condition 1: No wall has only watercolors displayed on it.
# i.e., every wall has at least one oil painting.
for w in walls:
    oil_on_wall = Sum([If(v == w, 1, 0) for v in [wall_F_O, wall_G_O, wall_H_O, wall_I_O]])
    solver.add(oil_on_wall >= 1)

# Condition 2: No wall has the work of only one student displayed on it.
# i.e., every wall has paintings by at least two different students.
for w in walls:
    student_on_wall = []
    for wo, ww in [(wall_F_O, wall_F_W), (wall_G_O, wall_G_W), 
                   (wall_H_O, wall_H_W), (wall_I_O, wall_I_W)]:
        student_on_wall.append(If(Or(wo == w, ww == w), 1, 0))
    solver.add(Sum(student_on_wall) >= 2)

# Condition 3: No wall has both a painting by Franz and a painting by Isaacs displayed on it.
for w in walls:
    franz_on_w = Or(wall_F_O == w, wall_F_W == w)
    isaacs_on_w = Or(wall_I_O == w, wall_I_W == w)
    solver.add(Not(And(franz_on_w, isaacs_on_w)))

# Condition 4: Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed.
solver.add(pos_G_W == 0)  # Greene's watercolor is upper position
solver.add(wall_G_W == wall_F_O)  # Same wall as Franz's oil

# Condition 5: Isaacs's oil is displayed in the lower position of wall 4.
solver.add(wall_I_O == 4)
solver.add(pos_I_O == 1)  # lower position

# Additional condition from the question: Greene's oil is displayed on the same wall as Franz's watercolor.
solver.add(wall_G_O == wall_F_W)

# Let's first check if the base constraints are satisfiable
print("Checking base constraints...")
result = solver.check()
print(f"Base result: {result}")

if result == sat:
    m = solver.model()
    print("Model found:")
    for v in all_wall_vars + all_pos_vars:
        print(f"  {v} = {m[v]}")
    
    # Now evaluate each answer choice as "must be true" - i.e., check if the negation is possible
    # For "must be true", we check if NOT(option) is unsatisfiable
    
    print("\nChecking 'must be true' for each option...")
    
    found_options = []
    for letter, constr in [("A", pos_G_O == 0), ("B", wall_H_W == wall_I_W), 
                           ("C", pos_H_O == 0), ("D", wall_H_O == wall_I_W), 
                           ("E", pos_I_W == 1)]:
        solver.push()
        # To check if something MUST be true, we check if its negation is UNSAT
        solver.add(Not(constr))
        neg_result = solver.check()
        print(f"  Option {letter} (negation): {neg_result}")
        if neg_result == unsat:
            found_options.append(letter)
        solver.pop()
    
    print(f"Found options that must be true: {found_options}")
    
    if len(found_options) == 1:
        print("STATUS: sat")
        print(f"answer:{found_options[0]}")
    elif len(found_options) > 1:
        print("STATUS: unsat")
        print(f"Refine: Multiple options found {found_options}")
    else:
        print("STATUS: unsat")
        print("Refine: No options found")
else:
    print("STATUS: unsat")
    print("Refine: Base constraints unsatisfiable")