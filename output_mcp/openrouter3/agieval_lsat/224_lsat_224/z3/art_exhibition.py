from z3 import *

# Create solver
solver = Solver()

# Define entities
students = ["Franz", "Greene", "Hidalgo", "Isaacs"]
walls = [1, 2, 3, 4]
positions = ["upper", "lower"]

# Create symbolic variables for each painting
# For each student, we have an oil and a watercolor
# Each painting is assigned to a wall and a position
paintings = {}
for student in students:
    for paint_type in ["oil", "watercolor"]:
        # Each painting has a wall and position
        wall = Int(f"{student}_{paint_type}_wall")
        position = Int(f"{student}_{paint_type}_pos")  # 0 = upper, 1 = lower
        
        # Constraints: wall must be 1-4, position must be 0 or 1
        solver.add(wall >= 1, wall <= 4)
        solver.add(position >= 0, position <= 1)
        
        paintings[(student, paint_type)] = {"wall": wall, "position": position}

# Constraint 1: No wall has only watercolors displayed on it
# For each wall, there must be at least one oil painting
for w in walls:
    # At least one oil painting on this wall
    oil_on_wall = Or([paintings[(s, "oil")]["wall"] == w for s in students])
    solver.add(oil_on_wall)

# Constraint 2: No wall has the work of only one student displayed on it
# For each wall, there must be at least two different students
for w in walls:
    # Count distinct students on this wall
    # We need at least 2 different students on each wall
    # This is tricky - we'll use a different approach
    # For each wall, there must be at least 2 paintings from different students
    # We'll ensure that for each wall, there exist at least 2 students with paintings there
    student_on_wall = []
    for s in students:
        # Student s has a painting on wall w if either oil or watercolor is on w
        has_painting = Or(
            paintings[(s, "oil")]["wall"] == w,
            paintings[(s, "watercolor")]["wall"] == w
        )
        student_on_wall.append(has_painting)
    
    # At least 2 students must have paintings on this wall
    # We need to count how many students have paintings on this wall
    # Use a more direct approach: ensure there are at least 2 different students
    # We'll create a constraint that there exist at least 2 students with paintings on wall w
    # This is complex in Z3, so we'll use a different method
    # For now, we'll skip this constraint and come back to it if needed

# Constraint 3: No wall has both a painting by Franz and a painting by Isaacs displayed on it
for w in walls:
    franz_on_wall = Or(
        paintings[("Franz", "oil")]["wall"] == w,
        paintings[("Franz", "watercolor")]["wall"] == w
    )
    isaacs_on_wall = Or(
        paintings[("Isaacs", "oil")]["wall"] == w,
        paintings[("Isaacs", "watercolor")]["wall"] == w
    )
    solver.add(Not(And(franz_on_wall, isaacs_on_wall)))

# Constraint 4: Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed
# This means: Greene's watercolor wall = Franz's oil wall, and Greene's watercolor position = upper (0)
solver.add(paintings[("Greene", "watercolor")]["wall"] == paintings[("Franz", "oil")]["wall"])
solver.add(paintings[("Greene", "watercolor")]["position"] == 0)

# Constraint 5: Isaacs's oil is displayed in the lower position of wall 4
solver.add(paintings[("Isaacs", "oil")]["wall"] == 4)
solver.add(paintings[("Isaacs", "oil")]["position"] == 1)  # lower = 1

# Additional constraint: Each wall has exactly 2 paintings (one upper, one lower)
# We need to ensure that for each wall and each position, exactly one painting is assigned
# This is complex - we'll use a different approach
# For each wall, we need exactly 2 paintings: one upper, one lower
# We'll create variables to track which painting is where

# Let's create a more structured approach
# For each wall and position, we need exactly one painting
# We'll create assignment variables: assign[(wall, position, student, type)] = Bool
# But this might be too complex

# Alternative approach: Use arrays to track paintings per wall
# For each wall, we need exactly 2 paintings: one upper, one lower
# We'll ensure that for each wall, there are exactly 2 paintings assigned

# Let's try a simpler approach: ensure all paintings are assigned to different wall-position pairs
# There are 4 walls × 2 positions = 8 slots, and we have 8 paintings (4 students × 2 types)
# So we need a bijection between paintings and slots

# Create a list of all paintings
all_paintings = []
for s in students:
    for t in ["oil", "watercolor"]:
        all_paintings.append((s, t))

# Create a mapping from slot (wall, position) to painting
# We'll use a constraint that each slot has exactly one painting
# and each painting is in exactly one slot

# For each slot, we'll create a variable indicating which painting is there
# But this is complex - let's use a different method

# Instead, we'll ensure that all paintings have distinct (wall, position) pairs
# We'll create a list of all (wall, position) pairs for each painting
painting_slots = []
for s in students:
    for t in ["oil", "watercolor"]:
        wall = paintings[(s, t)]["wall"]
        pos = paintings[(s, t)]["position"]
        # Create a unique identifier for the slot
        slot_id = wall * 2 + pos  # This gives unique IDs: 1*2+0=2, 1*2+1=3, 2*2+0=4, etc.
        painting_slots.append(slot_id)

# Ensure all slot IDs are distinct
solver.add(Distinct(painting_slots))

# Now let's add the constraint about exactly 2 paintings per wall
# For each wall, we need exactly 2 paintings (one upper, one lower)
# We can check this by ensuring that for each wall, there are exactly 2 paintings assigned
# We'll count paintings per wall using If conditions
for w in walls:
    count = Sum([If(paintings[(s, t)]["wall"] == w, 1, 0) for s in students for t in ["oil", "watercolor"]])
    solver.add(count == 2)

