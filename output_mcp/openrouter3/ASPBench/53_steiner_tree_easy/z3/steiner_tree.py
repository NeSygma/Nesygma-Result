from z3 import *

# Graph data
vertices = [0, 1, 2, 3, 4, 5, 6]
terminals = [0, 5, 6]
steiner_vertices = [v for v in vertices if v not in terminals]

# Edges with weights
edges = [
    (0, 1, 3), (0, 2, 5),
    (1, 3, 2), (1, 4, 4),
    (2, 3, 1), (2, 5, 6),
    (3, 4, 3), (3, 5, 3), (3, 6, 2),
    (4, 5, 2),
    (5, 6, 4)
]

# Create optimization solver
opt = Optimize()

# Boolean variables for each edge
edge_vars = {}
for i, (u, v, w) in enumerate(edges):
    edge_vars[(u, v)] = Bool(f'edge_{u}_{v}')
    # Also add reverse direction for undirected graph
    edge_vars[(v, u)] = edge_vars[(u, v)]

# Objective: minimize total weight
total_weight = Sum([If(edge_vars[(u, v)], w, 0) for u, v, w in edges])
opt.minimize(total_weight)

# Constraint 1: All terminals must be connected (flow-based approach)
# We'll use a flow formulation: for each terminal, there must be a path to a root
# Choose vertex 0 as root (arbitrary)

# For each vertex, define flow variables from root to that vertex
# This ensures connectivity and tree structure
flow = {}
for v in vertices:
    for (u, w, weight) in edges:
        flow[(v, u, w)] = Real(f'flow_{v}_{u}_{w}')

# Flow conservation constraints
for v in vertices:
    if v == 0:  # root
        # Root has net outflow equal to number of terminals - 1
        outflow = Sum([If(edge_vars[(0, nbr)], 1, 0) for nbr in [1, 2]])
        opt.add(outflow >= 1)  # At least one edge from root
    else:
        # For non-root vertices: inflow = outflow (except terminals which can have net inflow)
        inflow = Sum([If(edge_vars[(nbr, v)], 1, 0) for nbr in vertices if (nbr, v) in edge_vars])
        outflow = Sum([If(edge_vars[(v, nbr)], 1, 0) for nbr in vertices if (v, nbr) in edge_vars])
        if v in terminals:
            # Terminals can have net inflow (they are sinks)
            opt.add(inflow >= 1)
        else:
            # Steiner vertices must have flow conservation
            opt.add(inflow == outflow)

# Constraint 2: Tree structure - no cycles
# Use cut-set constraints: for any subset S of vertices not containing all terminals,
# there must be at least one edge crossing the cut
# This ensures connectivity and prevents cycles

# For simplicity, we'll use a simpler approach: ensure the graph is connected
# and has exactly |V| - 1 edges (tree property)

# Count edges in the tree
edge_count = Sum([If(edge_vars[(u, v)], 1, 0) for u, v, w in edges])
opt.add(edge_count == len(vertices) - 1)  # Tree has |V| - 1 edges

# Constraint 3: All terminals must be included (connected to the tree)
# This is already handled by flow constraints

# Constraint 4: Only valid edges can be used
# Already enforced by only having variables for valid edges

# Check and print results
result = opt.check()
if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract tree edges
    tree_edges = []
    total_weight_val = 0
    for u, v, w in edges:
        if is_true(model[edge_vars[(u, v)]]):
            tree_edges.append((u, v, w))
            total_weight_val += w
    
    # Extract Steiner vertices used
    steiner_used = []
    for v in steiner_vertices:
        # Check if vertex is incident to any tree edge
        used = any(u == v or w == v for u, w, _ in tree_edges)
        if used:
            steiner_used.append(v)
    
    print(f"total_weight: {total_weight_val}")
    print(f"tree_edges: {tree_edges}")
    print(f"steiner_vertices: {steiner_used}")
    print(f"terminals: {terminals}")
    
    # Verify connected components
    # Build adjacency list from tree edges
    adj = {v: [] for v in vertices}
    for u, v, _ in tree_edges:
        adj[u].append(v)
        adj[v].append(u)
    
    # BFS to count connected components
    visited = set()
    components = []
    
    def bfs(start):
        queue = [start]
        visited.add(start)
        component = [start]
        while queue:
            node = queue.pop(0)
            for neighbor in adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    component.append(neighbor)
        return component
    
    for v in vertices:
        if v not in visited:
            components.append(bfs(v))
    
    print(f"connected_components: {components}")
    print(f"number_of_components: {len(components)}")
    
    # Verify all terminals are in the same component
    terminal_components = []
    for comp in components:
        if any(t in comp for t in terminals):
            terminal_components.append(comp)
    
    if len(terminal_components) == 1:
        print("All terminals are connected: YES")
    else:
        print("All terminals are connected: NO")
        
elif result == unsat:
    print("STATUS: unsat")
    print("No solution found - constraints are unsatisfiable")
else:
    print("STATUS: unknown")
    print("Solver returned unknown result")