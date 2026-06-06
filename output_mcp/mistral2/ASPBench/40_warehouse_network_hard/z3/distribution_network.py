from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# --- Declare symbolic variables ---

# Binary: whether a facility is opened
open_h1 = Bool('open_h1')
open_h2 = Bool('open_h2')
open_r1 = Bool('open_r1')
open_r2 = Bool('open_r2')
open_r3 = Bool('open_r3')
open_r4 = Bool('open_r4')

# Hub assignment for regional warehouses (which hub supplies it)
hub_assign_r1 = Int('hub_assign_r1')  # 1 for H1, 2 for H2
hub_assign_r2 = Int('hub_assign_r2')
hub_assign_r3 = Int('hub_assign_r3')
hub_assign_r4 = Int('hub_assign_r4')

# Customer delivery assignments: (regional, time slot)
# We represent as a list of tuples: (customer, regional, time slot)
# We'll use Int variables for regional and time slot for each customer
c1_regional = Int('c1_regional')
c1_time = Int('c1_time')
c2_regional = Int('c2_regional')
c2_time = Int('c2_time')
c3_regional = Int('c3_regional')
c3_time = Int('c3_time')
c4_regional = Int('c4_regional')
c4_time = Int('c4_time')
c5_regional = Int('c5_regional')
c5_time = Int('c5_time')
c6_regional = Int('c6_regional')
c6_time = Int('c6_time')

# --- Helper functions ---

def regional_to_int(r):
    return {
        'R1': 1,
        'R2': 2,
        'R3': 3,
        'R4': 4
    }[r]

def hub_to_int(h):
    return {
        'H1': 1,
        'H2': 2
    }[h]

def customer_demand(c):
    return {
        'C1': 20,
        'C2': 30,
        'C3': 15,
        'C4': 25,
        'C5': 35,
        'C6': 10
    }[c]

def customer_time_window(c):
    return {
        'C1': (2, 3),
        'C2': (1, 2),
        'C3': (3, 4),
        'C4': (1, 4),
        'C5': (2, 4),
        'C6': (1, 1)
    }[c]

# --- Fixed data ---

# Opening costs
hub_opening_cost = {
    'H1': 1000,
    'H2': 1200
}
regional_opening_cost = {
    'R1': 200,
    'R2': 250,
    'R3': 220,
    'R4': 180
}

# Hub capacities
hub_capacity = {
    'H1': 400,
    'H2': 350
}

# Regional capacities
regional_capacity = {
    'R1': 70,
    'R2': 80,
    'R3': 60,
    'R4': 90
}

# Truck resources per hub per time slot
truck_resources = {
    'H1': [2, 2, 2, 2],  # 2 trucks per time slot
    'H2': [1, 1, 1, 1]   # 1 truck per time slot
}

# Hub to regional transport costs (per unit demand)
hub_to_regional_cost = {
    ('H1', 'R1'): 5,
    ('H1', 'R2'): 6,
    ('H2', 'R3'): 5,
    ('H2', 'R4'): 6
}

# Regional to customer transport costs (per unit demand)
regional_to_customer_cost = {
    ('R1', 'C1'): 10,
    ('R1', 'C2'): 12,
    ('R2', 'C2'): 13,
    ('R2', 'C3'): 15,
    ('R3', 'C4'): 9,
    ('R3', 'C5'): 11,
    ('R4', 'C5'): 14,
    ('R4', 'C6'): 7
}

# Connectivity constraints
hub_supplies_regional = {
    'H1': ['R1', 'R2'],
    'H2': ['R3', 'R4']
}

regional_serves_customer = {
    'R1': ['C1', 'C2'],
    'R2': ['C2', 'C3'],
    'R3': ['C4', 'C5'],
    'R4': ['C5', 'C6']
}

# Maintenance slots
maintenance_unavailable = {
    'R2': [2],
    'H1': [4]
}

# --- Constraints ---

solver = Optimize()

# 1. Hub assignment variables must be 1 or 2 (H1 or H2)
for r in ['r1', 'r2', 'r3', 'r4']:
    var = globals()[f'hub_assign_{r}']
    solver.add(Or(var == 1, var == 2))

# 2. Customer regional assignments must be 1,2,3,4 (R1,R2,R3,R4)
for c in ['c1', 'c2', 'c3', 'c4', 'c5', 'c6']:
    regional_var = globals()[f'{c}_regional']
    solver.add(Or(regional_var == 1, regional_var == 2, regional_var == 3, regional_var == 4))

