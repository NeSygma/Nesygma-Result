from z3 import *

solver = Solver()

# Declare symbolic variables for the order of recruitment
# We have 7 accomplices: Peters (0), Quinn (1), Rovero (2), Stanton (3), Tao (4), Villas (5), White (6)
# We represent their recruitment order as integers from 0 to 6 (0 = first, 6 = last)

# Create a list of integers representing the order
order = [Int(f"order_{i}") for i in range(7)]

# Each position in the order must be unique (one accomplice per position)
solver.add(Distinct(order))

# Each accomplice is assigned a unique position
# We will enforce this by ensuring all values in `order` are between 0 and 6
for pos in order:
    solver.add(pos >= 0, pos <= 6)

# Peters was recruited fourth (position 3, since 0 is first)
# Peters is represented as 0
solver.add(order[3] == 0)

# Villas was recruited immediately before White
# This means that in the order list, Villas (5) must appear immediately before White (6)
# We need to find the index of Villas and White in the order list
villan_pos = Int("villan_pos")
white_pos = Int("white_pos")
solver.add(Or([And(villan_pos == i, white_pos == i + 1, order[i] == 5, order[i + 1] == 6) for i in range(6)]))

# Quinn was recruited earlier than Rovero
# This means the index of Quinn (1) in the order list must be less than the index of Rovero (2)
quinn_pos = Int("quinn_pos")
rovero_pos = Int("rovero_pos")
solver.add(Or([And(quinn_pos == i, rovero_pos == j, i < j, order[i] == 1, order[j] == 2) for i in range(7) for j in range(7) if i < j]))

# Stanton was recruited neither immediately before nor immediately after Tao
# This means the indices of Stanton (3) and Tao (4) in the order list must not be consecutive
stanton_pos = Int("stanton_pos")
tao_pos = Int("tao_pos")
solver.add(Or([And(stanton_pos == i, tao_pos == j, 
                   And(i != j - 1, i != j + 1), order[i] == 3, order[j] == 4) 
               for i in range(7) for j in range(7) if i != j]))

# Now, let's define the options as constraints on the middle five positions (indices 1 to 5)
# We will test each option to see if it is consistent with the constraints

# Helper function to check if an option is valid
def check_option(option_name, option_constraints):
    solver.push()
    solver.add(option_constraints)
    result = solver.check()
    solver.pop()
    return result == sat

# Define the options as constraints on the order list
# The middle five positions are indices 1 to 5 (0-based)

# Option A: Quinn, Stanton, Peters, Tao, Villas
# This means:
# order[1] = Quinn (1)
# order[2] = Stanton (3)
# order[3] = Peters (0) (already fixed)
# order[4] = Tao (4)
# order[5] = Villas (5)
opt_a_constr = And(
    order[1] == 1,  # Quinn
    order[2] == 3,  # Stanton
    order[4] == 4,  # Tao
    order[5] == 5,  # Villas
)

# Option B: Quinn, Stanton, Peters, Tao, White
# order[1] = Quinn (1)
# order[2] = Stanton (3)
# order[3] = Peters (0)
# order[4] = Tao (4)
# order[5] = White (6)
opt_b_constr = And(
    order[1] == 1,  # Quinn
    order[2] == 3,  # Stanton
    order[4] == 4,  # Tao
    order[5] == 6,  # White
)

# Option C: Villas, White, Peters, Quinn, Stanton
# order[1] = Villas (5)
# order[2] = White (6)
# order[3] = Peters (0)
# order[4] = Quinn (1)
# order[5] = Stanton (3)
opt_c_constr = And(
    order[1] == 5,  # Villas
    order[2] == 6,  # White
    order[4] == 1,  # Quinn
    order[5] == 3,  # Stanton
)

# Option D: Villas, White, Peters, Rovero, Stanton
# order[1] = Villas (5)
# order[2] = White (6)
# order[3] = Peters (0)
# order[4] = Rovero (2)
# order[5] = Stanton (3)
opt_d_constr = And(
    order[1] == 5,  # Villas
    order[2] == 6,  # White
    order[4] == 2,  # Rovero
    order[5] == 3,  # Stanton
)

# Option E: Villas, White, Quinn, Rovero, Stanton
# order[1] = Villas (5)
# order[2] = White (6)
# order[3] = Peters (0)
# order[4] = Quinn (1)
# order[5] = Rovero (2)
opt_e_constr = And(
    order[1] == 5,  # Villas
    order[2] == 6,  # White
    order[4] == 1,  # Quinn
    order[5] == 2,  # Rovero
)

# Now, test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    if check_option(letter, constr):
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")