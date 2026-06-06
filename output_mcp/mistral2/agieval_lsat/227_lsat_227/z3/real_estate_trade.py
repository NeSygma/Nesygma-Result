from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Define building classes
# Class 1: Garza Tower (RealProp), Flores Tower (Southco)
# Class 2: Lynch Building (Southco), King Building (Trustcorp), Meyer Building (Trustcorp), Ortiz Building (Trustcorp)
# Class 3: Yates House (RealProp), Zimmer House (RealProp)

# Assign unique IDs to buildings for easier handling
# Class 1
garza_tower = 0  # RealProp
flores_tower = 1  # Southco

# Class 2
lynch_building = 2  # Southco
king_building = 3   # Trustcorp
meyer_building = 4  # Trustcorp
ortiz_building = 5  # Trustcorp

# Class 3
yates_house = 6  # RealProp
zimmer_house = 7  # RealProp

# Total buildings
buildings = [garza_tower, flores_tower, lynch_building, king_building, meyer_building, ortiz_building, yates_house, zimmer_house]

# Company IDs
realprop = 0
southco = 1
trustcorp = 2

# Initial building ownership
initial_ownership = [
    [garza_tower, yates_house, zimmer_house],  # RealProp
    [flores_tower, lynch_building],            # Southco
    [king_building, meyer_building, ortiz_building]  # Trustcorp
]

# Class of each building
building_class = {
    garza_tower: 1,
    flores_tower: 1,
    lynch_building: 2,
    king_building: 2,
    meyer_building: 2,
    ortiz_building: 2,
    yates_house: 3,
    zimmer_house: 3
}

# Current ownership (symbolic)
current_ownership = [[Int(f"rp_{i}") for i in range(3)],  # RealProp
                     [Int(f"sc_{i}") for i in range(2)],  # Southco
                     [Int(f"tc_{i}") for i in range(3)]]  # Trustcorp

# Initialize ownership to initial state
solver = Solver()
for j in range(len(initial_ownership[0])):
    solver.add(current_ownership[0][j] == initial_ownership[0][j])
for j in range(len(initial_ownership[1])):
    solver.add(current_ownership[1][j] == initial_ownership[1][j])
for j in range(len(initial_ownership[2])):
    solver.add(current_ownership[2][j] == initial_ownership[2][j])

# Ensure all buildings in current_ownership are distinct for each company
solver.add(Distinct(current_ownership[0]))
solver.add(Distinct(current_ownership[1]))
solver.add(Distinct(current_ownership[2]))

# Now, we will check each option to see if it is possible.

# Option A: The buildings owned by RealProp are the Flores Tower and the Garza Tower.
# This means RealProp owns exactly two buildings: garza_tower and flores_tower.
# But RealProp must own 3 buildings, so this is impossible.
opt_a_constr = And(
    current_ownership[0][0] == garza_tower,
    current_ownership[0][1] == flores_tower,
    current_ownership[0][2] == yates_house  # Must have 3 buildings
)

# Option B: The buildings owned by Southco are the Flores Tower and the Meyer Building.
opt_b_constr = And(
    current_ownership[1][0] == flores_tower,
    current_ownership[1][1] == meyer_building,
    current_ownership[2][0] == king_building,
    current_ownership[2][1] == ortiz_building,
    current_ownership[2][2] == meyer_building
)

# Option C: The buildings owned by Southco are the Garza Tower and the Lynch Building.
opt_c_constr = And(
    current_ownership[1][0] == garza_tower,
    current_ownership[1][1] == lynch_building,
    current_ownership[0][0] == flores_tower,
    current_ownership[0][1] == yates_house,
    current_ownership[0][2] == zimmer_house,
    current_ownership[2][0] == king_building,
    current_ownership[2][1] == meyer_building,
    current_ownership[2][2] == ortiz_building
)

# Option D: The buildings owned by Trustcorp are the Flores Tower and the Ortiz Building.
opt_d_constr = And(
    current_ownership[2][0] == flores_tower,
    current_ownership[2][1] == ortiz_building,
    current_ownership[2][2] == king_building,  # Trustcorp must own 3 buildings
    current_ownership[1][0] == lynch_building,
    current_ownership[1][1] == meyer_building,
    current_ownership[0][0] == garza_tower,
    current_ownership[0][1] == yates_house,
    current_ownership[0][2] == zimmer_house
)

# Option E: The buildings owned by Trustcorp are the Garza Tower and the Meyer Building.
opt_e_constr = And(
    current_ownership[2][0] == garza_tower,
    current_ownership[2][1] == meyer_building,
    current_ownership[2][2] == king_building,  # Trustcorp must own 3 buildings
    current_ownership[1][0] == flores_tower,
    current_ownership[1][1] == lynch_building,
    current_ownership[0][0] == yates_house,
    current_ownership[0][1] == zimmer_house,
    current_ownership[0][2] == ortiz_building
)

# Now, check each option
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