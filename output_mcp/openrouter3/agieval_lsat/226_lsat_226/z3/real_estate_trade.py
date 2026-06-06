from z3 import *

# Define building classes
# Buildings: Garza, Yates, Zimmer, Flores, Lynch, King, Meyer, Ortiz
# Classes: 1, 3, 3, 1, 2, 2, 2, 2

# We'll model ownership as variables for each building
# For each building, we track which company owns it after the trade
# Companies: 0=RealProp, 1=Southco, 2=Trustcorp

buildings = ["Garza", "Yates", "Zimmer", "Flores", "Lynch", "King", "Meyer", "Ortiz"]
classes = [1, 3, 3, 1, 2, 2, 2, 2]

# Initial ownership
initial_owner = {
    "Garza": 0, "Yates": 0, "Zimmer": 0,
    "Flores": 1, "Lynch": 1,
    "King": 2, "Meyer": 2, "Ortiz": 2
}

# Create variables for final ownership
owner = {b: Int(f"owner_{b}") for b in buildings}

# Base constraints: each building owned by exactly one company
solver = Solver()
for b in buildings:
    solver.add(Or([owner[b] == i for i in range(3)]))

# Constraint: exactly one trade occurred
# A trade involves two companies exchanging buildings according to the rules
# We need to model that the ownership changed for exactly two buildings (or more for class exchanges)

# Let's think about what a trade means:
# Option 1: Same class exchange - two buildings swap owners
# Option 2: Class 1 for two class 2 - one building from company A goes to B, two from B go to A
# Option 3: Class 2 for two class 3 - similar pattern

# We need to ensure that the final state differs from initial by exactly one trade operation

# Let's create a more direct approach: check each option by adding constraints that match the option's ownership
# and then check if it's reachable with exactly one trade

# First, let's define the trade rules more formally
# For each possible trade, we need to check if the ownership change matches one of the rules

# We'll create a function to check if a given ownership assignment is reachable with exactly one trade
def is_reachable_with_one_trade(final_ownership):
    # Check if the difference from initial ownership can be explained by exactly one trade
    
    # Count how many buildings changed hands
    changes = []
    for b in buildings:
        if final_ownership[b] != initial_owner[b]:
            changes.append(b)
    
    # If no changes, not a trade
    if len(changes) == 0:
        return False
    
    # If more than 4 buildings changed, likely more than one trade (but could be class 1 for 2 class 2)
    if len(changes) > 4:
        return False
    
    # Check possible trade patterns
    # Pattern 1: Same class exchange (2 buildings swap)
    if len(changes) == 2:
        b1, b2 = changes[0], changes[1]
        # Check if they swapped owners
        if (final_ownership[b1] == initial_owner[b2] and 
            final_ownership[b2] == initial_owner[b1]):
            # Check same class
            if classes[buildings.index(b1)] == classes[buildings.index(b2)]:
                return True
    
    # Pattern 2: Class 1 for two class 2
    # One class 1 building moves from A to B, two class 2 buildings move from B to A
    if len(changes) == 3:
        # Find the class 1 building
        class1_building = None
        class2_buildings = []
        for b in changes:
            idx = buildings.index(b)
            if classes[idx] == 1:
                class1_building = b
            elif classes[idx] == 2:
                class2_buildings.append(b)
        
        if class1_building is not None and len(class2_buildings) == 2:
            # Check ownership pattern
            owner_class1_initial = initial_owner[class1_building]
            owner_class1_final = final_ownership[class1_building]
            
            # The class 1 building should move to a different company
            if owner_class1_initial != owner_class1_final:
                # The two class 2 buildings should move from the new owner of class1 to the old owner
                for b in class2_buildings:
                    if final_ownership[b] != owner_class1_initial:
                        return False
                    if initial_owner[b] != owner_class1_final:
                        return False
                return True
    
    # Pattern 3: Class 2 for two class 3
    # One class 2 building moves from A to B, two class 3 buildings move from B to A
    if len(changes) == 3:
        # Find the class 2 building
        class2_building = None
        class3_buildings = []
        for b in changes:
            idx = buildings.index(b)
            if classes[idx] == 2:
                class2_building = b
            elif classes[idx] == 3:
                class3_buildings.append(b)
        
        if class2_building is not None and len(class3_buildings) == 2:
            # Check ownership pattern
            owner_class2_initial = initial_owner[class2_building]
            owner_class2_final = final_ownership[class2_building]
            
            # The class 2 building should move to a different company
            if owner_class2_initial != owner_class2_final:
                # The two class 3 buildings should move from the new owner of class2 to the old owner
                for b in class3_buildings:
                    if final_ownership[b] != owner_class2_initial:
                        return False
                    if initial_owner[b] != owner_class2_final:
                        return False
                return True
    
    return False

# Now test each option
options = {
    "A": {
        "RealProp": ["Flores Tower", "Garza Tower"],
        "Southco": ["Lynch Building", "Yates House", "Zimmer House"],
        "Trustcorp": ["King Building", "Meyer Building", "Ortiz Building"]
    },
    "B": {
        "RealProp": ["Garza Tower", "King Building", "Ortiz Building"],
        "Southco": ["Flores Tower", "Lynch Building"],
        "Trustcorp": ["Meyer Building", "Yates House", "Zimmer House"]
    },
    "C": {
        "RealProp": ["Garza Tower", "Lynch Building"],
        "Southco": ["Flores Tower", "Yates House", "Zimmer House"],
        "Trustcorp": ["King Building", "Meyer Building", "Ortiz Building"]
    },
    "D": {
        "RealProp": ["Garza Tower", "Meyer Building", "Yates House"],
        "Southco": ["Flores Tower", "Lynch Building"],
        "Trustcorp": ["King Building", "Ortiz Building", "Zimmer House"]
    },
    "E": {
        "RealProp": ["Garza Tower", "Yates House", "Zimmer House"],
        "Southco": ["Lynch Building", "Ortiz Building"],
        "Trustcorp": ["Flores Tower", "King Building", "Meyer Building"]
    }
}

# Map building names to our internal names
building_name_map = {
    "Garza Tower": "Garza",
    "Yates House": "Yates",
    "Zimmer House": "Zimmer",
    "Flores Tower": "Flores",
    "Lynch Building": "Lynch",
    "King Building": "King",
    "Meyer Building": "Meyer",
    "Ortiz Building": "Ortiz"
}

# Company mapping
company_map = {"RealProp": 0, "Southco": 1, "Trustcorp": 2}

found_options = []
for letter, option in options.items():
    # Create final ownership mapping for this option
    final_ownership = {}
    for company, building_list in option.items():
        company_id = company_map[company]
        for building_name in building_list:
            building = building_name_map[building_name]
            final_ownership[building] = company_id
    
    # Check if this ownership is reachable with exactly one trade
    if is_reachable_with_one_trade(final_ownership):
        found_options.append(letter)

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")