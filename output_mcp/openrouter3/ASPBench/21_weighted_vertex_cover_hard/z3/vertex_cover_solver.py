from z3 import *

# Problem data
vertices = list(range(16))
vertex_costs = {
    0: 1, 1: 1, 2: 3, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 
    8: 1, 9: 1, 10: 3, 11: 1, 12: 1, 13: 1, 14: 3, 15: 1
}

standard_edges = [(1,3), (1,4), (2,6), (3,7), (4,8), (5,11), (6,7), (7,12), (8,12), (11,13), (12,13), (13,14)]
heavy_edges = [(0,5), (9,10), (14,15)]
master_vertices = [0, 15]
antagonistic_pairs = [(1,2), (8,9)]

# Create solver
solver = Solver()

# Binary variables for vertex selection
selected = [Bool(f'selected_{v}') for v in vertices]

# Add cost variables for minimization
costs = [Int(f'cost_{v}') for v in vertices]
for v in vertices:
    solver.add(costs[v] == If(selected[v], vertex_costs[v], 0))

total_cost = Int('total_cost')
solver.add(total_cost == Sum(costs))

# Standard edge coverage: at least one endpoint selected
for u, v in standard_edges:
    solver.add(Or(selected[u], selected[v]))

# Heavy edge coverage: both endpoints OR master vertex exception
for u, v in heavy_edges:
    if u in master_vertices:
        # Master vertex u: can cover by selecting u alone OR both
        solver.add(Or(selected[u], And(selected[u], selected[v])))
    elif v in master_vertices:
        # Master vertex v: can cover by selecting v alone OR both
        solver.add(Or(selected[v], And(selected[u], selected[v])))
    else:
        # No master vertex: must select both
        solver.add(And(selected[u], selected[v]))

# Antagonistic pairs: at most one selected
for u, v in antagonistic_pairs:
    solver.add(Or(Not(selected[u]), Not(selected[v])))

# Minimize total cost
opt = Optimize()
opt.add([solver.assertions()[i] for i in range(len(solver.assertions()))])
opt.minimize(total_cost)

# Check and print results
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    selected_vertices = []
    for v in vertices:
        if is_true(model[selected[v]]):
            selected_vertices.append(v)
    
    total_cost_value = model[total_cost].as_long()
    
    print("STATUS: sat")
    print(f"vertex_cover: {sorted(selected_vertices)}")
    print(f"total_cost: {total_cost_value}")
    
    # Verify constraints
    print("\nVerification:")
    
    # Standard edges
    print("Standard edges coverage:")
    for u, v in standard_edges:
        covered = is_true(model[selected[u]]) or is_true(model[selected[v]])
        print(f"  ({u},{v}): {'✓' if covered else '✗'}")
    
    # Heavy edges
    print("Heavy edges coverage:")
    for u, v in heavy_edges:
        if u in master_vertices:
            covered = is_true(model[selected[u]])  # Master alone is sufficient
        elif v in master_vertices:
            covered = is_true(model[selected[v]])  # Master alone is sufficient
        else:
            covered = is_true(model[selected[u]]) and is_true(model[selected[v]])
        print(f"  ({u},{v}): {'✓' if covered else '✗'}")
    
    # Antagonistic pairs
    print("Antagonistic pairs:")
    for u, v in antagonistic_pairs:
        both_selected = is_true(model[selected[u]]) and is_true(model[selected[v]])
        print(f"  ({u},{v}): {'✗ (both selected)' if both_selected else '✓ (at most one)'}")
    
    # Expected optimal cost check
    if total_cost_value == 12:
        print(f"\n✓ Optimal cost achieved: {total_cost_value}")
    else:
        print(f"\n⚠ Cost {total_cost_value} differs from expected 12")
        
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")