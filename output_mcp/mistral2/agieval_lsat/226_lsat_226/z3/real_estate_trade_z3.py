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

# Possible trades
# Trade 1: Trade one building for one other building of the same class
# Trade 2: Trade one class 1 building for two class 2 buildings
# Trade 3: Trade one class 2 building for two class 3 buildings

# We need to model the possible trades and their outcomes
# For simplicity, we will model the possible outcomes after one trade

# Define the possible trades as constraints
# We will check each option (A-E) to see if it can be the result of one trade

# Helper function to get the class of a building
def get_class(building):
    return building_classes[building]

# Helper function to check if a trade is valid
# trade_type: 1 (same class), 2 (class 1 for two class 2), 3 (class 2 for two class 3)
# giver: company giving the building
# receiver: company receiving the building(s)
# given_building: building given away
# received_buildings: list of buildings received (1 or 2 depending on trade type)

def is_valid_trade(trade_type, giver, receiver, given_building, received_buildings):
    given_class = get_class(given_building)
    if trade_type == 1:
        # Trade one building for one other building of the same class
        if len(received_buildings) != 1:
            return False
        received_class = get_class(received_buildings[0])
        return given_class == received_class
    elif trade_type == 2:
        # Trade one class 1 building for two class 2 buildings
        if given_class != 1 or len(received_buildings) != 2:
            return False
        return all(get_class(b) == 2 for b in received_buildings)
    elif trade_type == 3:
        # Trade one class 2 building for two class 3 buildings
        if given_class != 2 or len(received_buildings) != 2:
            return False
        return all(get_class(b) == 3 for b in received_buildings)
    else:
        return False

# Now, we will model the problem as a constraint satisfaction problem
# We will check each option (A-E) to see if it can be the result of one trade

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

# We will now check each option to see if it can be the result of one trade
# We need to model the trade as a constraint

# We will use a solver to check each option
solver = Solver()

# We will model the trade as a constraint
# We need to ensure that the option is the result of exactly one trade

# We will iterate over each option and check if it can be the result of one trade
found_options = []

for letter, option in options.items():
    # Reset solver for each option
    solver.push()
    solver.reset()
    solver = Solver()

    # Add constraints to model the trade
    # We need to ensure that the option is the result of exactly one trade
    # We will model the trade as a constraint

    # Define the buildings in the option
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

    # We need to model the trade as a constraint
    # We will use a symbolic variable to represent the trade type
    trade_type = Int("trade_type")
    solver.add(Or(trade_type == 1, trade_type == 2, trade_type == 3))

    # We will model the trade as a constraint
    # We need to ensure that the trade is valid
    # We will use a symbolic variable to represent the building given away
    given_building = String("given_building")
    received_buildings = [String(f"received_{i}") for i in range(2)]

    # The given building must be in the initial ownership of one of the companies
    solver.add(Or(
        And(Or([given_building == b for b in initial_ownership["RealProp"]]),
            trade_type == 1),
        And(Or([given_building == b for b in initial_ownership["RealProp"]]),
            trade_type == 2),
        And(Or([given_building == b for b in initial_ownership["RealProp"]]),
            trade_type == 3),
        And(Or([given_building == b for b in initial_ownership["Southco"]]),
            trade_type == 1),
        And(Or([given_building == b for b in initial_ownership["Southco"]]),
            trade_type == 2),
        And(Or([given_building == b for b in initial_ownership["Southco"]]),
            trade_type == 3),
        And(Or([given_building == b for b in initial_ownership["Trustcorp"]]),
            trade_type == 1),
        And(Or([given_building == b for b in initial_ownership["Trustcorp"]]),
            trade_type == 2),
        And(Or([given_building == b for b in initial_ownership["Trustcorp"]]),
            trade_type == 3),
    ))

    # The received buildings must be in the final ownership of the companies
    # We need to ensure that the received buildings are not in the initial ownership
    # and are in the final ownership

    # We will model the received buildings as constraints
    for i in range(2):
        solver.add(Or(
            received_buildings[i] == "Garza Tower",
            received_buildings[i] == "Yates House",
            received_buildings[i] == "Zimmer House",
            received_buildings[i] == "Flores Tower",
            received_buildings[i] == "Lynch Building",
            received_buildings[i] == "King Building",
            received_buildings[i] == "Meyer Building",
            received_buildings[i] == "Ortiz Building",
        ))

    # The given building must not be in the final ownership
    solver.add(Not(Or([given_building == b for b in realprop_buildings + southco_buildings + trustcorp_buildings])))

    # The received buildings must be in the final ownership
    for received in received_buildings:
        solver.add(Or(
            Or([received == b for b in realprop_buildings]),
            Or([received == b for b in southco_buildings]),
            Or([received == b for b in trustcorp_buildings]),
        ))

    # The trade must be valid
    # We will model the trade as a constraint
    # We need to ensure that the trade is valid based on the trade type
    # We will use a symbolic variable to represent the giver and receiver
    giver = String("giver")
    receiver = String("receiver")

    # The giver must be the company that initially owns the given building
    solver.add(Or(
        And(giver == "RealProp", Or([given_building == b for b in initial_ownership["RealProp"]])),
        And(giver == "Southco", Or([given_building == b for b in initial_ownership["Southco"]])),
        And(giver == "Trustcorp", Or([given_building == b for b in initial_ownership["Trustcorp"]])),
    ))

    # The receiver must be a company that does not own the given building initially
    solver.add(Or(
        And(giver == "RealProp", receiver == "Southco"),
        And(giver == "RealProp", receiver == "Trustcorp"),
        And(giver == "Southco", receiver == "RealProp"),
        And(giver == "Southco", receiver == "Trustcorp"),
        And(giver == "Trustcorp", receiver == "RealProp"),
        And(giver == "Trustcorp", receiver == "Southco"),
    ))

    # The trade must be valid based on the trade type
    # We will model the trade as a constraint
    # We need to ensure that the trade is valid based on the trade type
    # We will use a symbolic variable to represent the trade type
    # We will model the trade as a constraint
    if trade_type == 1:
        # Trade one building for one other building of the same class
        solver.add(And(
            received_buildings[0] != received_buildings[1],  # Ensure two distinct buildings for trade type 2 and 3
            get_class(given_building) == get_class(received_buildings[0]),
        ))
    elif trade_type == 2:
        # Trade one class 1 building for two class 2 buildings
        solver.add(And(
            get_class(given_building) == 1,
            get_class(received_buildings[0]) == 2,
            get_class(received_buildings[1]) == 2,
        ))
    elif trade_type == 3:
        # Trade one class 2 building for two class 3 buildings
        solver.add(And(
            get_class(given_building) == 2,
            get_class(received_buildings[0]) == 3,
            get_class(received_buildings[1]) == 3,
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