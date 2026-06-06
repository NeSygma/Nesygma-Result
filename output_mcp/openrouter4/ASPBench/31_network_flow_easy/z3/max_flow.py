from z3 import *

# Create optimizer
opt = Optimize()

# Edge flow variables (all non-negative reals for flow)
f12 = Real('f_1_2')
f13 = Real('f_1_3')
f23 = Real('f_2_3')
f24 = Real('f_2_4')
f34 = Real('f_3_4')
f35 = Real('f_3_5')
f46 = Real('f_4_6')
f56 = Real('f_5_6')

# List all flow variables for convenience
flows = [f12, f13, f23, f24, f34, f35, f46, f56]

# Edge capacities
caps = {
    f12: 10,
    f13: 8,
    f23: 5,
    f24: 7,
    f34: 3,
    f35: 9,
    f46: 8,
    f56: 6
}

# Capacity constraints and non-negativity
for f in flows:
    opt.add(f >= 0)
    opt.add(f <= caps[f])

# Flow conservation at intermediate nodes (2, 3, 4, 5)

# Node 2: inflow from 1, outflow to 3 and 4
opt.add(f12 == f23 + f24)

# Node 3: inflow from 1 and 2, outflow to 4 and 5
opt.add(f13 + f23 == f34 + f35)

# Node 4: inflow from 2 and 3, outflow to 6
opt.add(f24 + f34 == f46)

# Node 5: inflow from 3, outflow to 6
opt.add(f35 == f56)

# Objective: maximize total flow from source (node 1)
# Total flow out of source = f12 + f13
total_flow = f12 + f13
opt.maximize(total_flow)

BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    max_flow_val = float(m.eval(total_flow).as_decimal(10))
    print("STATUS: sat")
    print(f"max_flow = {round(max_flow_val)}")
    print("flows:")
    print(f"  {{'from': 1, 'to': 2, 'flow': {float(m.eval(f12).as_decimal(10))}}}")
    print(f"  {{'from': 1, 'to': 3, 'flow': {float(m.eval(f13).as_decimal(10))}}}")
    print(f"  {{'from': 2, 'to': 3, 'flow': {float(m.eval(f23).as_decimal(10))}}}")
    print(f"  {{'from': 2, 'to': 4, 'flow': {float(m.eval(f24).as_decimal(10))}}}")
    print(f"  {{'from': 3, 'to': 4, 'flow': {float(m.eval(f34).as_decimal(10))}}}")
    print(f"  {{'from': 3, 'to': 5, 'flow': {float(m.eval(f35).as_decimal(10))}}}")
    print(f"  {{'from': 4, 'to': 6, 'flow': {float(m.eval(f46).as_decimal(10))}}}")
    print(f"  {{'from': 5, 'to': 6, 'flow': {float(m.eval(f56).as_decimal(10))}}}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")