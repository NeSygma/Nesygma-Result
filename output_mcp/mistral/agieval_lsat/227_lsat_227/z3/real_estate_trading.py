from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Define building classes
class1_buildings = ["Garza Tower", "Flores Tower"]
class2_buildings = ["Lynch Building", "King Building", "Meyer Building", "Ortiz Building"]
class3_buildings = ["Yates House", "Zimmer House"]

# Initial ownership
realprop_initial = set(["Garza Tower", "Yates House", "Zimmer House"])
southco_initial = set(["Flores Tower", "Lynch Building"])
trustcorp_initial = set(["King Building", "Meyer Building", "Ortiz Building"])

# All buildings
all_buildings = set(class1_buildings + class2_buildings + class3_buildings)

# Helper function to get class of a building
def get_class(building):
    if building in class1_buildings:
        return 1
    elif building in class2_buildings:
        return 2
    elif building in class3_buildings:
        return 3
    else:
        raise ValueError(f"Unknown building: {building}")

# Helper function to check if a trade is valid
def is_valid_trade(trade_type, building1, building2=None):
    if trade_type == 1:  # Trade one building for one other building of the same class
        return get_class(building1) == get_class(building2)
    elif trade_type == 2:  # Trade one class 1 building for two class 2 buildings
        return get_class(building1) == 1 and building2 is None
    elif trade_type == 3:  # Trade one class 2 building for two class 3 buildings
        return get_class(building1) == 2 and building2 is None
    else:
        raise ValueError(f"Unknown trade type: {trade_type}")

# Helper function to apply a trade and return new ownership
# This is a simplified model: we assume trades can be applied in any order and any number of times
# We model the reachable states by tracking the number of buildings of each class per company
# This is a heuristic to avoid state explosion; a full model would require a more complex representation

# Instead, we model the problem as a constraint on the possible ownership sets
# We assume that trades can be applied to change the ownership, but we do not model the exact sequence

# For the purpose of this problem, we will model the possible ownership sets for each company
# and check if the desired state in each option is reachable

# We will use a solver to check if the desired state is possible

# Define the solver
solver = Solver()

# We will model the problem by tracking the number of buildings of each class per company
# This is a simplified approach to avoid state explosion

# Let's define variables for the number of class 1, 2, and 3 buildings owned by each company
# We will use integers to represent the counts
rp_class1 = Int('rp_class1')
rp_class2 = Int('rp_class2')
rp_class3 = Int('rp_class3')

sc_class1 = Int('sc_class1')
sc_class2 = Int('sc_class2')
sc_class3 = Int('sc_class3')

tr_class1 = Int('tr_class1')
tr_class2 = Int('tr_class2')
tr_class3 = Int('tr_class3')

# Initial counts
solver.add(rp_class1 == 1, rp_class2 == 0, rp_class3 == 2)
solver.add(sc_class1 == 1, sc_class2 == 1, sc_class3 == 0)
solver.add(tr_class1 == 0, tr_class2 == 3, tr_class3 == 0)

# Trade constraints
# Trade type 1: Trade one building for one other building of the same class
# This does not change the count of buildings of that class
# Trade type 2: Trade one class 1 building for two class 2 buildings
# This decreases class 1 by 1 and increases class 2 by 2
# Trade type 3: Trade one class 2 building for two class 3 buildings
# This decreases class 2 by 1 and increases class 3 by 2

# We will model the possible trades as constraints on the counts
# The exact sequence of trades is not modeled; we only model the possible final counts

# The total number of buildings per company is fixed (3 for RealProp and Trustcorp, 2 for Southco)
# So we add constraints to ensure the total number of buildings is correct
solver.add(rp_class1 + rp_class2 + rp_class3 == 3)
solver.add(sc_class1 + sc_class2 + sc_class3 == 2)
solver.add(tr_class1 + tr_class2 + tr_class3 == 3)

# Now, we will check each option to see if it is possible

# Option A: The buildings owned by RealProp are the Flores Tower and the Garza Tower.
# This means RealProp owns 2 class 1 buildings and 0 class 2 and 0 class 3 buildings.
opt_a_constr = And(rp_class1 == 2, rp_class2 == 0, rp_class3 == 0)

# Option B: The buildings owned by Southco are the Flores Tower and the Meyer Building.
# Flores Tower is class 1, Meyer Building is class 2
# So Southco owns 1 class 1 and 1 class 2 building
opt_b_constr = And(sc_class1 == 1, sc_class2 == 1, sc_class3 == 0)

# Option C: The buildings owned by Southco are the Garza Tower and the Lynch Building.
# Garza Tower is class 1, Lynch Building is class 2
# So Southco owns 1 class 1 and 1 class 2 building
opt_c_constr = And(sc_class1 == 1, sc_class2 == 1, sc_class3 == 0)

# Option D: The buildings owned by Trustcorp are the Flores Tower and the Ortiz Building.
# Flores Tower is class 1, Ortiz Building is class 2
# So Trustcorp owns 1 class 1 and 1 class 2 building, and 1 class 3 building (since total is 3)
opt_d_constr = And(tr_class1 == 1, tr_class2 == 1, tr_class3 == 1)

# Option E: The buildings owned by Trustcorp are the Garza Tower and the Meyer Building.
# Garza Tower is class 1, Meyer Building is class 2
# So Trustcorp owns 1 class 1 and 1 class 2 building, and 1 class 3 building (since total is 3)
opt_e_constr = And(tr_class1 == 1, tr_class2 == 1, tr_class3 == 1)

# Now, we will check each option for satisfiability
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