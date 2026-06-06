from z3 import *

# Circuit definition
gates = [
    ("and1", "AND", ["in1", "in2"], "w1"),
    ("xor1", "XOR", ["in3", "in4"], "w2"),
    ("or1", "OR", ["in5", "in6"], "w3"),
    ("and2", "AND", ["in7", "in8"], "w4"),
    ("xor2", "XOR", ["in9", "in10"], "w5"),
    ("not1", "NOT", ["in1"], "w6"),
    ("or2", "OR", ["in3", "in5"], "w7"),
    ("and3", "AND", ["in4", "in6"], "w8"),
    ("and4", "AND", ["w1", "w2"], "w9"),
    ("or3", "OR", ["w3", "w4"], "w10"),
    ("xor4", "XOR", ["w5", "w6"], "w11"),
    ("and5", "AND", ["w2", "w7"], "w12"),
    ("or4", "OR", ["w8", "w5"], "w13"),
    ("not2", "NOT", ["w7"], "w14"),
    ("xor5", "XOR", ["w6", "w1"], "w15"),
    ("and6", "AND", ["w4", "w8"], "w16"),
    ("xor6", "XOR", ["w9", "w10"], "w17"),
    ("and7", "AND", ["w11", "w12"], "w18"),
    ("or5", "OR", ["w13", "w14"], "w19"),
    ("xor7", "XOR", ["w15", "w16"], "w20"),
    ("and8", "AND", ["w9", "w13"], "w21"),
    ("or6", "OR", ["w10", "w12"], "w22"),
    ("not3", "NOT", ["w11"], "w23"),
    ("xor8", "XOR", ["w14", "w16"], "w24"),
    ("and9", "AND", ["w17", "w18"], "w25"),
    ("or7", "OR", ["w19", "w20"], "w26"),
    ("xor9", "XOR", ["w21", "w22"], "w27"),
    ("and10", "AND", ["w23", "w24"], "w28"),
    ("or8", "OR", ["w25", "w26"], "w29"),
    ("xor10", "XOR", ["w27", "w28"], "w30"),
    ("and11", "AND", ["w22", "w24"], "w31"),
    ("or9", "OR", ["w21", "w23"], "w32"),
    ("xor11", "XOR", ["w29", "w30"], "u1"),
    ("and12", "AND", ["w31", "w32"], "u2"),
    ("or10", "OR", ["w17", "w29"], "u3"),
    ("not4", "NOT", ["u2"], "out2"),
    ("or11", "OR", ["u1", "u3"], "out1"),
    ("xor12", "XOR", ["w30", "w31"], "out3")
]

# 8 test cases
test_cases = [
    [1, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 0, 1, 1, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 1, 1, 0, 1, 1],
    [0, 0, 1, 0, 1, 0, 0, 1, 1, 0]
]
observed_outputs = [0, 1, 0] # out1, out2, out3

# Fault modes: 0: None, 1: stuck0, 2: stuck1, 3: invert, 4: open
# Costs: None:0, stuck0:1, stuck1:1, invert:1, open:2
opt = Optimize()

# Variables
# fault_mode[gate_idx]
fault_modes = [Int(f"mode_{g[0]}") for g in gates]
for m in fault_modes:
    opt.add(m >= 0, m <= 4)

# Wire values: wire_val[wire_name][test_idx]
all_wires = ["in1", "in2", "in3", "in4", "in5", "in6", "in7", "in8", "in9", "in10",
             "w1", "w2", "w3", "w4", "w5", "w6", "w7", "w8", "w9", "w10",
             "w11", "w12", "w13", "w14", "w15", "w16", "w17", "w18", "w19", "w20",
             "w21", "w22", "w23", "w24", "w25", "w26", "w27", "w28", "w29", "w30",
             "w31", "w32", "u1", "u2", "u3", "out1", "out2", "out3"]
wire_vals = {w: [Bool(f"{w}_{t}") for t in range(8)] for w in all_wires}

# Input values
for t in range(8):
    for i in range(10):
        opt.add(wire_vals[f"in{i+1}"][t] == (test_cases[t][i] == 1))

# Gate logic
for g_idx, (name, gtype, inputs, output) in enumerate(gates):
    for t in range(8):
        # Correct logic
        in_vals = [wire_vals[i][t] for i in inputs]
        if gtype == "AND":
            correct = And(*in_vals)
        elif gtype == "OR":
            correct = Or(*in_vals)
        elif gtype == "XOR":
            # XOR of multiple inputs: parity
            correct = Xor(*in_vals)
        elif gtype == "NOT":
            correct = Not(in_vals[0])
        
        # Actual logic with fault
        mode = fault_modes[g_idx]
        actual = wire_vals[output][t]
        
        # Fault mode constraints
        # 0: None, 1: stuck0, 2: stuck1, 3: invert, 4: open
        opt.add(If(mode == 0, actual == correct,
                If(mode == 1, actual == False,
                If(mode == 2, actual == True,
                If(mode == 3, actual == Not(correct),
                True))))) # open: no constraint on actual

# Output constraints
for t in range(8):
    opt.add(wire_vals["out1"][t] == (observed_outputs[0] == 1))
    opt.add(wire_vals["out2"][t] == (observed_outputs[1] == 1))
    opt.add(wire_vals["out3"][t] == (observed_outputs[2] == 1))

# Fault budget
faulty_gates = [If(m != 0, 1, 0) for m in fault_modes]
opt.add(Sum(faulty_gates) <= 3)

# Cost
costs = [If(m == 0, 0, If(m == 4, 2, 1)) for m in fault_modes]
opt.minimize(Sum(costs))

if opt.check() == sat:
    m = opt.model()
    print("STATUS: sat")
    total_cost = 0
    for i, g in enumerate(gates):
        mode = m[fault_modes[i]].as_long()
        if mode != 0:
            cost = 2 if mode == 4 else 1
            total_cost += cost
            print(f"{g[0]}: mode={mode}, cost={cost}")
    print(f"Total cost: {total_cost}")
else:
    print("STATUS: unsat")