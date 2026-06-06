from z3 import *
import itertools

# Define vertices, levels, costs, terminals
vertices = list(range(12))
levels = [2,2,1,1,1,1,0,0,0,0,0,0]
costs = [10,10,8,5,7,6,2,2,3,3,4,4]
terminals = [6,7,10,11]
terminal_set = set(terminals)

# Define edges: (u,v,weight,type)
edges = [
    (0,2,5,'fiber'),
    (1,3,4,'fiber'),
    (2,3,3,'fiber'),
    (2,4,6,'copper'),
    (2,6,2,'copper'),
    (3,5,2,'fiber'),
    (3,7,8,'copper'),
    (4,8,5,'fiber'),
    (5,9,4,'copper'),
    (5,10,3,'fiber'),
    (6,7,1,'copper'),
    (9,10,7,'fiber'),
    (10,11,2,'copper')
]

# Create solver
solver = Optimize()

# Declare variables
z = [Bool(f'z_{v}') for v in vertices]
y = [Bool(f'y_{i}') for i in range(len(edges))]
s = [Bool(f's_{i}') for i in range(len(edges))]

# Terminals are selected
for v in terminals:
    solver.add(z[v] == True)

# Edge selection implies vertex selection
for i, (u,v,_,_) in enumerate(edges):
    solver.add(Implies(y[i], z[u]))
    solver.add(Implies(y[i], z[v]))

# Vertex degree: sum of incident edges >= z[v]
for v in vertices:
    incident_edges = [i for i, (u,vv,_,_) in enumerate(edges) if u==v or vv==v]
    solver.add(Sum([If(y[i], 1, 0) for i in incident_edges]) >= If(z[v], 1, 0))

# Connectivity: cutset constraint with root=6
root = 6
all_vertices = set(vertices)
# Generate all non-empty subsets that do not contain root
for size in range(1, len(vertices)):
    for subset in itertools.combinations([v for v in vertices if v != root], size):
        S = set(subset)
        # Find crossing edges
        crossing_edges = []
        for i, (u,vv,_,_) in enumerate(edges):
            if (u in S and vv not in S) or (vv in S and u not in S):
                crossing_edges.append(i)
        if crossing_edges:
            condition = Or(Not(And([z[v] for v in S])), Or([y[i] for i in crossing_edges]))
            solver.add(condition)
        else:
            # No crossing edges: prevent S from being selected
            solver.add(Not(And([z[v] for v in S])))

# Hierarchy constraint
for i, (u,v,_,_) in enumerate(edges):
    solver.add(Implies(And(y[i], Not(terminal_set.__contains__(u))), levels[v] <= levels[u]))
    solver.add(Implies(And(y[i], Not(terminal_set.__contains__(v))), levels[u] <= levels[v]))

# Resource budget
resource_cost = Sum([If(Not(terminal_set.__contains__(v)), costs[v] * If(z[v], 1, 0), 0) for v in vertices])
solver.add(resource_cost <= 20)

# Edge type limit: copper edges
copper_edges = [i for i, (_,_,_,typ) in enumerate(edges) if typ == 'copper']
solver.add(Sum([If(y[i], 1, 0) for i in copper_edges]) <= 3)

# Gateway requirement
gateway_A = Or(y[4], y[6])  # edges 4 and 6
gateway_B = Or(y[9], y[11]) # edges 9 and 11
solver.add(gateway_A)
solver.add(gateway_B)

# Gateway connectivity: Steiner tree constraint
for i, (u,v,_,_) in enumerate(edges):
    solver.add(s[i] == And(y[i], Not(terminal_set.__contains__(u)), Not(terminal_set.__contains__(v))))

num_steiner_vertices = Sum([If(Not(terminal_set.__contains__(v)), If(z[v], 1, 0), 0) for v in vertices])
num_steiner_edges = Sum([If(s[i], 1, 0) for i in range(len(edges))])
solver.add(num_steiner_edges == num_steiner_vertices - 1)

# Overall tree constraint: edges = vertices - 1
total_edges = Sum([If(y[i], 1, 0) for i in range(len(edges))])
total_vertices = Sum([If(z[v], 1, 0) for v in vertices])
solver.add(total_edges == total_vertices - 1)

# Objective: minimize total weight
total_weight = Sum([edges[i][2] * If(y[i], 1, 0) for i in range(len(edges))])
solver.minimize(total_weight)

# Check
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Total weight:", model.eval(total_weight))
    # Print tree edges
    tree_edges = []
    for i, (u,v,w,_) in enumerate(edges):
        if is_true(model[y[i]]):
            tree_edges.append((u,v,w))
    print("Tree edges:", tree_edges)
    # Print Steiner vertices
    steiner_vertices = [v for v in vertices if v not in terminals and is_true(model[z[v]])]
    print("Steiner vertices:", steiner_vertices)
    # Print gateways
    gateways_A = []
    if is_true(model[y[4]]):
        gateways_A.append(2)
    if is_true(model[y[6]]):
        gateways_A.append(3)
    gateways_B = []
    if is_true(model[y[9]]):
        gateways_B.append(5)
    if is_true(model[y[11]]):
        gateways_B.append(9)
    print("Gateways A:", gateways_A)
    print("Gateways B:", gateways_B)
    # Print copper edge count
    copper_count = sum(1 for i in copper_edges if is_true(model[y[i]]))
    print("Copper edge count:", copper_count)
    # Print resource cost
    resource_cost_val = sum(costs[v] for v in steiner_vertices)
    print("Resource cost:", resource_cost_val)
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")