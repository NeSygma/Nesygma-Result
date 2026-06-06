from z3 import *

# Vertices
vertices = list(range(16))  # 0..15

# Costs
cost = {}
for v in vertices:
    if v in [2, 10, 14]:
        cost[v] = 3
    else:
        cost[v] = 1

# Standard edges
standard_edges = [
    (1,3), (1,4), (2,6), (3,7), (4,8), (5,11),
    (6,7), (7,12), (8,12), (11,13), (12,13), (13,14)
]

# Heavy edges
heavy_edges = [
    (0,5), (9,10), (14,15)
]

# Master vertices
masters = {0, 15}

# Antagonistic pairs
antagonistic = [(1,2), (8,9)]

# Decision variables: selected[v] = True if vertex v is in the cover
selected = {v: Bool(f'sel_{v}') for v in vertices}

opt = Optimize()

# Objective: minimize total cost
total_cost = Sum([If(selected[v], cost[v], 0) for v in vertices])
opt.minimize(total_cost)

# Constraint 1: Standard edge coverage - at least one endpoint selected
for (u, v) in standard_edges:
    opt.add(Or(selected[u], selected[v]))

# Constraint 2: Heavy edge coverage
for (u, v) in heavy_edges:
    u_is_master = u in masters
    v_is_master = v in masters
    
    if u_is_master and v_is_master:
        # Both are masters: selecting either one suffices
        opt.add(Or(selected[u], selected[v]))
    elif u_is_master:
        # u is master: selecting u alone suffices, or both
        # Selecting only v (without u) does NOT cover
        # Covered if: selected[u] OR (selected[u] AND selected[v])
        # Simplifies to: selected[u]
        # Wait, let me re-read: "selecting only the master vertex is sufficient"
        # So covered if: selected[u] (master alone) OR (selected[u] AND selected[v]) (both)
        # Which simplifies to: selected[u]
        # But what about selecting both? That's also covered.
        # Actually: covered = selected[u] OR (selected[u] AND selected[v]) = selected[u]
        # But we also need to handle: what if only v is selected? That does NOT cover.
        # So the constraint is: selected[u] must be true (since only master alone or both work)
        # Wait, re-reading more carefully:
        # "If a heavy edge has a master vertex as an endpoint, selecting only the master vertex is sufficient"
        # General rule: both endpoints needed
        # Exception: if master is endpoint, just master suffices
        # So: covered if (both selected) OR (master selected alone)
        # = selected[u] AND selected[v]) OR selected[u] = selected[u]
        opt.add(selected[u])
    elif v_is_master:
        opt.add(selected[v])
    else:
        # No master: both endpoints must be selected
        opt.add(And(selected[u], selected[v]))

# Constraint 3: Antagonistic pairs - at most one selected
for (u, v) in antagonistic:
    opt.add(Not(And(selected[u], selected[v])))

# Solve
result = opt.check()

if result == sat:
    m = opt.model()
    cover = sorted([v for v in vertices if m.evaluate(selected[v], model_completion=True)])
    total = sum(cost[v] for v in cover)
    print("STATUS: sat")
    print(f"vertex_cover = {cover}")
    print(f"total_cost = {total}")
    
    # Verify constraints
    print("\n--- Verification ---")
    print(f"Cover size: {len(cover)}")
    print(f"Total cost: {total}")
    
    # Check standard edges
    for (u,v) in standard_edges:
        assert u in cover or v in cover, f"Standard edge ({u},{v}) not covered!"
    print("All standard edges covered: OK")
    
    # Check heavy edges
    for (u,v) in heavy_edges:
        u_sel = u in cover
        v_sel = v in cover
        u_master = u in masters
        v_master = v in masters
        if u_master and not v_master:
            assert u_sel, f"Heavy edge ({u},{v}): master {u} not selected!"
        elif v_master and not u_master:
            assert v_sel, f"Heavy edge ({u},{v}): master {v} not selected!"
        elif u_master and v_master:
            assert u_sel or v_sel, f"Heavy edge ({u},{v}): no master selected!"
        else:
            assert u_sel and v_sel, f"Heavy edge ({u},{v}): not both selected!"
    print("All heavy edges covered: OK")
    
    # Check antagonistic
    for (u,v) in antagonistic:
        assert not (u in cover and v in cover), f"Antagonistic pair ({u},{v}) both selected!"
    print("Antagonistic pairs respected: OK")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No valid vertex cover exists.")
else:
    print("STATUS: unknown")