from z3 import *

solver = Solver()

# Constants for historians and topics
Farley, Garcia, Holden, Jiang = Ints('Farley Garcia Holden Jiang')
Lithographs, OilPaintings, Sculptures, Watercolors = Ints('Lithographs OilPaintings Sculptures Watercolors')

# Assign constant values for clarity
solver.add(Farley == 0, Garcia == 1, Holden == 2, Jiang == 3)
solver.add(Lithographs == 0, OilPaintings == 1, Sculptures == 2, Watercolors == 3)

# Use Arrays for historian and topic assignments to allow symbolic indexing
historian_arr = Array('historian_arr', IntSort(), IntSort())
topic_arr = Array('topic_arr', IntSort(), IntSort())

# Positions are 0, 1, 2, 3 (0 = first, 3 = last)
# Each position has a unique historian and a unique topic
# We will enforce uniqueness by adding constraints

# Helper: All historians are distinct
solver.add(historian_arr[0] != historian_arr[1])
solver.add(historian_arr[0] != historian_arr[2])
solver.add(historian_arr[0] != historian_arr[3])
solver.add(historian_arr[1] != historian_arr[2])
solver.add(historian_arr[1] != historian_arr[3])
solver.add(historian_arr[2] != historian_arr[3])

# Helper: All topics are distinct
solver.add(topic_arr[0] != topic_arr[1])
solver.add(topic_arr[0] != topic_arr[2])
solver.add(topic_arr[0] != topic_arr[3])
solver.add(topic_arr[1] != topic_arr[2])
solver.add(topic_arr[1] != topic_arr[3])
solver.add(topic_arr[2] != topic_arr[3])

# Base constraints from the problem
# 1. Oil paintings and watercolors must be earlier than lithographs
#    So lithographs cannot be in position 0 or 1
solver.add(topic_arr[0] != Lithographs)
solver.add(topic_arr[1] != Lithographs)

# 2. Farley's lecture must be earlier than the oil paintings lecture
#    So if oil paintings is at position i, Farley must be at position j < i
#    We need to find the position of oil paintings and ensure Farley is before it

# 3. Holden's lecture must be earlier than both Garcia's and Jiang's lectures
#    So Holden's position < Garcia's position and Holden's position < Jiang's position

# Additional constraint: Watercolors lecture is third (position 2)
solver.add(topic_arr[2] == Watercolors)

# Enforce Farley is before oil paintings
# We need to ensure that for the position of oil paintings, Farley is before it
# We will use a helper function to enforce this

def farley_before_oil():
    # Oil paintings can be at position 0, 1, 2, or 3
    # But watercolors is at position 2, so oil paintings cannot be at position 2
    # Lithographs must be after oil paintings, so oil paintings cannot be at position 3
    # So oil paintings can only be at position 0 or 1
    # If oil paintings is at position 0, Farley cannot be before it, so oil paintings must be at position 1
    # Therefore, Farley must be at position 0
    solver.add(Or(
        And(topic_arr[0] == OilPaintings, historian_arr[0] == Farley),
        And(topic_arr[1] == OilPaintings, historian_arr[0] == Farley)
    ))
    # If oil paintings is at position 1, Farley must be at position 0
    solver.add(Implies(topic_arr[1] == OilPaintings, historian_arr[0] == Farley))

farley_before_oil()

# Enforce Holden is before Garcia and Jiang
# We need to ensure that Holden's position is less than Garcia's and Jiang's
# We will use a helper function to enforce this

def holden_before_garcia_jiang():
    # Find Garcia's position
    g_pos = Int('g_pos')
    solver.add(Or(
        And(historian_arr[0] == Garcia, g_pos == 0),
        And(historian_arr[1] == Garcia, g_pos == 1),
        And(historian_arr[2] == Garcia, g_pos == 2),
        And(historian_arr[3] == Garcia, g_pos == 3)
    ))
    # Find Jiang's position
    j_pos = Int('j_pos')
    solver.add(Or(
        And(historian_arr[0] == Jiang, j_pos == 0),
        And(historian_arr[1] == Jiang, j_pos == 1),
        And(historian_arr[2] == Jiang, j_pos == 2),
        And(historian_arr[3] == Jiang, j_pos == 3)
    ))
    # Holden must be before Garcia and Jiang
    solver.add(historian_arr[0] == Holden)
    solver.add(Or(
        And(g_pos == 1, historian_arr[0] == Holden),
        And(g_pos == 2, historian_arr[0] == Holden),
        And(g_pos == 3, historian_arr[0] == Holden)
    ))
    solver.add(Or(
        And(j_pos == 1, historian_arr[0] == Holden),
        And(j_pos == 2, historian_arr[0] == Holden),
        And(j_pos == 3, historian_arr[0] == Holden)
    ))

holden_before_garcia_jiang()

# Now, define the options as constraints and test them

# Option A: Farley gives the watercolors lecture
# Since watercolors is at position 2, this means historian_arr[2] == Farley
opt_a_constr = (historian_arr[2] == Farley)

# Option B: Garcia gives the oil paintings lecture
# Oil paintings is at position 1, so this means historian_arr[1] == Garcia
opt_b_constr = (historian_arr[1] == Garcia)

# Option C: Garcia gives the sculptures lecture
opt_c_constr = Or(
    And(topic_arr[0] == Sculptures, historian_arr[0] == Garcia),
    And(topic_arr[1] == Sculptures, historian_arr[1] == Garcia),
    And(topic_arr[2] == Sculptures, historian_arr[2] == Garcia),
    And(topic_arr[3] == Sculptures, historian_arr[3] == Garcia)
)

# Option D: Holden gives the sculptures lecture
opt_d_constr = Or(
    And(topic_arr[0] == Sculptures, historian_arr[0] == Holden),
    And(topic_arr[1] == Sculptures, historian_arr[1] == Holden),
    And(topic_arr[2] == Sculptures, historian_arr[2] == Holden),
    And(topic_arr[3] == Sculptures, historian_arr[3] == Holden)
)

# Option E: Jiang gives the lithographs lecture
# Lithographs must be at position 3 (since it must be after oil paintings and watercolors)
opt_e_constr = (historian_arr[3] == Jiang)

# Now, test each option
found_options = []
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