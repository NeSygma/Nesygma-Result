from z3 import *

# Define bidders with budgets and synergy bonuses
bidders = {
    'a': {'budget': 150, 'synergy_bonus': 20},
    'b': {'budget': 200, 'synergy_bonus': 10},
    'c': {'budget': 180, 'synergy_bonus': 25},
    'd': {'budget': 100, 'synergy_bonus': 5}
}

# Define items with categories
items = {
    'item1': 'electronics',
    'item2': 'electronics',
    'item3': 'furniture',
    'item4': 'furniture',
    'item5': 'electronics',
    'item6': 'furniture',
    'lic_E': 'license_electronics',
    'lic_F': 'license_furniture'
}

# Define bids: (id, bidder, items_list, price)
bids = [
    (1, 'a', ['item1', 'item2'], 70),
    (2, 'a', ['lic_E'], 40),
    (3, 'b', ['item3', 'item4'], 90),
    (4, 'b', ['lic_F'], 50),
    (5, 'b', ['item5'], 60),
    (6, 'c', ['item1', 'item5'], 100),
    (7, 'c', ['lic_E'], 60),
    (8, 'c', ['item3', 'item6'], 80),
    (9, 'd', ['lic_F'], 25),
    (10, 'd', ['item4'], 70)
]

# Create solver
solver = Optimize()

# Define win variables for each bid
win = [Bool(f'win_{i}') for i in range(len(bids))]

# Map items to bids that contain them
item_to_bids = {}
for item in items:
    item_to_bids[item] = []
for i, (bid_id, bidder, items_list, price) in enumerate(bids):
    for item in items_list:
        if item in item_to_bids:
            item_to_bids[item].append(i)

# 1. Item Exclusivity: Each item can appear in at most one winning bid
for item, bid_indices in item_to_bids.items():
    if bid_indices:
        solver.add(Sum([If(win[i], 1, 0) for i in bid_indices]) <= 1)

# 2. Budget Compliance: Total price of winning bids per bidder <= budget
for bidder, budget in [(b, bidders[b]['budget']) for b in bidders]:
    bidder_bids = [i for i, (bid_id, b, items_list, price) in enumerate(bids) if b == bidder]
    total_price = Sum([If(win[i], bids[i][3], 0) for i in bidder_bids])
    solver.add(total_price <= budget)

# 3. Licensing Requirement: For electronics and furniture categories
# Electronics: if a bidder wins any bid with electronics items (excluding license), they must win a lic_E bid
# Furniture: if a bidder wins any bid with furniture items (excluding license), they must win a lic_F bid

# First, identify electronics bids (excluding license) and furniture bids (excluding license)
electronics_bids = []  # bids with electronics items (not license)
furniture_bids = []    # bids with furniture items (not license)
license_E_bids = []    # bids with lic_E
license_F_bids = []    # bids with lic_F

for i, (bid_id, bidder, items_list, price) in enumerate(bids):
    has_electronics = any(items[item] == 'electronics' for item in items_list if item != 'lic_E' and item != 'lic_F')
    has_furniture = any(items[item] == 'furniture' for item in items_list if item != 'lic_E' and item != 'lic_F')
    has_lic_E = 'lic_E' in items_list
    has_lic_F = 'lic_F' in items_list
    
    if has_electronics and not has_lic_E and not has_lic_F:
        electronics_bids.append(i)
    if has_furniture and not has_lic_E and not has_lic_F:
        furniture_bids.append(i)
    if has_lic_E:
        license_E_bids.append(i)
    if has_lic_F:
        license_F_bids.append(i)

