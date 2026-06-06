from z3 import *

# ============================================================================
# Problem Data
# ============================================================================

# Bidders: (name, budget, synergy_bonus)
bidders_data = [
    ("a", 150, 20),
    ("b", 200, 10),
    ("c", 180, 25),
    ("d", 100, 5)
]

# Items: (name, category)
items_data = [
    ("item1", "electronics"),
    ("item2", "electronics"),
    ("item3", "furniture"),
    ("item4", "furniture"),
    ("item5", "electronics"),
    ("item6", "furniture"),
    ("lic_E", "license"),
    ("lic_F", "license")
]

# Bids: (bid_id, bidder, items, price)
bids_data = [
    (1, "a", ["item1", "item2"], 70),
    (2, "a", ["lic_E"], 40),
    (3, "b", ["item3", "item4"], 90),
    (4, "b", ["lic_F"], 50),
    (5, "b", ["item5"], 60),
    (6, "c", ["item1", "item5"], 100),
    (7, "c", ["lic_E"], 60),
    (8, "c", ["item3", "item6"], 80),
    (9, "d", ["lic_F"], 25),
    (10, "d", ["item4"], 70)
]

# ============================================================================
# Z3 Model
# ============================================================================

solver = Optimize()

# Decision variables
is_winning = {bid_id: Bool(f"is_winning_{bid_id}") for bid_id, _, _, _ in bids_data}

# Map from item to the bid that wins it (None if unallocated)
item_alloc = {item: Int(f"item_alloc_{item}") for item, _ in items_data}

# Track total items and winning bids per bidder
bidder_item_count = {bidder: Int(f"bidder_item_count_{bidder}") for bidder, _, _ in bidders_data}
bidder_win_count = {bidder: Int(f"bidder_win_count_{bidder}") for bidder, _, _ in bidders_data}

# Total revenue
TotalRevenue = Int("TotalRevenue")

# ============================================================================
# Helper Functions
# ============================================================================

def get_bidder_from_bid(bid_id):
    for bid in bids_data:
        if bid[0] == bid_id:
            return bid[1]
    return None

def get_items_from_bid(bid_id):
    for bid in bids_data:
        if bid[0] == bid_id:
            return bid[2]
    return []

def get_price_from_bid(bid_id):
    for bid in bids_data:
        if bid[0] == bid_id:
            return bid[3]
    return 0

def get_budget(bidder):
    for b in bidders_data:
        if b[0] == bidder:
            return b[1]
    return 0

def get_synergy_bonus(bidder):
    for b in bidders_data:
        if b[0] == bidder:
            return b[2]
    return 0

# ============================================================================
# Constraints
# ============================================================================

# 1. Item Exclusivity: Each item can be allocated to at most one winning bid
for item, _ in items_data:
    # item_alloc[item] = bid_id if item is allocated to that bid, else -1
    solver.add(Or(item_alloc[item] == -1, And([item_alloc[item] == bid_id for bid_id in is_winning.keys()])))
    # If a bid wins an item, that bid must be marked as winning
    for bid_id in is_winning.keys():
        items_in_bid = get_items_from_bid(bid_id)
        if item in items_in_bid:
            solver.add(Implies(item_alloc[item] == bid_id, is_winning[bid_id]))
    # Only one bid can allocate this item
    solver.add(Sum([If(item_alloc[item] == bid_id, 1, 0) for bid_id in is_winning.keys()]) <= 1)

# 2. Budget Compliance: Total price of winning bids for a bidder <= budget
for bidder, _, _ in bidders_data:
    total_cost = Sum([If(is_winning[bid_id], get_price_from_bid(bid_id), 0) for bid_id in is_winning.keys() if get_bidder_from_bid(bid_id) == bidder])
    solver.add(total_cost <= get_budget(bidder))

# 3. Synergy Bonus: If a bidder wins >=2 bids, add synergy bonus to revenue
synergy_bonuses = []
for bidder, _, _ in bidders_data:
    win_count = bidder_win_count[bidder]
    synergy = get_synergy_bonus(bidder)
    # Count winning bids for this bidder
    solver.add(win_count == Sum([If(And(is_winning[bid_id], get_bidder_from_bid(bid_id) == bidder), 1, 0) for bid_id in is_winning.keys()]))
    # Add synergy bonus if win_count >= 2
    synergy_bonuses.append(If(win_count >= 2, synergy, 0))

# 4. Licensing Requirement: To win bids with items from a category, must win the license bid
# Electronics category: item1, item2, item5, lic_E
# Furniture category: item3, item4, item6, lic_F

# For electronics: if any winning bid contains item1, item2, or item5, then lic_E must be won
solver.add(Implies(
    Or([And(is_winning[bid_id], any(item in ["item1", "item2", "item5"] for item in get_items_from_bid(bid_id))) for bid_id in is_winning.keys()]),
    is_winning[2]  # lic_E bid
))

# For furniture: if any winning bid contains item3, item4, or item6, then lic_F must be won
solver.add(Implies(
    Or([And(is_winning[bid_id], any(item in ["item3", "item4", "item6"] for item in get_items_from_bid(bid_id))) for bid_id in is_winning.keys()]),
    is_winning[4]  # lic_F bid
))

# 5. Fairness Constraint: No bidder can be allocated more than 3 items total
for bidder, _, _ in bidders_data:
    # Count total items allocated to this bidder across all winning bids
    items_won_by_bidder = []
    for item, _ in items_data:
        for bid_id in is_winning.keys():
            if get_bidder_from_bid(bid_id) == bidder:
                items_in_bid = get_items_from_bid(bid_id)
                if item in items_in_bid:
                    items_won_by_bidder.append(If(And(is_winning[bid_id], item_alloc[item] == bid_id), 1, 0))
    solver.add(Sum(items_won_by_bidder) <= 3)

# ============================================================================
# Objective: Maximize total revenue = sum of winning bid prices + synergy bonuses
# ============================================================================

# Sum of winning bid prices
sum_prices = Sum([If(is_winning[bid_id], get_price_from_bid(bid_id), 0) for bid_id in is_winning.keys()])

# Total revenue = sum_prices + sum of synergy bonuses
solver.add(TotalRevenue == sum_prices + Sum(synergy_bonuses))

solver.maximize(TotalRevenue)

# ============================================================================
# Solve and Output
# ============================================================================

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Total revenue:", model[TotalRevenue])
    
    # Extract winning bids
    winning_bids = [bid_id for bid_id in is_winning.keys() if is_true(model[is_winning[bid_id]])]
    winning_bids.sort()
    print("Winning bids:", winning_bids)
    
    # Extract item allocation
    item_allocation = {}
    for item, _ in items_data:
        allocated_bid = model[item_alloc[item]]
        if allocated_bid is not None and str(allocated_bid) != "-1":
            item_allocation[item] = str(allocated_bid)
    print("Item allocation:", item_allocation)
    
    # Extract synergy bonuses
    synergy_bonuses_list = []
    for bidder, _, _ in bidders_data:
        win_count = model[bidder_win_count[bidder]]
        if win_count is not None and win_count.as_long() >= 2:
            bonus = get_synergy_bonus(bidder)
            synergy_bonuses_list.append((bidder, bonus))
    print("Synergy bonuses:", synergy_bonuses_list)
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")