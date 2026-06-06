from z3 import *

# Create optimizer
opt = Optimize()

# Define flow variables for each edge
f_1_2 = Int('f_1_2')  # 1 → 2
f_1_3 = Int('f_1_3')  # 1 → 3
f_2_3 = Int('f_2_3')  # 2 → 3
f_2_4 = Int('f_2_4')  # 2 → 4
f_3_4 = Int('f_3_4')  # 3 → 4
f_3_5 = Int('f_3_5')  # 3 → 5
f_4_6 = Int('f_4_6')  # 4 → 6
f_5_6 = Int('f_5_6')  # 5 → 6

# Total flow from source to sink
max_flow = Int('max_flow')

# Capacity constraints (0 ≤ flow ≤ capacity)
opt.add(f_1_2 >= 0, f_1_2 <= 10)
opt.add(f_1_3 >= 0, f_1_3 <= 8)
opt.add(f_2_3 >= 0, f_2_3 <= 5)
opt.add(f_2_4 >= 0, f_2_4 <= 7)
opt.add(f_3_4 >= 0, f_3_4 <= 3)
opt.add(f_3_5 >= 0, f_3_5 <= 9)
opt.add(f_4_6 >= 0, f_4_6 <= 8)
opt.add(f_5_6 >= 0, f_5_6 <= 6)

# Flow conservation at intermediate nodes
# Node 2: incoming = outgoing
opt.add(f_1_2 == f_2_3 + f_2_4)
# Node 3: incoming = outgoing
opt.add(f_1_3 + f_2_3 == f_3_4 + f_3_5)
# Node 4: incoming = outgoing
opt.add(f_2_4 + f_3_4 == f_4_6)
# Node 5: incoming = outgoing
opt.add(f_3_5 == f_5_6)

# Total flow from source (node 1) = sum of outgoing flows from source
opt.add(max_flow == f_1_2 + f_1_3)

# Total flow into sink (node 6) = sum of incoming flows to sink
opt.add(max_flow == f_4_6 + f_5_6)

# Maximize the total flow
opt.maximize(max_flow)

# Check and get result
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print(f"max_flow = {model[max_flow]}")
    print("flows:")
    print(f"  1 → 2: {model[f_1_2]}")
    print(f"  1 → 3: {model[f_1_3]}")
    print(f"  2 → 3: {model[f_2_3]}")
    print(f"  2 → 4: {model[f_2_4]}")
    print(f"  3 → 4: {model[f_3_4]}")
    print(f"  3 → 5: {model[f_3_5]}")
    print(f"  4 → 6: {model[f_4_6]}")
    print(f"  5 → 6: {model[f_5_6]}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")