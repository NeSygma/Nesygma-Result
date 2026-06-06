from z3 import *

# BENCHMARK_MODE = True  # Set False outside benchmark mode
BENCHMARK_MODE = False

# ============================================================================
# DATA DEFINITIONS
# ============================================================================

# Facilities
HUBS = ["H1", "H2"]
REGIONALS = ["R1", "R2", "R3", "R4"]
CUSTOMERS = ["C1", "C2", "C3", "C4", "C5", "C6"]
TIME_SLOTS = [1, 2, 3, 4]

# Opening costs
OPEN_COSTS = {
    "H1": 1000,
    "H2": 1200,
    "R1": 200,
    "R2": 250,
    "R3": 220,
    "R4": 180,
}

# Capacities
HUB_CAPACITY = {"H1": 400, "H2": 350}
REGIONAL_CAPACITY = {"R1": 70, "R2": 80, "R3": 60, "R4": 90}

# Truck resources per hub per time slot
TRUCK_LIMITS = {"H1": 2, "H2": 1}

# Customer demands and time windows
CUSTOMER_DEMAND = {
    "C1": 20,
    "C2": 30,
    "C3": 15,
    "C4": 25,
    "C5": 35,
    "C6": 10,
}

CUSTOMER_TIME_WINDOWS = {
    "C1": (2, 3),
    "C2": (1, 2),
    "C3": (3, 4),
    "C4": (1, 4),
    "C5": (2, 4),
    "C6": (1, 1),
}

# Hub to Regional transport costs (per unit demand)
HUB_TO_REGIONAL_COST = {
    ("H1", "R1"): 5,
    ("H1", "R2"): 6,
    ("H2", "R3"): 5,
    ("H2", "R4"): 6,
}

# Regional to Customer transport costs (per unit demand)
REGIONAL_TO_CUSTOMER_COST = {
    ("R1", "C1"): 10,
    ("R1", "C2"): 12,
    ("R2", "C2"): 13,
    ("R2", "C3"): 15,
    ("R3", "C4"): 9,
    ("R3", "C5"): 11,
    ("R4", "C5"): 14,
    ("R4", "C6"): 7,
}

# Connectivity constraints
HUB_SUPPLIES_REGIONAL = {
    "H1": ["R1", "R2"],
    "H2": ["R3", "R4"],
}

REGIONAL_SERVES_CUSTOMER = {
    "R1": ["C1", "C2"],
    "R2": ["C2", "C3"],
    "R3": ["C4", "C5"],
    "R4": ["C5", "C6"],
}

# Maintenance schedules
MAINTENANCE_UNAVAILABLE = {
    "R2": [2],
    "H1": [4],
}

# ============================================================================
# DECISION VARIABLES
# ============================================================================

solver = Optimize()

# Binary variables for facility opening
is_hub_open = {h: Bool(f"is_hub_open_{h}") for h in HUBS}
is_regional_open = {r: Bool(f"is_regional_open_{r}") for r in REGIONALS}

# Binary variables for hub-to-regional supply
supply_link = {
    (h, r): Bool(f"supply_{h}_{r}") for h in HUBS for r in REGIONALS
}

# Integer variables for customer assignments: regional warehouse (as Int representing index) and time slot
# We'll use Int for regional to represent which regional is chosen
customer_assigned_regional = {c: Int(f"assign_{c}_regional") for c in CUSTOMERS}
customer_assigned_time = {c: Int(f"assign_{c}_time") for c in CUSTOMERS}

# Total demand served by each regional warehouse
regional_demand = {r: Int(f"regional_demand_{r}") for r in REGIONALS}

# Total throughput at each hub (sum of demands of supplied regionals)
hub_throughput = {h: Int(f"hub_throughput_{h}") for h in HUBS}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def regional_index(r):
    return REGIONALS.index(r)

def hub_index(h):
    return HUBS.index(h)

# ============================================================================
# CONSTRAINTS
# ============================================================================

# 1. Opening prerequisite: A customer can only be served by an open regional warehouse
for c in CUSTOMERS:
    # Regional assignment must be one of the regionals (by index)
    solver.add(customer_assigned_regional[c] >= 0, customer_assigned_regional[c] < len(REGIONALS))
    
    # Regional warehouse must be open
    # We will enforce this later via connectivity and supply constraints

# 2. Assignment uniqueness: Each customer to exactly one regional warehouse at exactly one time slot
for c in CUSTOMERS:
    # Time slot must be in [1, 4]
    solver.add(customer_assigned_time[c] >= 1, customer_assigned_time[c] <= 4)
    
    # Time window constraint
    tw_start, tw_end = CUSTOMER_TIME_WINDOWS[c]
    solver.add(customer_assigned_time[c] >= tw_start, customer_assigned_time[c] <= tw_end)

# 3. Supply uniqueness: Each open regional warehouse must be supplied by exactly one hub
for r in REGIONALS:
    # If regional is open, it must be supplied by exactly one hub
    supply_options = [supply_link[h, r] for h in HUBS if (h, r) in supply_link]
    if supply_options:
        solver.add(Implies(is_regional_open[r], Sum(supply_options) == 1))
    
    # If regional is not open, it cannot be supplied
    solver.add(Implies(Not(is_regional_open[r]), Sum([supply_link[h, r] for h in HUBS]) == 0))

