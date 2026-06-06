from z3 import *

opt = Optimize()

# Flow variables for each edge
f_1_2 = Int('f_1_2')
f_1_3 = Int('f_1_3')
f_2_3 = Int('f_2_3')
f_2_4 = Int('f_2_4')
f_3_4 = Int('f_3_4')
f_3_5 = Int('f_3_5')
f_4_6 = Int('f_4_6')
f_5_6 = Int('f_5_6')

# Capacity constraints
opt.add(f_1_2 >= 0, f_1_2 <= 10)
opt.add(f_1_3 >= 0, f_1_3 <= 8)
opt.add(f_2_3 >= 0, f_2_3 <= 5)
opt.add(f_2_4 >= 0, f_2_4 <= 7)
opt.add(f_3_4 >= 0, f_3_4 <= 3)
opt.add(f_3_5 >= 0, f_3_5 <= 9)
opt.add(f_4_6 >= 0, f_4_6 <= 8)
opt.add(f_5_6 >= 0, f_5_6 <= 6)

# Flow conservation at intermediate nodes (2,3,4,5)
# Node 2: inflow = f_1_2, outflow = f_2_3 + f_2_4
opt.add(f_1_2 == f_2_3 + f_2_4)
# Node 3: inflow = f_1_3 + f_2_3, outflow = f_3_4 + f_3_5
opt.add(f_1_3 + f_2_3 == f_3_4 + f_3_5)
# Node 4: inflow = f_2_4 + f_3_4, outflow = f_4_6
opt.add(f_2_4 + f_3_4 == f_4_6)
# Node 5: inflow = f_3_5, outflow = f_5_6
opt.add(f_3_5 == f_5_6)

# Objective: maximize flow into sink (edges into node 6)
opt.maximize(f_4_6 + f_5_6)

# Solve
result = opt.check()
if result == sat:
    print("STATUS: sat")
    m = opt.model()
    # Print total max flow
    print("max_flow =", m.eval(f_4_6 + f_5_6))
    # Print each flow variable
    print("flow_1_2 =", m.eval(f_1_2))
    print("flow_1_3 =", m.eval(f_1_3))
    print("flow_2_3 =", m.eval(f_2_3))
    print("flow_2_4 =", m.eval(f_2_4))
    print("flow_3_4 =", m.eval(f_3_4))
    print("flow_3_5 =", m.eval(f_3_5))
    print("flow_4_6 =", m.eval(f_4_6))
    print("flow_5_6 =", m.eval(f_5_6))
else:
    print("STATUS: unsat")