# For each bidder, enforce licensing requirements
for bidder in bidders:
    # Get bids for this bidder
    bidder_electronics = [i for i in electronics_bids if bids[i][1] == bidder]
    bidder_furniture = [i for i in furniture_bids if bids[i][1] == bidder]
    bidder_license_E = [i for i in license_E_bids if bids[i][1] == bidder]
    bidder_license_F = [i for i in license_F_bids if bids[i][1] == bidder]
    
    # If bidder wins any electronics bid, they must win at least one lic_E bid
    if bidder_electronics and bidder_license_E:
        # At least one electronics bid won => at least one lic_E bid won
        electronics_won = Or([win[i] for i in bidder_electronics])
        license_E_won = Or([win[i] for i in bidder_license_E])
        solver.add(Implies(electronics_won, license_E_won))
    elif bidder_electronics and not bidder_license_E:
        # Bidder has electronics bids but no lic_E bid - cannot win any electronics bid
        for i in bidder_electronics:
            solver.add(Not(win[i]))
    
    # If bidder wins any furniture bid, they must win at least one lic_F bid
    if bidder_furniture and bidder_license_F:
        furniture_won = Or([win[i] for i in bidder_furniture])
        license_F_won = Or([win[i] for i in bidder_license_F])
        solver.add(Implies(furniture_won, license_F_won))
    elif bidder_furniture and not bidder_license_F:
        # Bidder has furniture bids but no lic_F bid - cannot win any furniture bid
        for i in bidder_furniture:
            solver.add(Not(win[i]))

# 4. Fairness Constraint: No bidder can have more than 3 items total
for bidder in bidders:
    bidder_bids = [i for i, (bid_id, b, items_list, price) in enumerate(bids) if b == bidder]
    total_items = Sum([If(win[i], len(bids[i][2]), 0) for i in bidder_bids])
    solver.add(total_items <= 3)

# 5. Objective: Maximize total revenue (bid prices + synergy bonuses)
# First, calculate total bid prices
total_bid_prices = Sum([If(win[i], bids[i][3], 0) for i in range(len(bids))])

# Calculate synergy bonuses: for each bidder with at least 2 winning bids
synergy_bonuses = []
for bidder in bidders:
    bidder_bids = [i for i, (bid_id, b, items_list, price) in enumerate(bids) if b == bidder]
    # Count winning bids for this bidder
    winning_count = Sum([If(win[i], 1, 0) for i in bidder_bids])
    # Get synergy bonus
    bonus = bidders[bidder]['synergy_bonus']
    # Add bonus if at least 2 winning bids
    synergy_bonuses.append(If(winning_count >= 2, bonus, 0))

total_synergy = Sum(synergy_bonuses)
total_revenue = total_bid_prices + total_synergy

# Maximize total revenue
solver.maximize(total_revenue)

# Check and get model
result = solver.check()
if result == sat:
    model = solver.model()
    
    # Get winning bids
    winning_bids = []
    for i, (bid_id, bidder, items_list, price) in enumerate(bids):
        if is_true(model[win[i]]):
            winning_bids.append(bid_id)
    winning_bids.sort()
    
    # Calculate total revenue from model
    revenue = 0
    for i, (bid_id, bidder, items_list, price) in enumerate(bids):
        if is_true(model[win[i]]):
            revenue += price
    
    # Add synergy bonuses
    synergy_details = []
    for bidder in bidders:
        bidder_bids = [i for i, (bid_id, b, items_list, price) in enumerate(bids) if b == bidder]
        winning_count = sum(1 for i in bidder_bids if is_true(model[win[i]]))
        if winning_count >= 2:
            revenue += bidders[bidder]['synergy_bonus']
            synergy_details.append({'bidder': bidder, 'bonus': bidders[bidder]['synergy_bonus']})
    
    # Item allocation
    item_allocation = {}
    for item in items:
        for i, (bid_id, bidder, items_list, price) in enumerate(bids):
            if item in items_list and is_true(model[win[i]]):
                item_allocation[item] = bidder
                break
    
    print("STATUS: sat")
    print(f"winning_bids: {winning_bids}")
    print(f"total_revenue: {revenue}")
    print(f"synergy_bonuses: {synergy_details}")
    print(f"item_allocation: {item_allocation}")
    
    # Verify expected revenue
    if revenue == 335:
        print("SUCCESS: Revenue matches expected maximum of 335")
    else:
        print(f"NOTE: Revenue is {revenue}, expected 335")
        
elif result == unsat:
    print("STATUS: unsat")
    print("No solution exists - constraints are unsatisfiable")
else:
    print("STATUS: unknown")
    print("Solver returned unknown result")