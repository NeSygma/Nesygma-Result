from z3 import *

# Base setup: Companies and their initial buildings
companies = ["RealProp", "Southco", "Trustcorp"]
building_classes = {
    "Garza Tower": 1,
    "Yates House": 3,
    "Zimmer House": 3,
    "Flores Tower": 1,
    "Lynch Building": 2,
    "King Building": 2,
    "Meyer Building": 2,
    "Ortiz Building": 2,
}

# Initial ownership
initial_ownership = {
    "RealProp": ["Garza Tower", "Yates House", "Zimmer House"],
    "Southco": ["Flores Tower", "Lynch Building"],
    "Trustcorp": ["King Building", "Meyer Building", "Ortiz Building"],
}

# Define the options
options = {
    "A": {
        "RealProp": ["Flores Tower", "Garza Tower"],
        "Southco": ["Lynch Building", "Yates House", "Zimmer House"],
        "Trustcorp": ["King Building", "Meyer Building", "Ortiz Building"],
    },
    "B": {
        "RealProp": ["Garza Tower", "King Building", "Ortiz Building"],
        "Southco": ["Flores Tower", "Lynch Building"],
        "Trustcorp": ["Meyer Building", "Yates House", "Zimmer House"],
    },
    "C": {
        "RealProp": ["Garza Tower", "Lynch Building"],
        "Southco": ["Flores Tower", "Yates House", "Zimmer House"],
        "Trustcorp": ["King Building", "Meyer Building", "Ortiz Building"],
    },
    "D": {
        "RealProp": ["Garza Tower", "Meyer Building", "Yates House"],
        "Southco": ["Flores Tower", "Lynch Building"],
        "Trustcorp": ["King Building", "Ortiz Building", "Zimmer House"],
    },
    "E": {
        "RealProp": ["Garza Tower", "Yates House", "Zimmer House"],
        "Southco": ["Lynch Building", "Ortiz Building"],
        "Trustcorp": ["Flores Tower", "King Building", "Meyer Building"],
    },
}

# Helper function to get the class of a building
def get_class(building):
    return building_classes[str(building)]

# We will now check each option to see if it can be the result of one trade
found_options = []

# We will use a single solver and push/pop contexts for each option
solver = Solver()

for letter, option in options.items():
    solver.push()
    
    # Extract the buildings for each company in the option
    realprop_buildings = option["RealProp"]
    southco_buildings = option["Southco"]
    trustcorp_buildings = option["Trustcorp"]

    # Calculate the total number of buildings before and after the trade
    initial_total_buildings = (
        len(initial_ownership["RealProp"]) +
        len(initial_ownership["Southco"]) +
        len(initial_ownership["Trustcorp"])
    )
    final_total_buildings = (
        len(realprop_buildings) +
        len(southco_buildings) +
        len(trustcorp_buildings)
    )

    # The total number of buildings must be the same or differ by the trade type
    # Trade 1: same number of buildings
    # Trade 2: +1 building (give 1, receive 2)
    # Trade 3: +1 building (give 1, receive 2)
    # So the final total must be initial_total_buildings + 1
    solver.add(final_total_buildings == initial_total_buildings + 1)

    # Define symbolic variables for the trade
    given_building = String("given_building")
    received_building1 = String("received_building1")
    received_building2 = String("received_building2")
    trade_type = Int("trade_type")

    # The given building must be in the initial ownership of one of the companies
    solver.add(Or(
        Or([given_building == b for b in initial_ownership["RealProp"]]),
        Or([given_building == b for b in initial_ownership["Southco"]]),
        Or([given_building == b for b in initial_ownership["Trustcorp"]]),
    ))

    # The given building must not be in the final ownership
    solver.add(Not(Or(
        Or([given_building == b for b in realprop_buildings]),
        Or([given_building == b for b in southco_buildings]),
        Or([given_building == b for b in trustcorp_buildings]),
    )))

    # The received buildings must be in the final ownership
    solver.add(Or(
        received_building1 == realprop_buildings[0],
        received_building1 == realprop_buildings[1],
        received_building1 == realprop_buildings[2] if len(realprop_buildings) > 2 else False,
        received_building1 == southco_buildings[0],
        received_building1 == southco_buildings[1],
        received_building1 == trustcorp_buildings[0],
        received_building1 == trustcorp_buildings[1],
        received_building1 == trustcorp_buildings[2],
    ))
    solver.add(Or(
        received_building2 == realprop_buildings[0],
        received_building2 == realprop_buildings[1],
        received_building2 == realprop_buildings[2] if len(realprop_buildings) > 2 else False,
        received_building2 == southco_buildings[0],
        received_building2 == southco_buildings[1],
        received_building2 == trustcorp_buildings[0],
        received_building2 == trustcorp_buildings[1],
        received_building2 == trustcorp_buildings[2],
    ))

    # The trade type must be valid
    solver.add(Or(trade_type == 1, trade_type == 2, trade_type == 3))

    # Encode the trade type constraints
    # Trade 1: one building for one building of the same class
    solver.add(Implies(
        trade_type == 1,
        And(
            received_building2 == received_building1,  # Only one building received
            get_class(given_building) == get_class(received_building1),
        )
    ))

    # Trade 2: one class 1 building for two class 2 buildings
    solver.add(Implies(
        trade_type == 2,
        And(
            get_class(given_building) == 1,
            get_class(received_building1) == 2,
            get_class(received_building2) == 2,
        )
    ))

    # Trade 3: one class 2 building for two class 3 buildings
    solver.add(Implies(
        trade_type == 3,
        And(
            get_class(given_building) == 2,
            get_class(received_building1) == 3,
            get_class(received_building2) == 3,
        )
    ))

    # Check if the option is valid
    if solver.check() == sat:
        found_options.append(letter)
    
    solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")