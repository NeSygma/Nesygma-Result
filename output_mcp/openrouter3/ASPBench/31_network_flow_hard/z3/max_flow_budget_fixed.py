from z3 import *

# Problem data
nodes = [1, 2, 3, 4, 5, 6, 7, 8]
source = 1
sink = 8
budget = 100
priority_nodes = [3, 5]

# Edge data: (from, to, capacity, cost, type)
# type: 0 = standard, 1 = premium
edges_data = [
    (1, 2, 10, 2, 0),  # standard
    (1, 3, 12, 4, 1),  # premium
    (2, 4, 8, 1, 0),   # standard
    (2, 5, 4, 3, 1),   # premium
    (3, 4, 5, 3, 0),   # standard
    (3, 6, 10, 5, 1),  # premium
    (4, 7, 10, 2, 0),  # standard
    (5, 7, 7, 4, 1),   # premium
    (6, 8, 12, 2, 1),  # premium
    (7, 8, 15, 1, 0)   # standard
]

# Create solver
solver = Solver()

# Declare flow variables for each edge
flow_vars = []
for i, (u, v, cap, cost, edge_type) in enumerate(edges_data):
    f = Int(f'flow_{u}_{v}')
    solver.add(f >= 0, f <= cap)
    flow_vars.append((u, v, f, cap, cost, edge_type))

# Total flow from source to sink (to maximize)
total_flow = Int('total_flow')
solver.add(total_flow >= 0)

# Calculate total flow from source (sum of outgoing from node 1)
source_outgoing = Sum([f for (u, v, f, cap, cost, edge_type) in flow_vars if u == source])
solver.add(total_flow == source_outgoing)

# Flow conservation for intermediate nodes
intermediate_nodes = [2, 3, 4, 5, 6, 7]
for node in intermediate_nodes:
    incoming = Sum([f for (u, v, f, cap, cost, edge_type) in flow_vars if v == node])
    outgoing = Sum([f for (u, v, f, cap, cost, edge_type) in flow_vars if u == node])
    solver.add(incoming == outgoing)

# Budget constraint
total_cost_expr = Sum([f * cost for (u, v, f, cap, cost, edge_type) in flow_vars])
solver.add(total_cost_expr <= budget)

# Calculate total standard and premium flow
standard_flow = Sum([f for (u, v, f, cap, cost, edge_type) in flow_vars if edge_type == 0])
premium_flow = Sum([f for (u, v, f, cap, cost, edge_type) in flow_vars if edge_type == 1])

# Flow balancing: standard >= 0.5 * premium
solver.add(standard_flow >= premium_flow / 2)

# Priority node constraints
for node in priority_nodes:
    # Get outgoing edges from this node
    outgoing_edges = [(u, v, f, cap, cost, edge_type) for (u, v, f, cap, cost, edge_type) in flow_vars if u == node]
    if outgoing_edges:
        # Calculate total outgoing flow
        total_outgoing = Sum([f for (u, v, f, cap, cost, edge_type) in outgoing_edges])
        # Calculate premium outgoing flow
        premium_outgoing = Sum([f for (u, v, f, cap, cost, edge_type) in outgoing_edges if edge_type == 1])
        
        # If there is incoming flow to this node, then premium_outgoing >= 0.75 * total_outgoing
        incoming_to_node = Sum([f for (u, v, f, cap, cost, edge_type) in flow_vars if v == node])
        
        # Use implication: if incoming > 0, then premium_outgoing >= 0.75 * total_outgoing
        # We'll use a linear formulation: 4 * premium_outgoing >= 3 * total_outgoing when incoming > 0
        # But we need to handle the case where total_outgoing = 0
        
        # Better approach: use implication with a boolean variable
        has_incoming = Bool(f'has_incoming_{node}')
        solver.add(has_incoming == (incoming_to_node > 0))
        
        # When has_incoming is true, enforce the constraint
        solver.add(Implies(has_incoming, premium_outgoing * 4 >= 3 * total_outgoing))

# Use optimization to maximize total flow
opt = Optimize()
opt.add(solver.assertions())
opt.maximize(total_flow)

# Check and print results
result = opt.check()
if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print(f"Maximum flow: {model[total_flow]}")
    
    # Evaluate complex expressions using model.eval()
    total_cost_val = model.eval(total_cost_expr, model_completion=True)
    standard_flow_val = model.eval(standard_flow, model_completion=True)
    premium_flow_val = model.eval(premium_flow, model_completion=True)
    
    print(f"Total cost: {total_cost_val}")
    print(f"Standard flow: {standard_flow_val}")
    print(f"Premium flow: {premium_flow_val}")
    print("\nEdge flows:")
    for (u, v, f, cap, cost, edge_type) in flow_vars:
        flow_val = model[f]
        type_str = "standard" if edge_type == 0 else "premium"
        print(f"  Edge ({u},{v}): flow={flow_val}, capacity={cap}, cost={cost}, type={type_str}")
    
    # Verify constraints
    print("\nConstraint verification:")
    print(f"  Budget constraint: {total_cost_val} <= {budget}: {total_cost_val <= budget}")
    print(f"  Flow balancing: standard >= 0.5 * premium: {standard_flow_val} >= {premium_flow_val/2}: {standard_flow_val * 2 >= premium_flow_val}")
    
    # Check priority nodes
    for node in priority_nodes:
        outgoing_edges = [(u, v, f, cap, cost, edge_type) for (u, v, f, cap, cost, edge_type) in flow_vars if u == node]
        if outgoing_edges:
            total_out = sum(model[f] for (u, v, f, cap, cost, edge_type) in outgoing_edges)
            premium_out = sum(model[f] for (u, v, f, cap, cost, edge_type) in outgoing_edges if edge_type == 1)
            incoming = sum(model[f] for (u, v, f, cap, cost, edge_type) in flow_vars if v == node)
            if incoming > 0:
                ratio = premium_out / total_out if total_out > 0 else 0
                print(f"  Node {node}: incoming={incoming}, total_outgoing={total_out}, premium_outgoing={premium_out}, ratio={ratio:.2f} (>=0.75: {ratio >= 0.75})")
            else:
                print(f"  Node {node}: no incoming flow, constraint not applicable")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No feasible solution found")
else:
    print("STATUS: unknown")
    print("Solver returned unknown")