# Now let's add the constraint about no wall having only one student
# For each wall, we need at least 2 different students
# We'll ensure this by checking that there are at least 2 students with paintings on each wall
for w in walls:
    # For each student, check if they have any painting on this wall
    student_has_painting = []
    for s in students:
        has_any = Or(
            paintings[(s, "oil")]["wall"] == w,
            paintings[(s, "watercolor")]["wall"] == w
        )
        student_has_painting.append(has_any)
    
    # We need at least 2 students to have paintings on this wall
    # We'll create a constraint that there exist at least 2 students with paintings
    # This is tricky - we'll use a different approach
    # For each pair of students, ensure they're not the only one on a wall
    # Actually, we can ensure that for each wall, there are at least 2 students
    # by checking that not all paintings on a wall are from the same student
    # But we need to be careful

# Let's try a different approach for the "no wall has only one student" constraint
# For each wall, we'll ensure that there are at least 2 different students
# We can do this by ensuring that for each wall, there exist at least 2 students with paintings
# We'll use a counter for each student on each wall
for w in walls:
    # For each student, count how many paintings they have on this wall
    for s in students:
        count_s = Sum([
            If(paintings[(s, "oil")]["wall"] == w, 1, 0),
            If(paintings[(s, "watercolor")]["wall"] == w, 1, 0)
        ])
        # If a student has 2 paintings on a wall, that's okay as long as there's another student
        # But we need to ensure that not all paintings on a wall are from one student
        # We'll handle this differently

# Actually, let's think about this differently
# For each wall, we have exactly 2 paintings
# If both paintings are from the same student, that violates the constraint
# So we need to ensure that for each wall, the two paintings are from different students
# We can do this by ensuring that for each wall, there are at least 2 students with paintings

# Let's create a more direct constraint
# For each wall, we'll create variables indicating which students have paintings there
# Then ensure at least 2 students have paintings

# We'll use a simpler approach: for each wall, ensure that there are at least 2 students
# by checking that the set of students on that wall has size at least 2
# We can do this by ensuring that for each wall, there exist two different students with paintings

# For each wall, we'll create a constraint that there exist at least 2 students
# We'll iterate over all pairs of students and ensure that for each wall,
# at least one pair has both students with paintings on that wall
# But this is getting complex

# Let's try a different strategy: use the fact that we have exactly 2 paintings per wall
# and ensure that these 2 paintings are from different students
# We can do this by ensuring that for each wall, the two paintings are from different students

# We'll create a constraint for each wall: the two paintings on that wall are from different students
# But we don't know which paintings are on which wall yet

# Let's proceed with the constraints we have and see if we can add the student constraint later

# Now let's define the answer choices as constraints
# Each choice is about which paintings are in upper or lower positions

# For each student, we have two paintings: oil and watercolor
# Each can be in upper (0) or lower (1) position

# Choice A: Both of Franz's paintings and both of Greene's paintings are displayed in lower positions
opt_a_constr = And(
    paintings[("Franz", "oil")]["position"] == 1,
    paintings[("Franz", "watercolor")]["position"] == 1,
    paintings[("Greene", "oil")]["position"] == 1,
    paintings[("Greene", "watercolor")]["position"] == 1
)

# Choice B: Both of Franz's paintings and both of Greene's paintings are displayed in upper positions
opt_b_constr = And(
    paintings[("Franz", "oil")]["position"] == 0,
    paintings[("Franz", "watercolor")]["position"] == 0,
    paintings[("Greene", "oil")]["position"] == 0,
    paintings[("Greene", "watercolor")]["position"] == 0
)

# Choice C: Both of Franz's paintings and both of Hidalgo's paintings are displayed in upper positions
opt_c_constr = And(
    paintings[("Franz", "oil")]["position"] == 0,
    paintings[("Franz", "watercolor")]["position"] == 0,
    paintings[("Hidalgo", "oil")]["position"] == 0,
    paintings[("Hidalgo", "watercolor")]["position"] == 0
)

# Choice D: Both of Greene's paintings and both of Hidalgo's paintings are displayed in lower positions
opt_d_constr = And(
    paintings[("Greene", "oil")]["position"] == 1,
    paintings[("Greene", "watercolor")]["position"] == 1,
    paintings[("Hidalgo", "oil")]["position"] == 1,
    paintings[("Hidalgo", "watercolor")]["position"] == 1
)

# Choice E: Both of Greene's paintings and both of Hidalgo's paintings are displayed in upper positions
opt_e_constr = And(
    paintings[("Greene", "oil")]["position"] == 0,
    paintings[("Greene", "watercolor")]["position"] == 0,
    paintings[("Hidalgo", "oil")]["position"] == 0,
    paintings[("Hidalgo", "watercolor")]["position"] == 0
)

# Now we need to add the constraint about no wall having only one student
# Let's try to add this constraint properly
# For each wall, we need to ensure that the two paintings are from different students
# We can do this by ensuring that for each wall, there are at least 2 students with paintings

# We'll create a helper function to check if a student has a painting on a wall
def student_has_painting_on_wall(student, wall):
    return Or(
        paintings[(student, "oil")]["wall"] == wall,
        paintings[(student, "watercolor")]["wall"] == wall
    )

# For each wall, we need at least 2 students with paintings
# We'll create a constraint for each wall
for w in walls:
    # Count how many students have paintings on this wall
    # We'll use a sum of indicators
    student_count = Sum([If(student_has_painting_on_wall(s, w), 1, 0) for s in students])
    solver.add(student_count >= 2)

# Now let's test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
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