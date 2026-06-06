from z3 import *

# Define bids
bids = [
    {'bidder':'A', 'items':['item1','item2'], 'price':100},
    {'bidder':'A', 'items':['item3'], 'price':50},
    {'bidder':'B', 'items':['item2','item3'], 'price':120},
    {'bidder':'B', 'items':['item4','item5'], 'price':80},
    {'bidder':'C', 'items':['item1','item3','item5'], 'price':150},
    {'bidder':'D', 'items':['item4'], 'price':40}
]

items = ['item1','item2','item3','item4','item5']

opt = Optimize()
# binary variables for each bid
bid_vars = [Int(f'bid_{i}') for i in range(len(bids))]
for v in bid_vars:
    opt.add(v >= 0, v <= 1)

# item constraints: each item at most one bid selected
for item in items:
    opt.add(Sum([If(v==1, 1, 0) for v, bid in zip(bid_vars, bids) if item in bid['items']]) <= 1)

# objective: maximize revenue
revenue_expr = Sum([v * bid['price'] for v, bid in zip(bid_vars, bids)])
opt.maximize(revenue_expr)

# Solve
result = opt.check()
if result == sat:
    model = opt.model()
    total_rev = model.evaluate(revenue_expr).as_long()
    # Determine winning bids
    winning = []
    for i, v in enumerate(bid_vars):
        if model.evaluate(v).as_long() == 1:
            winning.append(bids[i])
    # Build item allocation
    allocation = {item: None for item in items}
    for bid in winning:
        for item in bid['items']:
            allocation[item] = bid['bidder']
    # Output
    print("STATUS: sat")
    print("total_revenue =", total_rev)
    print("winning_bids = [")
    for bid in winning:
        print(f"  {{'bidder': '{bid['bidder']}', 'items': {bid['items']}, 'price': {bid['price']}}},")
    print("]")
    print("item_allocation = {")
    for item in items:
        print(f"  '{item}': '{allocation[item]}'")
    print("}")
else:
    print("STATUS: unsat")
    if result == unknown:
        print("RAW_RESULT: unknown")