# 3. Customer time slots must be 1,2,3,4
for c in ['c1', 'c2', 'c3', 'c4', 'c5', 'c6']:
    time_var = globals()[f'{c}_time']
    solver.add(Or(time_var == 1, time_var == 2, time_var == 3, time_var == 4))

# 4. If a regional warehouse is opened, it must be assigned to exactly one hub
# H1 supplies R1, R2; H2 supplies R3, R4
solver.add(Implies(open_r1, hub_assign_r1 == 1))
solver.add(Implies(open_r2, hub_assign_r2 == 1))
solver.add(Implies(open_r3, hub_assign_r3 == 2))
solver.add(Implies(open_r4, hub_assign_r4 == 2))

# 5. If a hub is not opened, no regional warehouse can be assigned to it
solver.add(Not(And(open_h1 == False, hub_assign_r1 == 1)))
solver.add(Not(And(open_h1 == False, hub_assign_r2 == 1)))
solver.add(Not(And(open_h2 == False, hub_assign_r3 == 2)))
solver.add(Not(And(open_h2 == False, hub_assign_r4 == 2)))

# 6. Each customer must be assigned to a regional warehouse that serves them
for c in ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']:
    c_regional_var = globals()[f'{c[0].lower()}{c[1]}_regional']
    c_time_var = globals()[f'{c[0].lower()}{c[1]}_time']
    demand = customer_demand(c)
    time_window = customer_time_window(c)
    # Regional must be one that serves the customer
    allowed_regionals = regional_serves_customer.keys()
    for r in allowed_regionals:
        r_int = regional_to_int(r)
        # If assigned to this regional, it must be open
        regional_opened = globals()[f'open_{r.lower()}']
        solver.add(Implies(c_regional_var == r_int, regional_opened == True))
    # Time must be within window
    solver.add(c_time_var >= time_window[0])
    solver.add(c_time_var <= time_window[1])

# 7. Maintenance: no deliveries through facilities during maintenance
# R2 unavailable at time slot 2
solver.add(Not(And(c2_regional == 2, c2_time == 2)))
solver.add(Not(And(c3_regional == 2, c3_time == 2)))
# H1 unavailable at time slot 4 (no hub assignment at time slot 4, but hub assignment is not time-dependent)
# Since hub assignment is not time-dependent, we assume maintenance only affects regional warehouses

# 8. Regional capacity: total demand served by each regional <= its capacity
# We need to sum demand for each regional over all customers assigned to it
for r in ['R1', 'R2', 'R3', 'R4']:
    r_int = regional_to_int(r)
    total_demand = Int(f'total_demand_{r}')
    # Sum demand for all customers assigned to this regional
    demand_exprs = []
    for c in ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']:
        c_lower = c[0].lower() + c[1]
        demand_val = customer_demand(c)
        regional_var = globals()[f'{c_lower}_regional']
        demand_exprs.append(If(regional_var == r_int, demand_val, 0))
    solver.add(total_demand == Sum(demand_exprs))
    solver.add(total_demand <= regional_capacity[r])
    # If the regional is not opened, total demand must be 0
    solver.add(Implies(Not(globals()[f'open_{r.lower()}']), total_demand == 0))

# 9. Hub capacity: total demand passing through each hub <= its capacity
# Total demand = sum of demands of all customers served by regionals supplied by the hub
for h in ['H1', 'H2']:
    h_int = hub_to_int(h)
    total_demand = Int(f'hub_total_demand_{h}')
    # Sum demand for all customers whose regional is supplied by this hub
    demand_exprs = []
    for c in ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']:
        c_lower = c[0].lower() + c[1]
        demand_val = customer_demand(c)
        regional_var = globals()[f'{c_lower}_regional']
        # For each customer, if its regional is supplied by this hub, add its demand
        for r in ['R1', 'R2', 'R3', 'R4']:
            if r in hub_supplies_regional.get(h, []):
                r_int = regional_to_int(r)
                demand_exprs.append(If(regional_var == r_int, demand_val, 0))
    solver.add(total_demand == Sum(demand_exprs))
    solver.add(total_demand <= hub_capacity[h])

