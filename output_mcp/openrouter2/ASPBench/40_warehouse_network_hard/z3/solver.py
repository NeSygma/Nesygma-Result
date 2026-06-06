from z3 import *

# Problem data
hubs = ['H1','H2']
regionals = ['R1','R2','R3','R4']
customers = ['C1','C2','C3','C4','C5','C6']
times = [1,2,3,4]

cost_hub = {'H1':1000,'H2':1200}
cost_reg = {'R1':200,'R2':250,'R3':220,'R4':180}
capacity_hub = {'H1':400,'H2':350}
capacity_reg = {'R1':70,'R2':80,'R3':60,'R4':90}
trucks = {'H1':2,'H2':1}

demand = {'C1':20,'C2':30,'C3':15,'C4':25,'C5':35,'C6':10}
time_window = {'C1':[2,3],'C2':[1,2],'C3':[3,4],'C4':[1,4],'C5':[2,4],'C6':[1,1]}

cost_hub_to_reg = {('H1','R1'):5,('H1','R2'):6,('H2','R3'):5,('H2','R4'):6}
cost_reg_to_cust = {('R1','C1'):10,('R1','C2'):12,('R2','C2'):13,('R2','C3'):15,('R3','C4'):9,('R3','C5'):11,('R4','C5'):14,('R4','C6'):7}

connectivity_hub = {'H1':['R1','R2'],'H2':['R3','R4']}
connectivity_reg = {'R1':['C1','C2'],'R2':['C2','C3'],'R3':['C4','C5'],'R4':['C5','C6']}

maintenance = {'R2':2,'H1':4}

# Solver
solver = Optimize()

# Variables
open_hub = {h: Int(f'open_hub_{h}') for h in hubs}
open_reg = {r: Int(f'open_reg_{r}') for r in regionals}
supply = {(h,r): Int(f'supply_{h}_{r}') for h in hubs for r in regionals}
assign = {(c,r,t): Int(f'assign_{c}_{r}_{t}') for c in customers for r in regionals for t in times}

# Domain constraints
for h in hubs:
    solver.add(open_hub[h] >= 0, open_hub[h] <= 1)
for r in regionals:
    solver.add(open_reg[r] >= 0, open_reg[r] <= 1)
for h in hubs:
    for r in regionals:
        solver.add(supply[(h,r)] >= 0, supply[(h,r)] <= 1)
for c in customers:
    for r in regionals:
        for t in times:
            solver.add(assign[(c,r,t)] >= 0, assign[(c,r,t)] <= 1)

# Connectivity constraints for supply
for h in hubs:
    for r in regionals:
        if r not in connectivity_hub[h]:
            solver.add(supply[(h,r)] == 0)
        else:
            solver.add(supply[(h,r)] <= open_hub[h])
            solver.add(supply[(h,r)] <= open_reg[r])

# Each open regional has exactly one supplying hub
for r in regionals:
    solver.add(Sum([supply[(h,r)] for h in hubs]) == open_reg[r])

# Assignment constraints
# Each customer assigned exactly once
for c in customers:
    solver.add(Sum([assign[(c,r,t)] for r in regionals for t in times]) == 1)

# Assignments only if regional open and supplied
for c in customers:
    for r in regionals:
        for t in times:
            solver.add(assign[(c,r,t)] <= open_reg[r])
            solver.add(assign[(c,r,t)] <= Sum([supply[(h,r)] for h in hubs]))
            if c not in connectivity_reg[r]:
                solver.add(assign[(c,r,t)] == 0)
            if t not in time_window[c]:
                solver.add(assign[(c,r,t)] == 0)
            if r == 'R2' and t == 2:
                solver.add(assign[(c,r,t)] == 0)
            if t == 4:
                # H1 unavailable at time 4, so cannot deliver from any regional supplied by H1
                solver.add(assign[(c,r,t)] <= 1 - supply[('H1',r)])

# Regional capacity
for r in regionals:
    total_demand_r = Sum([assign[(c,r,t)] * demand[c] for c in customers for t in times])
    solver.add(total_demand_r <= capacity_reg[r] * open_reg[r])

# Hub capacity
for h in hubs:
    total_demand_h = Sum([If(supply[(h,r)] == 1,
                             Sum([assign[(c,r,t)] * demand[c] for c in customers for t in times]),
                             0) for r in regionals])
    solver.add(total_demand_h <= capacity_hub[h] * open_hub[h])

# Truck limits per hub per time slot
for h in hubs:
    for t in times:
        deliveries = Sum([If(supply[(h,r)] == 1,
                              Sum([assign[(c,r,t)] for c in customers]),
                              0) for r in regionals])
        solver.add(deliveries <= trucks[h])

# Objective: total cost
open_cost = Sum([open_hub[h] * cost_hub[h] for h in hubs]) + Sum([open_reg[r] * cost_reg[r] for r in regionals])
# Hub-to-regional transport cost
hub_to_reg_cost = Sum([supply[(h,r)] * cost_hub_to_reg.get((h,r),0) * Sum([assign[(c,r,t)] * demand[c] for c in customers for t in times])
                       for h in hubs for r in regionals])
# Regional-to-customer transport cost
reg_to_cust_cost = Sum([assign[(c,r,t)] * demand[c] * cost_reg_to_cust.get((r,c),0)
                        for c in customers for r in regionals for t in times])

total_cost_expr = open_cost + hub_to_reg_cost + reg_to_cust_cost
solver.minimize(total_cost_expr)

# Solve
result = solver.check()
if result == sat:
    model = solver.model()
    open_hubs_list = [h for h in hubs if model[open_hub[h]] == 1]
    open_regionals_list = [r for r in regionals if model[open_reg[r]] == 1]
    hub_assignments = {}
    for r in regionals:
        for h in hubs:
            if model[supply[(h,r)]] == 1:
                hub_assignments[r] = h
    customer_deliveries = []
    for c in customers:
        for r in regionals:
            for t in times:
                if model[assign[(c,r,t)]] == 1:
                    customer_deliveries.append((c,r,t))
    total_cost_val = model.evaluate(total_cost_expr, model_completion=True).as_long()
    print("STATUS: sat")
    print("open_hubs =", open_hubs_list)
    print("open_regionals =", open_regionals_list)
    print("hub_assignments =", hub_assignments)
    print("customer_deliveries =", customer_deliveries)
    print("total_cost =", total_cost_val)
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")