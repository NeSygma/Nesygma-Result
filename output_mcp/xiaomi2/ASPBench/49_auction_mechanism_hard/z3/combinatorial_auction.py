from z3 import *

solver = Optimize()

# === DATA ===
bidders = ['a', 'b', 'c', 'd']
budgets = {'a': 150, 'b': 200, 'c': 180, 'd': 100}
synergy_bonuses = {'a': 20, 'b': 10, 'c': 25, 'd': 5}

bid_data = [
    (1, 'a', ['item1', 'item2'], 70),
    (2, 'a', ['lic_E'], 40),
    (3, 'b', ['item3', 'item4'], 90),
    (4, 'b', ['lic_F'], 50),
    (5, 'b', ['item5'], 60),
    (6, 'c', ['item1', 'item5'], 100),
    (7, 'c', ['lic_E'], 60),
    (8, 'c', ['item3', 'item6'], 80),
    (9, 'd', ['lic_F'], 25),
    (10, 'd', ['item4'], 70),
]

all_items = ['item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'lic_E', 'lic_F']
electronics_items = {'item1', 'item2', 'item5'}
furniture_items = {'item3', 'item4', 'item6'}

# === DECISION VARIABLES ===
win = {i: Bool(f'win_{i}') for i in range(1, 11)}

# === CONSTRAINT 1: Item Exclusivity ===
# Each item appears in at most one winning bid
for item in all_items:
    bids_with_item = [i for i in range(1, 11) if item in bid_data[i-1][2]]
    for j in range(len(bids_with_item)):
        for k in range(j+1, len(bids_with_item)):
            solver.add(Not(And(win[bids_with_item[j]], win[bids_with_item[k]])))

# === CONSTRAINT 2: Budget Compliance ===
for bidder in bidders:
    bidder_bids = [(i, price) for i, b, items, price in bid_data if b == bidder]
    solver.add(Sum([If(win[i], price, 0) for i, price in bidder_bids]) <= budgets[bidder])

# === CONSTRAINT 3: Synergy Bonus (handled in objective) ===
# If a bidder wins 2+ bids, their synergy_bonus is added to revenue

# === CONSTRAINT 4: Licensing Requirement ===
for bidder in bidders:
    bidder_bids_info = [(i, items) for i, b, items, price in bid_data if b == bidder]

    # Electronics licensing
    elec_bids = [i for i, items in bidder_bids_info if any(it in electronics_items for it in items)]
    lic_e_bids = [i for i, items in bidder_bids_info if 'lic_E' in items]

    if elec_bids and lic_e_bids:
        solver.add(Implies(Or([win[i] for i in elec_bids]), Or([win[i] for i in lic_e_bids])))
    elif elec_bids and not lic_e_bids:
        # Cannot win electronics bids without a license bid
        for i in elec_bids:
            solver.add(Not(win[i]))

    # Furniture licensing
    furn_bids = [i for i, items in bidder_bids_info if any(it in furniture_items for it in items)]
    lic_f_bids = [i for i, items in bidder_bids_info if 'lic_F' in items]

    if furn_bids and lic_f_bids:
        solver.add(Implies(Or([win[i] for i in furn_bids]), Or([win[i] for i in lic_f_bids])))
    elif furn_bids and not lic_f_bids:
        # Cannot win furniture bids without a license bid
        for i in furn_bids:
            solver.add(Not(win[i]))

# === CONSTRAINT 5: Fairness - Max 3 items per bidder ===
for bidder in bidders:
    bidder_bids_info = [(i, items) for i, b, items, price in bid_data if b == bidder]
    item_count = Sum([If(win[i], len(items), 0) for i, items in bidder_bids_info])
    solver.add(item_count <= 3)

# === OBJECTIVE: Maximize Total Revenue ===
revenue_terms = []
for bidder in bidders:
    bidder_bid_ids = [i for i, b, items, price in bid_data if b == bidder]
    bidder_bids_price = [(i, price) for i, b, items, price in bid_data if b == bidder]

    # Sum of winning bid prices
    for i, price in bidder_bids_price:
        revenue_terms.append(If(win[i], price, 0))

    # Synergy bonus if 2+ winning bids
    num_wins = Sum([If(win[i], 1, 0) for i in bidder_bid_ids])
    revenue_terms.append(If(num_wins >= 2, synergy_bonuses[bidder], 0))

total_revenue = Sum(revenue_terms)
solver.maximize(total_revenue)

# === SOLVE ===
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")

    winning_bids = []
    for i in range(1, 11):
        if is_true(m.evaluate(win[i], model_completion=True)):
            winning_bids.append(i)

    winning_bids_sorted = sorted(winning_bids)
    print(f"winning_bids: {winning_bids_sorted}")

    rev = m.evaluate(total_revenue, model_completion=True)
    print(f"total_revenue: {rev}")

    # Item allocation
    item_allocation = {}
    for i in winning_bids:
        bidder = bid_data[i-1][1]
        items = bid_data[i-1][2]
        for it in items:
            item_allocation[it] = bidder
    print(f"item_allocation: {item_allocation}")

    # Synergy bonuses
    synergy_details = []
    for bidder in bidders:
        bidder_bid_ids = [i for i, b, items, price in bid_data if b == bidder]
        num_wins = sum(1 for i in bidder_bid_ids if is_true(m.evaluate(win[i], model_completion=True)))
        if num_wins >= 2:
            synergy_details.append({'bidder': bidder, 'bonus': synergy_bonuses[bidder]})
    print(f"synergy_bonuses: {synergy_details}")

    # Detailed bid info
    for i in winning_bids:
        _, bidder, items, price = bid_data[i-1]
        print(f"  Bid {i}: bidder={bidder}, items={items}, price={price}")

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")