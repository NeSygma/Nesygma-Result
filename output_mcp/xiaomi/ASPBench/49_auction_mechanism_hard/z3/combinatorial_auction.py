from z3 import *

# Create optimizer
opt = Optimize()

# Define bidders
bidders = ['a', 'b', 'c', 'd']
bidder_budget = {'a': 150, 'b': 200, 'c': 180, 'd': 100}
bidder_synergy = {'a': 20, 'b': 10, 'c': 25, 'd': 5}

# Define items and categories
items = ['item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'lic_E', 'lic_F']
electronics_items = ['item1', 'item2', 'item5', 'lic_E']
furniture_items = ['item3', 'item4', 'item6', 'lic_F']

# Define bids
bids = [
    {'id': 1, 'bidder': 'a', 'items': ['item1', 'item2'], 'price': 70},
    {'id': 2, 'bidder': 'a', 'items': ['lic_E'], 'price': 40},
    {'id': 3, 'bidder': 'b', 'items': ['item3', 'item4'], 'price': 90},
    {'id': 4, 'bidder': 'b', 'items': ['lic_F'], 'price': 50},
    {'id': 5, 'bidder': 'b', 'items': ['item5'], 'price': 60},
    {'id': 6, 'bidder': 'c', 'items': ['item1', 'item5'], 'price': 100},
    {'id': 7, 'bidder': 'c', 'items': ['lic_E'], 'price': 60},
    {'id': 8, 'bidder': 'c', 'items': ['item3', 'item6'], 'price': 80},
    {'id': 9, 'bidder': 'd', 'items': ['lic_F'], 'price': 25},
    {'id': 10, 'bidder': 'd', 'items': ['item4'], 'price': 70},
]

# Decision variables: whether each bid is won
bid_won = {bid['id']: Bool(f"bid_{bid['id']}_won") for bid in bids}

# Constraint 1: Item Exclusivity - each item in at most one winning bid
for item in items:
    bids_containing_item = [bid for bid in bids if item in bid['items']]
    if len(bids_containing_item) > 1:
        # At most one of these bids can be won
        opt.add(AtMost(*[bid_won[bid['id']] for bid in bids_containing_item], 1))

# Constraint 2: Budget Compliance
for bidder in bidders:
    bidder_bids = [bid for bid in bids if bid['bidder'] == bidder]
    total_cost = Sum([If(bid_won[bid['id']], bid['price'], 0) for bid in bidder_bids])
    opt.add(total_cost <= bidder_budget[bidder])

# Constraint 3: Synergy Bonus - tracked separately in revenue calculation

# Constraint 4: Licensing Requirement
# For electronics: if a bidder wins any electronics item (not lic_E), they must also win lic_E
for bidder in bidders:
    # Get all bids by this bidder that contain electronics items (excluding lic_E itself)
    electronics_bids = [bid for bid in bids if bid['bidder'] == bidder and any(item in electronics_items and item != 'lic_E' for item in bid['items'])]
    lic_E_bids = [bid for bid in bids if bid['bidder'] == bidder and 'lic_E' in bid['items']]
    
    if electronics_bids and lic_E_bids:
        # If any electronics bid is won, then lic_E must also be won
        won_electronics = Or([bid_won[bid['id']] for bid in electronics_bids])
        won_lic_E = Or([bid_won[bid['id']] for bid in lic_E_bids])
        opt.add(Implies(won_electronics, won_lic_E))

# For furniture: if a bidder wins any furniture item (not lic_F), they must also win lic_F
for bidder in bidders:
    furniture_bids = [bid for bid in bids if bid['bidder'] == bidder and any(item in furniture_items and item != 'lic_F' for item in bid['items'])]
    lic_F_bids = [bid for bid in bids if bid['bidder'] == bidder and 'lic_F' in bid['items']]
    
    if furniture_bids and lic_F_bids:
        won_furniture = Or([bid_won[bid['id']] for bid in furniture_bids])
        won_lic_F = Or([bid_won[bid['id']] for bid in lic_F_bids])
        opt.add(Implies(won_furniture, won_lic_F))

# Constraint 5: Fairness - max 3 items per bidder
for bidder in bidders:
    bidder_bids = [bid for bid in bids if bid['bidder'] == bidder]
    total_items = Sum([If(bid_won[bid['id']], len(bid['items']), 0) for bid in bidder_bids])
    opt.add(total_items <= 3)

# Synergy bonus tracking
# A bidder gets synergy bonus if they win 2 or more bids
bidder_won_count = {}
for bidder in bidders:
    bidder_bids = [bid for bid in bids if bid['bidder'] == bidder]
    count = Sum([If(bid_won[bid['id']], 1, 0) for bid in bidder_bids])
    bidder_won_count[bidder] = count

# Revenue calculation: sum of winning bid prices + synergy bonuses
base_revenue = Sum([If(bid_won[bid['id']], bid['price'], 0) for bid in bids])
synergy_revenue = Sum([If(bidder_won_count[bidder] >= 2, bidder_synergy[bidder], 0) for bidder in bidders])
total_revenue = base_revenue + synergy_revenue

# Maximize total revenue
opt.maximize(total_revenue)

# Check and print results
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Determine winning bids
    winning_bids = []
    for bid in bids:
        if is_true(model[bid_won[bid['id']]]):
            winning_bids.append(bid['id'])
    winning_bids.sort()
    print(f"winning_bids: {winning_bids}")
    
    # Calculate total revenue
    base_sum = sum(bid['price'] for bid in bids if bid['id'] in winning_bids)
    synergy_sum = 0
    synergy_bonuses = []
    for bidder in bidders:
        bidder_bids = [bid for bid in bids if bid['bidder'] == bidder]
        won_count = sum(1 for bid in bidder_bids if bid['id'] in winning_bids)
        if won_count >= 2:
            synergy_sum += bidder_synergy[bidder]
            synergy_bonuses.append({'bidder': bidder, 'bonus': bidder_synergy[bidder]})
    
    total_rev = base_sum + synergy_sum
    print(f"total_revenue: {total_rev}")
    print(f"synergy_bonuses: {synergy_bonuses}")
    
    # Item allocation
    item_allocation = {}
    for bid in bids:
        if bid['id'] in winning_bids:
            for item in bid['items']:
                item_allocation[item] = bid['bidder']
    print(f"item_allocation: {item_allocation}")
    
    # Print bid details
    print("\nWinning bid details:")
    for bid in bids:
        if bid['id'] in winning_bids:
            print(f"  Bid {bid['id']}: bidder={bid['bidder']}, items={bid['items']}, price={bid['price']}")
    
    # Print bidder totals
    print("\nBidder totals:")
    for bidder in bidders:
        bidder_bids = [bid for bid in bids if bid['bidder'] == bidder]
        won_bids = [bid for bid in bidder_bids if bid['id'] in winning_bids]
        total_cost = sum(bid['price'] for bid in won_bids)
        total_items = sum(len(bid['items']) for bid in won_bids)
        won_count = len(won_bids)
        bonus = bidder_synergy[bidder] if won_count >= 2 else 0
        print(f"  Bidder {bidder}: won {won_count} bids, cost={total_cost}, items={total_items}, bonus={bonus}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")