# 10. Truck limits: number of customer deliveries in each time slot from regionals supplied by a hub <= trucks available
for h in ['H1', 'H2']:
    for t in range(1, 5):  # time slots 1-4
        deliveries_in_slot = Int(f'deliveries_in_slot_{h}_{t}')
        # Count number of customers assigned to a regional supplied by this hub at this time
        count_exprs = []
        for c in ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']:
            c_lower = c[0].lower() + c[1]
            regional_var = globals()[f'{c_lower}_regional']
            time_var = globals()[f'{c_lower}_time']
            # For each customer, if its regional is supplied by this hub and time matches
            for r in ['R1', 'R2', 'R3', 'R4']:
                if r in hub_supplies_regional.get(h, []):
                    r_int = regional_to_int(r)
                    count_exprs.append(If(And(regional_var == r_int, time_var == t), 1, 0))
        solver.add(deliveries_in_slot == Sum(count_exprs))
        solver.add(deliveries_in_slot <= truck_resources[h][t-1])  # t-1 because list is 0-indexed

# --- Objective: Minimize total cost ---

# Fixed opening costs
fixed_cost = (
    If(open_h1, hub_opening_cost['H1'], 0) +
    If(open_h2, hub_opening_cost['H2'], 0) +
    If(open_r1, regional_opening_cost['R1'], 0) +
    If(open_r2, regional_opening_cost['R2'], 0) +
    If(open_r3, regional_opening_cost['R3'], 0) +
    If(open_r4, regional_opening_cost['R4'], 0)
)

# Hub-to-regional transport costs: for each regional, if opened and assigned to a hub, add (total demand of regional) * (unit cost)
hub_to_regional_transport_cost = Int('hub_to_regional_transport_cost')
terms = []
for r in ['R1', 'R2', 'R3', 'R4']:
    r_int = regional_to_int(r)
    regional_opened = globals()[f'open_{r.lower()}']
    total_demand_r = Int(f'total_demand_{r}')
    # Unit cost depends on hub and regional
    # H1 supplies R1, R2; H2 supplies R3, R4
    if r in ['R1', 'R2']:
        unit_cost = 5 if r == 'R1' else 6
        terms.append(If(And(regional_opened, hub_assign_r1 == 1 if r == 'R1' else hub_assign_r2 == 1), total_demand_r * unit_cost, 0))
    else:
        unit_cost = 5 if r == 'R3' else 6
        terms.append(If(And(regional_opened, hub_assign_r3 == 2 if r == 'R3' else hub_assign_r4 == 2), total_demand_r * unit_cost, 0))

solver.add(hub_to_regional_transport_cost == Sum(terms))

# Regional-to-customer transport costs: for each customer, add demand * cost
regional_to_customer_transport_cost = Int('regional_to_customer_transport_cost')
terms = []
for c in ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']:
    c_lower = c[0].lower() + c[1]
    demand_val = customer_demand(c)
    regional_var = globals()[f'{c_lower}_regional']
    # Find cost based on regional and customer
    cost = None
    for r in ['R1', 'R2', 'R3', 'R4']:
        if c in regional_serves_customer.get(r, []):
            cost = regional_to_customer_cost[(r, c)]
    if cost is not None:
        terms.append(demand_val * cost)

solver.add(regional_to_customer_transport_cost == Sum(terms))

# Total cost
total_cost_expr = fixed_cost + hub_to_regional_transport_cost + regional_to_customer_transport_cost

# --- Solve ---

solver.minimize(total_cost_expr)
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Total cost:", model.eval(total_cost_expr))
    print("Open hubs:")
    print("  H1:", model[open_h1])
    print("  H2:", model[open_h2])
    print("Open regionals:")
    print("  R1:", model[open_r1])
    print("  R2:", model[open_r2])
    print("  R3:", model[open_r3])
    print("  R4:", model[open_r4])
    print("Hub assignments:")
    print("  R1 -> H", model[hub_assign_r1])
    print("  R2 -> H", model[hub_assign_r2])
    print("  R3 -> H", model[hub_assign_r3])
    print("  R4 -> H", model[hub_assign_r4])
    print("Customer deliveries:")
    print("  C1 -> R", model[c1_regional], "at time", model[c1_time])
    print("  C2 -> R", model[c2_regional], "at time", model[c2_time])
    print("  C3 -> R", model[c3_regional], "at time", model[c3_time])
    print("  C4 -> R", model[c4_regional], "at time", model[c4_time])
    print("  C5 -> R", model[c5_regional], "at time", model[c5_time])
    print("  C6 -> R", model[c6_regional], "at time", model[c6_time])
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")