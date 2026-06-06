from z3 import *

# Define buildings and their classes
buildings = ["Garza", "Yates", "Zimmer", "Flores", "Lynch", "King", "Meyer", "Ortiz"]

# Class mapping: 0=class1, 1=class2, 2=class3
bld_class = {
    "Garza": 0,   # class 1
    "Yates": 2,   # class 3
    "Zimmer": 2,  # class 3
    "Flores": 0,  # class 1
    "Lynch": 1,   # class 2
    "King": 1,    # class 2
    "Meyer": 1,   # class 2
    "Ortiz": 1    # class 2
}

companies = ["RealProp", "Southco", "Trustcorp"]

# Initial ownership: each building owned by which company
init_owner = {
    "Garza": "RealProp",
    "Yates": "RealProp",
    "Zimmer": "RealProp",
    "Flores": "Southco",
    "Lynch": "Southco",
    "King": "Trustcorp",
    "Meyer": "Trustcorp",
    "Ortiz": "Trustcorp"
}

# Each option defines a final ownership
options = {
    "A": {
        "RealProp": ["Flores", "Garza"],
        "Southco": ["Lynch", "Yates", "Zimmer"],
        "Trustcorp": ["King", "Meyer", "Ortiz"]
    },
    "B": {
        "RealProp": ["Garza", "King", "Ortiz"],
        "Southco": ["Flores", "Lynch"],
        "Trustcorp": ["Meyer", "Yates", "Zimmer"]
    },
    "C": {
        "RealProp": ["Garza", "Lynch"],
        "Southco": ["Flores", "Yates", "Zimmer"],
        "Trustcorp": ["King", "Meyer", "Ortiz"]
    },
    "D": {
        "RealProp": ["Garza", "Meyer", "Yates"],
        "Southco": ["Flores", "Lynch"],
        "Trustcorp": ["King", "Ortiz", "Zimmer"]
    },
    "E": {
        "RealProp": ["Garza", "Yates", "Zimmer"],
        "Southco": ["Lynch", "Ortiz"],
        "Trustcorp": ["Flores", "King", "Meyer"]
    }
}

