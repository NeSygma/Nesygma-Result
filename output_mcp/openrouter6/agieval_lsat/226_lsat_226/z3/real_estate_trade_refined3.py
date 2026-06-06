from z3 import *

# Company indices
R, S, T = 0, 1, 2
company_names = ["RealProp", "Southco", "Trustcorp"]

# Buildings with their classes
buildings = [
    "Garza Tower",   # class 1
    "Yates House",   # class 3
    "Zimmer House",  # class 3
    "Flores Tower",  # class 1
    "Lynch Building", # class 2
    "King Building", # class 2
    "Meyer Building", # class 2
    "Ortiz Building" # class 2
]

building_classes = {
    "Garza Tower": 1,
    "Yates House": 3,
    "Zimmer House": 3,
    "Flores Tower": 1,
    "Lynch Building": 2,
    "King Building": 2,
    "Meyer Building": 2,
    "Ortiz Building": 2
}

# Initial ownership
initial_owner = {
    "Garza Tower": R,
    "Yates House": R,
    "Zimmer House": R,
    "Flores Tower": S,
    "Lynch Building": S,
    "King Building": T,
    "Meyer Building": T,
    "Ortiz Building": T
}

# Final ownership for each option
option_final_owners = {
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

def check_option(option_letter):
    """Check if the given option is reachable via exactly one valid trade."""
    solver = Solver()
    
    # Get final ownership for this option
    final_owners_dict = option_final_owners[option_letter]
    
    # Convert to building -> owner mapping
    final_owner = {}
    for company_name, building_list in final_owners_dict.items():
        company_idx = company_names.index(company_name)
        for building in building_list:
            final_owner[building] = company_idx
    
    # Define symbolic variables for the trade
    c1 = Int('c1')  # First company in trade
    c2 = Int('c2')  # Second company in trade
    t = Int('t')    # Trade type (1, 2, or 3)
    
    # Constraints on company indices
    solver.add(c1 >= 0, c1 <= 2)
    solver.add(c2 >= 0, c2 <= 2)
    solver.add(c1 < c2)  # Avoid duplicate pairs
    
    # Constraints on trade type
    solver.add(t >= 1, t <= 3)
    
    # For each building, define whether it's transferred
    transfers_c1_to_c2 = []
    transfers_c2_to_c1 = []
    
    for building in buildings:
        init_owner = initial_owner[building]
        final_owner_val = final_owner[building]
        building_class = building_classes[building]
        
        # Check if building is transferred from c1 to c2
        is_c1_to_c2 = And(init_owner == c1, final_owner_val == c2)
        # Check if building is transferred from c2 to c1
        is_c2_to_c1 = And(init_owner == c2, final_owner_val == c1)
        
        transfers_c1_to_c2.append(is_c1_to_c2)
        transfers_c2_to_c1.append(is_c2_to_c1)
        
        # For each building, final owner must be either:
        # 1. Same as initial owner (not transferred)
        # 2. c2 if initial owner is c1 (transferred from c1 to c2)
        # 3. c1 if initial owner is c2 (transferred from c2 to c1)
        solver.add(Or(
            final_owner_val == init_owner,
            And(init_owner == c1, final_owner_val == c2),
            And(init_owner == c2, final_owner_val == c1)
        ))
    
    # Count transfers
    count_c1_to_c2 = Sum([If(tc, 1, 0) for tc in transfers_c1_to_c2])
    count_c2_to_c1 = Sum([If(tc, 1, 0) for tc in transfers_c2_to_c1])
    
    # Trade type constraints
    # Type 1: One building for one building of same class
    type1 = And(count_c1_to_c2 == 1, count_c2_to_c1 == 1)
    
    # For type 1, the two transferred buildings must have same class
    # We need to find the class of the building transferred from c1 to c2
    # and from c2 to c1, and ensure they're equal
    class_c1_to_c2 = Int('class_c1_to_c2')
    class_c2_to_c1 = Int('class_c2_to_c1')
    
    # Find the class of the building transferred from c1 to c2
    class_constraints_c1_to_c2 = []
    for i, building in enumerate(buildings):
        class_val = building_classes[building]
        class_constraints_c1_to_c2.append(
            Implies(transfers_c1_to_c2[i], class_c1_to_c2 == class_val)
        )
    solver.add(Or(class_constraints_c1_to_c2))
    
    # Find the class of the building transferred from c2 to c1
    class_constraints_c2_to_c1 = []
    for i, building in enumerate(buildings):
        class_val = building_classes[building]
        class_constraints_c2_to_c1.append(
            Implies(transfers_c2_to_c1[i], class_c2_to_c1 == class_val)
        )
    solver.add(Or(class_constraints_c2_to_c1))
    
    # For type 1, classes must be equal
    type1_class = (class_c1_to_c2 == class_c2_to_c1)
    solver.add(Implies(t == 1, And(type1, type1_class)))
    
    # Type 2: One class 1 building from c1 to c2, two class 2 buildings from c2 to c1
    count_class1_c1_to_c2 = Sum([
        If(And(transfers_c1_to_c2[i], building_classes[buildings[i]] == 1), 1, 0)
        for i in range(len(buildings))
    ])
    count_class2_c2_to_c1 = Sum([
        If(And(transfers_c2_to_c1[i], building_classes[buildings[i]] == 2), 1, 0)
        for i in range(len(buildings))
    ])
    type2 = And(count_class1_c1_to_c2 == 1, count_class2_c2_to_c1 == 2)
    solver.add(Implies(t == 2, type2))
    
    # Type 3: One class 2 building from c1 to c2, two class 3 buildings from c2 to c1
    count_class2_c1_to_c2 = Sum([
        If(And(transfers_c1_to_c2[i], building_classes[buildings[i]] == 2), 1, 0)
        for i in range(len(buildings))
    ])
    count_class3_c2_to_c1 = Sum([
        If(And(transfers_c2_to_c1[i], building_classes[buildings[i]] == 3), 1, 0)
        for i in range(len(buildings))
    ])
    type3 = And(count_class2_c1_to_c2 == 1, count_class3_c2_to_c1 == 2)
    solver.add(Implies(t == 3, type3))
    
    # Check if satisfiable
    result = solver.check()
    if result == sat:
        # Print some debug info
        m = solver.model()
        print(f"Option {option_letter}: SAT")
        print(f"  Trade between companies {m[c1]} and {m[c2]}")
        print(f"  Trade type: {m[t]}")
        
        # Print which buildings are transferred
        print(f"  Buildings transferred from c1 to c2:")
        for i, building in enumerate(buildings):
            if m.eval(transfers_c1_to_c2[i]) == True:
                print(f"    {building} (class {building_classes[building]})")
        print(f"  Buildings transferred from c2 to c1:")
        for i, building in enumerate(buildings):
            if m.eval(transfers_c2_to_c1[i]) == True:
                print(f"    {building} (class {building_classes[building]})")
    return result == sat

# Evaluate all options using the exact skeleton
found_options = []
for letter in ["A", "B", "C", "D", "E"]:
    solver = Solver()
    # We'll use the check_option function directly
    if check_option(letter):
        found_options.append(letter)

# Print results using the required format
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")