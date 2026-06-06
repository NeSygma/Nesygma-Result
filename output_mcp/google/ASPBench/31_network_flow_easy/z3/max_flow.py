from z3 import *

# Create an optimization solver
opt = Optimize()

# Define flow variables for each edge
f12 = Int('f12')
f13 = Int('f13')
f23 = Int('f23')
f24 = Int('f24')
f34 = Int('f34')
f35 = Int('f35')
f46 = Int('f46')
f56 = Int('f56')

# Capacity constraints
opt.add(f12 >= 0, f12 <= 10)
opt.add(f13 >= 0, f13 <= 8)
opt.add(f23 >= 0, f23 <= 5)
opt.add(f24 >= 0, f24 <= 7)
opt.add(f34 >= 0, f34 <= 3)
opt.add(f35 >= 0, f35 <= 9)
opt.add(f46 >= 0, f46 <= 8)
opt.add(f56 >= 0, f56 <= 6)

# Flow conservation constraints
# Node 2: In(1,2) = Out(2,3) + Out(2,4)
opt.add(f12 == f23 + f24)
# Node 3: In(1,3) + In(2,3) = Out(3,4) + Out(3,5)
opt.add(f13 + f23 == f34 + f35)
# Node 4: In(2,4) + In(3,4) = Out(4,6)
opt.add(f24 + f34 == f46)
# Node 5: In(3,5) = Out(5,6)
opt.add(f35 == f56)

# Objective: Maximize total flow out of source (1)
total_flow = f12 + f13
opt.maximize(total_flow)

# Solve
if opt.check() == sat:
    m = opt.model()
    print("STATUS: sat")
    print(f"max_flow = {m.evaluate(total_flow)}")
    print("flows = [")
    print(f"  {{'from': 1, 'to': 2, 'flow': {m[f12]}}},")
    print(f"  {{'from': 1, 'to': 3, 'flow': {m[f13]}}},")
    print(f"  {{'from': 2, 'to': 3, 'flow': {m[f23]}}},")
    print(f"  {{'from': 2, 'to': 4, 'flow': {m[f24]}}},")
    print(f"  {{'from': 3, 'to': 4, 'flow': {m[f34]}}},")
    print(f"  {{'from': 3, 'to': 5, 'flow': {m[f35]}}},")
    print(f"  {{'from': 4, 'to': 6, 'flow': {m[f46]}}},")
    print(f"  {{'from': 5, 'to': 6, 'flow': {m[f56]}}}")
    print("]")
else:
    print("STATUS: unsat")