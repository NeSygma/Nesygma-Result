from z3 import *

# Problem data
vertices = [0, 1, 2, 3, 4, 5]
edges = [(0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5), (1, 5)]

# Create solver
opt = Optimize()

# Decision variables: selected[v] = True if vertex v is in the cover
selected = [Bool(f'selected_{v}') for v in vertices]

# Objective: minimize the number of selected vertices
# Convert Bool to Int (1 if True, 0 if False) and sum
cover_size = Sum([If(selected[v], 1, 0) for v in vertices])
opt.minimize(cover_size)

# Constraint: every edge must be covered
for (u, v) in edges:
    # Edge (u,v) is covered if u is selected OR v is selected
    opt.add(Or(selected[u], selected[v]))

# Check and get solution
result = opt.check()

if result == sat:
    model = opt.model()
    
    # Extract selected vertices
    vertex_cover = []
    for v in vertices:
        if is_true(model[selected[v]]):
            vertex_cover.append(v)
    
    # Calculate cover size
    cover_size_val = len(vertex_cover)
    
    # Verify all edges are covered
    covered_edges = []
    all_covered = True
    for (u, v) in edges:
        u_selected = is_true(model[selected[u]])
        v_selected = is_true(model[selected[v]])
        if u_selected or v_selected:
            covered_edges.append([u, v])
        else:
            all_covered = False
    
    # Print results
    print("STATUS: sat")
    print(f"vertex_cover = {vertex_cover}")
    print(f"cover_size = {cover_size_val}")
    print(f"covered_edges = {covered_edges}")
    print(f"all_edges_covered = {all_covered}")
    
    # Verify it's optimal (expected size 3)
    if cover_size_val == 3:
        print("Optimal solution found: cover size = 3")
    else:
        print(f"Note: Found cover size = {cover_size_val}, expected 3")
        
elif result == unsat:
    print("STATUS: unsat")
    print("No vertex cover exists (should not happen for this graph)")
else:
    print("STATUS: unknown")