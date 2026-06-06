from z3 import *

# Bidders
bidders = ['a', 'b', 'c', 'd']
budgets = {'a': 150, 'b': 200, 'c': 180, 'd': 100}
synergy_bonuses = {'a': 20, 'b': 10, 'c': 25, 'd': 5}

# Items and their categories
items = ['item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'lic_E', 'lic_F']
categories = {
    'item1': 'electronics', 'item2': 'electronics', 'item5': 'electronics',
    'item3': 'furniture', 'item4': 'furniture', 'item6': 'furniture',
    'lic_E': 'electronics', 'lic_F': 'furniture'
}

# Bids
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
    {'id': 10, 'bidder': 'd', 'items': ['item4'], 'price': 70}
]

# Initialize optimizer
opt = Optimize()

# Decision variables
winning_bid = [Bool(f'winning_bid_{bid["id"]}') for bid in bids]
item_alloc = {item: Int(f'item_alloc_{item}') for item in items}
bidder_items = {bidder: Int(f'bidder_items_{bidder}') for bidder in bidders}
bidder_total = {bidder: Int(f'bidder_total_{bidder}') for bidder in bidders}
total_revenue = Int('total_revenue')

# Helper: Map item to its category
def get_category(item):
    return categories[item]

# Helper: Map bidder to their synergy bonus
def get_synergy(bidder):
    return synergy_bonuses[bidder]

# Helper: Map bidder to their budget
def get_budget(bidder):
    return budgets[bidder]

# Constraint 1: Item exclusivity
for item in items:
    opt.add(Or([And(item_alloc[item] == bid["id"], winning_bid[bid["id"]-1]) for bid in bids] +
               [item_alloc[item] == -1]))

# Constraint 2: Budget compliance and bidder_total calculation
for bidder in bidders:
    opt.add(bidder_total[bidder] == Sum([If(And(winning_bid[bid["id"]-1], bid["bidder"] == bidder),
                                            bid["price"], 0) for bid in bids]))
    opt.add(bidder_total[bidder] <= get_budget(bidder))

# Constraint 3: Synergy bonus calculation
synergy_bonus_vars = {bidder: Int(f'synergy_bonus_{bidder}') for bidder in bidders}
for bidder in bidders:
    num_winning_bids = Sum([If(And(winning_bid[bid["id"]-1], bid["bidder"] == bidder), 1, 0)
                            for bid in bids])
    opt.add(synergy_bonus_vars[bidder] == If(num_winning_bids >= 2, get_synergy(bidder), 0))

# Constraint 4: Licensing requirement
for bidder in bidders:
    # Electronics license requirement
    electronics_bids = [bid for bid in bids if any(get_category(item) == 'electronics' for item in bid["items"])]
    for bid in electronics_bids:
        opt.add(Implies(And(winning_bid[bid["id"]-1], bid["bidder"] == bidder),
                        Or([And(winning_bid[lic_bid["id"]-1], lic_bid["bidder"] == bidder, 
                                'lic_E' in lic_bid["items"]) for lic_bid in bids])))
    # Furniture license requirement
    furniture_bids = [bid for bid in bids if any(get_category(item) == 'furniture' for item in bid["items"])]
    for bid in furniture_bids:
        opt.add(Implies(And(winning_bid[bid["id"]-1], bid["bidder"] == bidder),
                        Or([And(winning_bid[lic_bid["id"]-1], lic_bid["bidder"] == bidder, 
                                'lic_F' in lic_bid["items"]) for lic_bid in bids])))

# Constraint 5: Fairness (max 3 items per bidder)
for bidder in bidders:
    opt.add(bidder_items[bidder] == Sum([If(And(winning_bid[bid["id"]-1], bid["bidder"] == bidder),
                                            len(bid["items"]), 0) for bid in bids]))
    opt.add(bidder_items[bidder] <= 3)

# Objective: Maximize total_revenue
opt.add(total_revenue == Sum([If(winning_bid[bid["id"]-1], bid["price"], 0) for bid in bids]) +
                             Sum([synergy_bonus_vars[bidder] for bidder in bidders]))
opt.maximize(total_revenue)

# Check and print result
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print("Total revenue:", model[total_revenue])
    winning_bids = [bid["id"] for bid in bids if is_true(model[winning_bid[bid["id"]-1]])]
    print("Winning bids:", sorted(winning_bids))
    item_allocation = {item: model[item_alloc[item]] for item in items}
    print("Item allocation:", item_allocation)
    # Synergy bonuses applied: check if synergy_bonus_vars[bidder] > 0
    synergy_bonuses_applied = []
    for bidder in bidders:
        if model.eval(synergy_bonus_vars[bidder], model_completion=True).as_long() > 0:
            synergy_bonuses_applied.append(bidder)
    print("Synergy bonuses applied to:", synergy_bonuses_applied)
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")