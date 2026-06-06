from z3 import *

# Data
hubs = ['H1', 'H2']
regionals = ['R1', 'R2', 'R3', 'R4']
customers = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']
time_slots = [1, 2, 3, 4]

hub_costs = {'H1': 1000, 'H2': 1200}
reg_costs = {'R1': 200, 'R2': 250, 'R3': 220, 'R4': 180}
hub_caps = {'H1': 400, 'H2': 350}
reg_caps = {'R1': 70, 'R2': 80, 'R3': 60, 'R4': 90}
trucks = {'H1': {1: 2, 2: 2, 3: 2, 4: 0}, 'H2': {1: 1, 2: 1, 3: 1, 4: 1}}
cust_demands = {'C1': 20, 'C2': 30, 'C3': 15, 'C4': 25, 'C5': 35, 'C6': 10}
cust_windows = {'C1': (2, 3), 'C2': (1, 2), 'C3': (3, 4), 'C4': (1, 4), 'C5': (2, 4), 'C6': (1, 1)}
h_r_costs = {('H1', 'R1'): 5, ('H1', 'R2'): 6, ('H2', 'R3'): 5, ('H2', 'R4'): 6}
r_c_costs = {('R1', 'C1'): 10, ('R1', 'C2'): 12, ('R2', 'C2'): 13, ('R2', 'C3'): 15, ('R3', 'C4'): 9, ('R3', 'C5'): 11, ('R4', 'C5'): 14, ('R4', 'C6'): 7}
connectivity_h_r = {'H1': ['R1', 'R2'], 'H2': ['R3', 'R4']}
connectivity_r_c = {'R1': ['C1', 'C2'], 'R2': ['C2', 'C3'], 'R3': ['C4', 'C5'], 'R4': ['C5', 'C6']}
maintenance = {'R2': [2], 'H1': [4]}

# Solver
solver = Solver()

# Variables
hub_open = {h: Bool(f'hub_open_{h}') for h in hubs}
reg_open = {r: Bool(f'reg_open_{r}') for r in regionals}
hub_supplies_reg = {(h, r): Bool(f'hsr_{h}_{r}') for h in hubs for r in regionals if r in connectivity_h_r[h]}
cust_assigned_to_reg = {(c, r, t): Bool(f'catr_{c}_{r}_{t}') for c in customers for r in regionals for t in time_slots if r in connectivity_r_c.get(c, [])}

# Constraints
for c in customers:
    for r in regionals:
        for t in time_slots:
            if (c, r, t) in cust_assigned_to_reg:
                solver.add(Implies(cust_assigned_to_reg[(c, r, t)], reg_open[r]))
                h_options = [h for h in hubs if r in connectivity_h_r[h]]
                solver.add(Implies(cust_assigned_to_reg[(c, r, t)], Or([And(hub_supplies_reg[(h, r)], hub_open[h]) for h in h_options])))

for c in customers:
    solver.add(Sum([If(cust_assigned_to_reg[(c, r, t)], 1, 0) for r in regionals for t in time_slots if (c, r, t) in cust_assigned_to_reg]) == 1)

for r in regionals:
    h_options = [h for h in hubs if r in connectivity_h_r[h]]
    solver.add(Sum([If(hub_supplies_reg[(h, r)], 1, 0) for h in h_options]) == If(reg_open[r], 1, 0))

for c in customers:
    start, end = cust_windows[c]
    for r in regionals:
        for t in time_slots:
            if (c, r, t) in cust_assigned_to_reg:
                if t < start or t > end:
                    solver.add(Not(cust_assigned_to_reg[(c, r, t)]))

for r in regionals:
    if r in maintenance:
        for t in maintenance[r]:
            for c in customers:
                if (c, r, t) in cust_assigned_to_reg:
                    solver.add(Not(cust_assigned_to_reg[(c, r, t)]))
for h in hubs:
    if h in maintenance:
        for t in maintenance[h]:
            for r in regionals:
                if (h, r) in hub_supplies_reg:
                    for c in customers:
                        if (c, r, t) in cust_assigned_to_reg:
                            solver.add(Not(cust_assigned_to_reg[(c, r, t)]))

for r in regionals:
    solver.add(Sum([If(cust_assigned_to_reg[(c, r, t)], cust_demands[c], 0) for c in customers for t in time_slots if (c, r, t) in cust_assigned_to_reg]) <= reg_caps[r])

for h in hubs:
    solver.add(Sum([If(hub_supplies_reg[(h, r)], Sum([If(cust_assigned_to_reg[(c, r, t)], cust_demands[c], 0) for c in customers for t in time_slots if (c, r, t) in cust_assigned_to_reg]), 0) for r in regionals if (h, r) in hub_supplies_reg]) <= hub_caps[h])

for h in hubs:
    for t in time_slots:
        solver.add(Sum([If(And(hub_supplies_reg[(h, r)], cust_assigned_to_reg[(c, r, t)]), 1, 0) for r in regionals for c in customers if (h, r) in hub_supplies_reg and (c, r, t) in cust_assigned_to_reg]) <= trucks[h][t])

if solver.check() == sat:
    print("STATUS: sat")
else:
    print("STATUS: unsat")
    print(solver.unsat_core())