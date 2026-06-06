from z3 import *

# Create optimizer
opt = Optimize()

# Flow variables for each edge
f12 = Int('f12')  # (1,2) standard
f13 = Int('f13')  # (1,3) premium
f24 = Int('f24')  # (2,4) standard
f25 = Int('f25')  # (2,5) premium
f34 = Int('f34')  # (3,4) standard
f36 = Int('f36')  # (3,6) premium
f47 = Int('f47')  # (4,7) standard
f57 = Int('f57')  # (5,7) premium
f68 = Int('f68')  # (6,8) premium
f78 = Int('f78')  # (7,8) standard

# All flows must be non-negative integers
flows = [f12, f13, f24, f25, f34, f36, f47, f57, f68, f78]
for f in flows:
    opt.add(f >= 0)

# 1. Capacity constraints
opt.add(f12 <= 10)
opt.add(f13 <= 12)
opt.add(f24 <= 8)
opt.add(f25 <= 4)
opt.add(f34 <= 5)
opt.add(f36 <= 10)
opt.add(f47 <= 10)
opt.add(f57 <= 7)
opt.add(f68 <= 12)
opt.add(f78 <= 15)

# 2. Flow conservation at intermediate nodes
# Node 2: incoming = f12, outgoing = f24 + f25
opt.add(f12 == f24 + f25)

# Node 3: incoming = f13, outgoing = f34 + f36
opt.add(f13 == f34 + f36)

# Node 4: incoming = f24 + f34, outgoing = f47
opt.add(f24 + f34 == f47)

# Node 5: incoming = f25, outgoing = f57
opt.add(f25 == f57)

# Node 6: incoming = f36, outgoing = f68
opt.add(f36 == f68)

# Node 7: incoming = f47 + f57, outgoing = f78
opt.add(f47 + f57 == f78)

# 3. Budget constraint: sum(flow * cost) <= 100
# (1,2):2, (1,3):4, (2,4):1, (2,5):3, (3,4):3, (3,6):5, (4,7):2, (5,7):4, (6,8):2, (7,8):1
total_cost = (2*f12 + 4*f13 + 1*f24 + 3*f25 + 3*f34 + 5*f36 + 2*f47 + 4*f57 + 2*f68 + 1*f78)
opt.add(total_cost <= 100)

# 4. Priority Node Rule - Node 3
# If node 3 has incoming flow (f13 > 0), then at least 75% of outgoing flow must be premium
# Premium outgoing from node 3 = f36, total outgoing = f34 + f36
# f36 >= 0.75 * (f34 + f36) => 4*f36 >= 3*f34 + 3*f36 => f36 >= 3*f34
opt.add(Implies(f13 > 0, f36 >= 3 * f34))

# Priority Node Rule - Node 5
# If node 5 has incoming flow (f25 > 0), then at least 75% of outgoing flow must be premium
# Premium outgoing from node 5 = f57, total outgoing = f57 (only outgoing edge)
# f57 >= 0.75 * f57 always holds for f57 >= 0
# So this constraint is automatically satisfied. No need to add anything.

# 5. Flow Balancing: total standard flow >= 0.5 * total premium flow
# Standard edges: (1,2), (2,4), (3,4), (4,7), (7,8)
# Premium edges: (1,3), (2,5), (3,6), (5,7), (6,8)
total_standard = f12 + f24 + f34 + f47 + f78
total_premium = f13 + f25 + f36 + f57 + f68
opt.add(2 * total_standard >= total_premium)

# Objective: Maximize total flow from source to sink
# Total flow = flow out of source = f12 + f13 = flow into sink = f68 + f78
total_flow = f12 + f13
opt.maximize(total_flow)

# Solve
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    print(f"max_flow = {m.eval(total_flow)}")
    print(f"f12 (1->2, std) = {m.eval(f12)}")
    print(f"f13 (1->3, prem) = {m.eval(f13)}")
    print(f"f24 (2->4, std) = {m.eval(f24)}")
    print(f"f25 (2->5, prem) = {m.eval(f25)}")
    print(f"f34 (3->4, std) = {m.eval(f34)}")
    print(f"f36 (3->6, prem) = {m.eval(f36)}")
    print(f"f47 (4->7, std) = {m.eval(f47)}")
    print(f"f57 (5->7, prem) = {m.eval(f57)}")
    print(f"f68 (6->8, prem) = {m.eval(f68)}")
    print(f"f78 (7->8, std) = {m.eval(f78)}")
    print(f"total_cost = {m.eval(total_cost)}")
    print(f"total_standard = {m.eval(total_standard)}")
    print(f"total_premium = {m.eval(total_premium)}")
    
    # Build flows array output
    print("\nflows = [")
    print(f"  {{'from': 1, 'to': 2, 'flow': {m.eval(f12)}}},")
    print(f"  {{'from': 1, 'to': 3, 'flow': {m.eval(f13)}}},")
    print(f"  {{'from': 2, 'to': 4, 'flow': {m.eval(f24)}}},")
    print(f"  {{'from': 2, 'to': 5, 'flow': {m.eval(f25)}}},")
    print(f"  {{'from': 3, 'to': 4, 'flow': {m.eval(f34)}}},")
    print(f"  {{'from': 3, 'to': 6, 'flow': {m.eval(f36)}}},")
    print(f"  {{'from': 4, 'to': 7, 'flow': {m.eval(f47)}}},")
    print(f"  {{'from': 5, 'to': 7, 'flow': {m.eval(f57)}}},")
    print(f"  {{'from': 6, 'to': 8, 'flow': {m.eval(f68)}}},")
    print(f"  {{'from': 7, 'to': 8, 'flow': {m.eval(f78)}}}")
    print("]")
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")