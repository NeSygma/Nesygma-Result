from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Define building classes
# Class 1: garza_tower, flores_tower
# Class 2: lynch_building, king_building, meyer_building, ortiz_building
# Class 3: yates_house, zimmer_house

# Assign unique IDs to buildings
garza_tower = 0
flores_tower = 1
lynch_building = 2
king_building = 3
meyer_building = 4
ortiz_building = 5
yates_house = 6
zimmer_house = 7

# Company IDs
realprop = 0
southco = 1
trustcorp = 2

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
# Each company owns exactly 3 buildings
current_ownership = [[Int(f"rp_{i}") for i in range(3)],  # RealProp
                     [Int(f"sc_{i}") for i in range(3)],  # Southco
                     [Int(f"tc_{i}") for i in range(3)]]  # Trustcorp

# Ensure all buildings in current_ownership are distinct for each company
solver = Solver()
solver.add(Distinct(current_ownership[0]))
solver.add(Distinct(current_ownership[1]))
solver.add(Distinct(current_ownership[2]))

# Helper function to check if a building is owned by a company
def owns(company, building):
    return Or([current_ownership[company][i] == building for i in range(3)])

# Option A: The buildings owned by RealProp are the Flores Tower and the Garza Tower.
# This implies RealProp owns exactly two buildings: garza_tower and flores_tower.
# But RealProp must own 3 buildings, so this is impossible.
opt_a_constr = And(
    owns(realprop, garza_tower),
    owns(realprop, flores_tower),
    Not(Or(owns(realprop, yates_house), owns(realprop, zimmer_house)))
)

# Option B: The buildings owned by Southco are the Flores Tower and the Meyer Building.
# Southco must own 3 buildings, so this is possible if it also owns one more building.
opt_b_constr = And(
    owns(southco, flores_tower),
    owns(southco, meyer_building),
    Or(owns(southco, lynch_building), owns(southco, king_building), owns(southco, ortiz_building))
)

# Option C: The buildings owned by Southco are the Garza Tower and the Lynch Building.
# Southco must own 3 buildings, so this is possible if it also owns one more building.
opt_c_constr = And(
    owns(southco, garza_tower),
    owns(southco, lynch_building),
    Or(owns(southco, flores_tower), owns(southco, king_building), owns(southco, meyer_building), owns(southco, ortiz_building))
)

# Option D: The buildings owned by Trustcorp are the Flores Tower and the Ortiz Building.
# Trustcorp must own 3 buildings, so this is possible if it also owns one more building.
opt_d_constr = And(
    owns(trustcorp, flores_tower),
    owns(trustcorp, ortiz_building),
    Or(owns(trustcorp, king_building), owns(trustcorp, meyer_building))
)

# Option E: The buildings owned by Trustcorp are the Garza Tower and the Meyer Building.
# Trustcorp must own 3 buildings, so this is possible if it also owns one more building.
opt_e_constr = And(
    owns(trustcorp, garza_tower),
    owns(trustcorp, meyer_building),
    Or(owns(trustcorp, king_building), owns(trustcorp, ortiz_building))
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