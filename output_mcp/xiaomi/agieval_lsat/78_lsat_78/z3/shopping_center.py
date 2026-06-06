from z3 import *

solver = Solver()

# Define the businesses
# 0: optometrist, 1: pharmacy, 2: restaurant1, 3: restaurant2, 4: shoe store, 5: toy store, 6: veterinarian
businesses = [Int(f'biz_{i}') for i in range(7)]

# Each business is assigned to a space 1-7
for biz in businesses:
    solver.add(biz >= 1, biz <= 7)

# All businesses are in different spaces
solver.add(Distinct(businesses))

# The pharmacy must be at one end of the row and one of the restaurants at the other.
# Ends are spaces 1 and 7.
# Pharmacy is business 1, restaurants are businesses 2 and 3.
solver.add(Or(
    And(businesses[1] == 1, Or(businesses[2] == 7, businesses[3] == 7)),
    And(businesses[1] == 7, Or(businesses[2] == 1, businesses[3] == 1))
))

# The two restaurants must be separated by at least two other businesses.
# This means |businesses[2] - businesses[3]| >= 3
solver.add(Abs(businesses[2] - businesses[3]) >= 3)

# The pharmacy must be next to either the optometrist or the veterinarian.
# Next to means |businesses[1] - businesses[0]| == 1 or |businesses[1] - businesses[6]| == 1
solver.add(Or(
    Abs(businesses[1] - businesses[0]) == 1,
    Abs(businesses[1] - businesses[6]) == 1
))

# The toy store cannot be next to the veterinarian.
# |businesses[5] - businesses[6]| != 1
solver.add(Abs(businesses[5] - businesses[6]) != 1)

# Given: The veterinarian is in space 5.
solver.add(businesses[6] == 5)

# Define the options
opt_a_constr = (businesses[0] == 2)  # The optometrist is in space 2.
opt_b_constr = (businesses[1] == 7)  # The pharmacy is in space 7.
opt_c_constr = Or(businesses[2] == 4, businesses[3] == 4)  # A restaurant is in space 4.
opt_d_constr = (businesses[4] == 6)  # The shoe store is in space 6.
opt_e_constr = (businesses[5] == 3)  # The toy store is in space 3.

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