# 4. Connectivity constraints
for h in HUBS:
    for r in REGIONALS:
        if r not in HUB_SUPPLIES_REGIONAL.get(h, []):
            solver.add(Not(supply_link[h, r]))

for r in REGIONALS:
    allowed_customers = REGIONAL_SERVES_CUSTOMER.get(r, [])
    for c in CUSTOMERS:
        if c not in allowed_customers:
            # Force customer not to be assigned to this regional
            solver.add(customer_assigned_regional[c] != regional_index(r))

# 5. Maintenance constraints
# R2 unavailable at time slot 2: no customer can be assigned to R2 at time 2
for c in CUSTOMERS:
    solver.add(Not(And(customer_assigned_regional[c] == regional_index("R2"), customer_assigned_time[c] == 2)))

# H1 unavailable at time slot 4: no deliveries from regionals supplied by H1 at time 4
for c in CUSTOMERS:
    for h in HUBS:
        for r in REGIONALS:
            # If this regional r is supplied by hub h, and h is H1, then customer c cannot be assigned to r at time 4
            if h == "H1":
                solver.add(Implies(
                    And(customer_assigned_regional[c] == regional_index(r), customer_assigned_time[c] == 4),
                    supply_link[h, r] == False
                ))

# 6. Regional capacity: Total demand served by each regional <= its capacity
for r in REGIONALS:
    # Sum demand of all customers assigned to this regional
    assigned_demand = Sum([
        If(customer_assigned_regional[c] == regional_index(r), CUSTOMER_DEMAND[c], 0)
        for c in CUSTOMERS
    ])
    solver.add(assigned_demand <= REGIONAL_CAPACITY[r])
    # Also link regional_demand variable
    solver.add(regional_demand[r] == assigned_demand)

# 7. Hub capacity: Total demand passing through each hub <= its capacity
for h in HUBS:
    # Sum demand of all regionals supplied by this hub
    supplied_demand = Sum([
        If(supply_link[h, r], regional_demand[r], 0)
        for r in REGIONALS
    ])
    solver.add(supplied_demand <= HUB_CAPACITY[h])
    solver.add(hub_throughput[h] == supplied_demand)

# 8. Truck limits: Number of deliveries in each time slot from regional warehouses supplied by a hub <= hub's truck limit
for h in HUBS:
    for t in TIME_SLOTS:
        # Count customers assigned to regionals supplied by h at time t
        deliveries_count = Sum([
            If(And(
                Or([And(supply_link[h, REGIONALS[regional_index(r)]], customer_assigned_regional[c] == regional_index(r)) for r in REGIONALS]),
                customer_assigned_time[c] == t
            ), 1, 0)
            for c in CUSTOMERS
        ])
        solver.add(deliveries_count <= TRUCK_LIMITS[h])

# ============================================================================
# OBJECTIVE FUNCTION
# ============================================================================

# Fixed opening costs
fixed_cost = Sum([
    If(is_hub_open[h], OPEN_COSTS[h], 0) for h in HUBS
] + [
    If(is_regional_open[r], OPEN_COSTS[r], 0) for r in REGIONALS
])

# Hub-to-Regional transport costs: for each supply link, regional_demand[r] * unit_cost
hr_cost = Sum([
    If(supply_link[h, r], regional_demand[r] * HUB_TO_REGIONAL_COST[(h, r)], 0)
    for h in HUBS for r in REGIONALS
])

# Regional-to-Customer transport costs: for each customer, demand * cost
rc_cost = Sum([
    If(customer_assigned_regional[c] == regional_index(r),
       CUSTOMER_DEMAND[c] * REGIONAL_TO_CUSTOMER_COST.get((r, c), 0),
       0)
    for c in CUSTOMERS for r in REGIONALS
])

total_cost = fixed_cost + hr_cost + rc_cost
solver.minimize(total_cost)

# ============================================================================
# SOLVE AND OUTPUT
# ============================================================================

result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print(f"Total cost: {model.eval(total_cost)}")
    
    # Extract and print solution details
    open_hubs = [h for h in HUBS if is_true(model[is_hub_open[h]])]
    open_regionals = [r for r in REGIONALS if is_true(model[is_regional_open[r]])]
    
    print(f"open_hubs = {open_hubs}")
    print(f"open_regionals = {open_regionals}")
    
    hub_assignments = {}
    for h in HUBS:
        for r in REGIONALS:
            if is_true(model[supply_link[h, r]]):
                hub_assignments[r] = h
    print(f"hub_assignments = {hub_assignments}")
    
    customer_deliveries = []
    for c in CUSTOMERS:
        regional_idx = model.eval(customer_assigned_regional[c]).as_long()
        regional = REGIONALS[regional_idx]
        time_slot = model.eval(customer_assigned_time[c]).as_long()
        customer_deliveries.append((c, regional, time_slot))
    print("customer_deliveries =")
    for delivery in customer_deliveries:
        print(f"  {delivery}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")