def check_option(letter, final_owner_dict):
    solver = Solver()
    
    # For each building, we have a variable representing its owner after the trade
    owner_vars = {}
    for b in buildings:
        owner_vars[b] = Int(f"owner_{b}")
        # Domain: 0=RealProp, 1=Southco, 2=Trustcorp
        solver.add(owner_vars[b] >= 0, owner_vars[b] <= 2)
    
    # Map company name to index
    comp_idx = {"RealProp": 0, "Southco": 1, "Trustcorp": 2}
    
    # Constraint: final ownership matches the option
    for comp, bld_list in final_owner_dict.items():
        for b in bld_list:
            solver.add(owner_vars[b] == comp_idx[comp])
    
    # Constraint: only one trade is made
    # We model which buildings change owner
    # A trade involves two parties exchanging buildings according to one of three rules
    
    # Let's model the trade explicitly:
    # party_a and party_b are the two trading companies (0, 1, or 2)
    party_a = Int('party_a')
    party_b = Int('party_b')
    solver.add(party_a >= 0, party_a <= 2)
    solver.add(party_b >= 0, party_b <= 2)
    solver.add(party_a != party_b)
    
    # trade_type: 0 = type 1 (one-for-one same class), 1 = type 2 (1 class1 for 2 class2), 2 = type 3 (1 class2 for 2 class3)
    trade_type = Int('trade_type')
    solver.add(trade_type >= 0, trade_type <= 2)
    
    # For each building, determine if it's given by its original owner to the other party
    # The original owner is init_owner[b]
    # After trade, the building is owned by whoever it's given to
    
    # For each building, track:
    # - Its original owner
    # - Whether it changes hands in the trade
    
    # The key insight: a trade involves each party giving some of their buildings to the other.
    # Buildings not involved in the trade stay with their original owner.
    
    # Let's think about it differently.
    # A trade of type k means:
    # Party A gives some buildings to Party B, and Party B gives some buildings to Party A.
    # The buildings given by A were originally owned by A (before trade).
    # Type 1: A gives 1 bld, B gives 1 bld of same class.
    # Type 2: A gives 1 class-1 bld, B gives 2 class-2 blds.
    # Type 3: A gives 1 class-2 bld, B gives 2 class-3 blds.
    
    # Let me encode this using symbolic variables for which buildings are traded.
    
    # For each building, a boolean: is it involved in the trade?
    # For each building, a variable: who receives it in the trade?
    
    involved = {b: Bool(f"involved_{b}") for b in buildings}
    receiver = {b: Int(f"receiver_{b}") for b in buildings}
    
    for b in buildings:
        solver.add(receiver[b] >= 0, receiver[b] <= 2)
        
        # If building is not involved in trade, its owner doesn't change
        # The owner after trade = original owner
        solver.add(Implies(Not(involved[b]), owner_vars[b] == comp_idx[init_owner[b]]))
        
        # If building is involved, the receiver is one of the two trading parties (the one that's not the original owner)
        solver.add(Implies(involved[b], 
            Or(
                And(receiver[b] == party_a, comp_idx[init_owner[b]] != party_a),
                And(receiver[b] == party_b, comp_idx[init_owner[b]] != party_b)
            )
        ))
        
        # If involved, the new owner is the receiver
        solver.add(Implies(involved[b], owner_vars[b] == receiver[b]))
    
    # Now constrain based on trade type
    # Type 0: one-for-one same class
    # One building goes from A to B, one goes from B to A, same class
    
    # Type 1: one class 1 from A to B, two class 2 from B to A
    
    # Type 2: one class 2 from A to B, two class 3 from B to A
    
    # Buildings given by A (originally owned by A) that go to B
    given_by_A_to_B = [And(
        involved[b],
        comp_idx[init_owner[b]] == party_a,
        receiver[b] == party_b
    ) for b in buildings]
    
    # Buildings given by B (originally owned by B) that go to A
    given_by_B_to_A = [And(
        involved[b],
        comp_idx[init_owner[b]] == party_b,
        receiver[b] == party_a
    ) for b in buildings]
    
    # Count buildings given by A to B, by class
    count_A_to_B_class1 = Sum([If(given_by_A_to_B[i], 1, 0) for i, b in enumerate(buildings) if bld_class[b] == 0])
    count_A_to_B_class2 = Sum([If(given_by_A_to_B[i], 1, 0) for i, b in enumerate(buildings) if bld_class[b] == 1])
    count_A_to_B_class3 = Sum([If(given_by_A_to_B[i], 1, 0) for i, b in enumerate(buildings) if bld_class[b] == 2])
    
    count_B_to_A_class1 = Sum([If(given_by_B_to_A[i], 1, 0) for i, b in enumerate(buildings) if bld_class[b] == 0])
    count_B_to_A_class2 = Sum([If(given_by_B_to_A[i], 1, 0) for i, b in enumerate(buildings) if bld_class[b] == 1])
    count_B_to_A_class3 = Sum([If(given_by_B_to_A[i], 1, 0) for i, b in enumerate(buildings) if bld_class[b] == 2])
    
    # Constraint based on trade type
    # Type 0: A gives 1 to B, B gives 1 to A, same class
    solver.add(Implies(trade_type == 0,
        And(
            Sum([If(given_by_A_to_B[i], 1, 0) for i in range(len(buildings))]) == 1,
            Sum([If(given_by_B_to_A[i], 1, 0) for i in range(len(buildings))]) == 1,
            Or(
                And(count_A_to_B_class1 == 1, count_B_to_A_class1 == 1),
                And(count_A_to_B_class2 == 1, count_B_to_A_class2 == 1),
                And(count_A_to_B_class3 == 1, count_B_to_A_class3 == 1)
            )
        )
    ))
    
    # Type 1: A gives 1 class-1 to B, B gives 2 class-2 to A
    solver.add(Implies(trade_type == 1,
        And(
            count_A_to_B_class1 == 1,
            count_A_to_B_class2 == 0,
            count_A_to_B_class3 == 0,
            count_B_to_A_class2 == 2,
            count_B_to_A_class1 == 0,
            count_B_to_A_class3 == 0,
            Sum([If(given_by_A_to_B[i], 1, 0) for i in range(len(buildings))]) == 1,
            Sum([If(given_by_B_to_A[i], 1, 0) for i in range(len(buildings))]) == 2
        )
    ))
    
    # Type 2: A gives 1 class-2 to B, B gives 2 class-3 to A
    solver.add(Implies(trade_type == 2,
        And(
            count_A_to_B_class2 == 1,
            count_A_to_B_class1 == 0,
            count_A_to_B_class3 == 0,
            count_B_to_A_class3 == 2,
            count_B_to_A_class1 == 0,
            count_B_to_A_class2 == 0,
            Sum([If(given_by_A_to_B[i], 1, 0) for i in range(len(buildings))]) == 1,
            Sum([If(given_by_B_to_A[i], 1, 0) for i in range(len(buildings))]) == 2
        )
    ))
    
    result = solver.check()
    return result

found_options = []
for letter in ["A", "B", "C", "D", "E"]:
    result = check_option(letter, options[letter])
    if result == sat:
        found_options.append(letter)
        print(f"Option {letter}: SAT (valid)")
    else:
        print(f"Option {letter}: UNSAT (invalid)")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")