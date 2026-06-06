from z3 import *

# Define vertices 1..24
verts = list(range(1, 25))
# Bool variable for each vertex
in_set = {v: Bool(f"v{v}") for v in verts}

# Edge list
edges = [(1,2), (1,4), (1,10), (1,17), (2,5), (2,9), (3,6), (4,7), (5,8), (6,7), (8,16), (8,24), (9,10), (9,12), (9,17), (10,14), (11,15), (12,16), (13,14), (16,24), (17,18), (17,20), (18,19), (18,21), (19,22), (20,23), (21,24)]

# Types
core = {1,9,17}
support = {2,3,10,11,18,19}
peripheral = {4,5,6,7,8,12,13,14,15,16,20,21,22,23,24}

# Zones mapping
zone1 = set(range(1,9))
zone2 = set(range(9,17))
zone3 = set(range(17,25))

# Helper to get zone of vertex
def zone(v):
    if v in zone1: return 1
    if v in zone2: return 2
    return 3

# Build optimizer
opt = Optimize()

# 1. Independence constraints
for (u,v) in edges:
    opt.add(Or(Not(in_set[u]), Not(in_set[v])))

# 2. Core count limit <=2
core_count = Sum([If(in_set[v], 1, 0) for v in core])
opt.add(core_count <= 2)

# 3. Core-Support Dependency
# For each core, at least one support in same zone
support_by_zone = {
    1: [v for v in support if zone(v)==1],
    2: [v for v in support if zone(v)==2],
    3: [v for v in support if zone(v)==3]
}
for c in core:
    z = zone(c)
    supp_in_zone = support_by_zone[z]
    # At least one support selected if core selected
    opt.add(Implies(in_set[c], Or([in_set[s] for s in supp_in_zone])))

# 4. Conditional Zone Exclusion
periph_zone1 = [v for v in peripheral if zone(v)==1]
zone3_verts = [v for v in verts if zone(v)==3]
opt.add(Implies(Or([in_set[v] for v in periph_zone1]), And([Not(in_set[v]) for v in zone3_verts])))

# 5. Peripheral headcount <= core count
periph_count = Sum([If(in_set[v], 1, 0) for v in peripheral])
opt.add(periph_count <= core_count)

# Objective: maximize total selected
total = Sum([If(in_set[v], 1, 0) for v in verts])
opt.maximize(total)

# Solve
if opt.check() == sat:
    m = opt.model()
    selected = [v for v in verts if is_true(m.eval(in_set[v]))]
    selected.sort()
    core_sel = sorted([v for v in selected if v in core])
    supp_sel = sorted([v for v in selected if v in support])
    periph_sel = sorted([v for v in selected if v in peripheral])
    print("STATUS: sat")
    print("size =", len(selected))
    print("independent_set =", selected)
    print("core_vertices =", core_sel)
    print("support_vertices =", supp_sel)
    print("peripheral_vertices =", periph_sel)
    print("core_count =", len(core_sel))
    print("support_count =", len(supp_sel))
    print("peripheral_count =", len(periph_sel))
else:
    print("STATUS: unsat")