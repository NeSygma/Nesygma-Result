from z3 import *

# ============================================================
# Circuit Definition
# ============================================================

# Gate definitions: (name, type, inputs, output_wire)
gates = [
    # Layer 1
    ("and1", "AND", ["in1", "in2"], "w1"),
    ("xor1", "XOR", ["in3", "in4"], "w2"),
    ("or1", "OR", ["in5", "in6"], "w3"),
    ("and2", "AND", ["in7", "in8"], "w4"),
    ("xor2", "XOR", ["in9", "in10"], "w5"),
    ("not1", "NOT", ["in1"], "w6"),
    ("or2", "OR", ["in3", "in5"], "w7"),
    ("and3", "AND", ["in4", "in6"], "w8"),
    # Layer 2
    ("and4", "AND", ["w1", "w2"], "w9"),
    ("or3", "OR", ["w3", "w4"], "w10"),
    ("xor4", "XOR", ["w5", "w6"], "w11"),
    ("and5", "AND", ["w2", "w7"], "w12"),
    ("or4", "OR", ["w8", "w5"], "w13"),
    ("not2", "NOT", ["w7"], "w14"),
    ("xor5", "XOR", ["w6", "w1"], "w15"),
    ("and6", "AND", ["w4", "w8"], "w16"),
    # Layer 3
    ("xor6", "XOR", ["w9", "w10"], "w17"),
    ("and7", "AND", ["w11", "w12"], "w18"),
    ("or5", "OR", ["w13", "w14"], "w19"),
    ("xor7", "XOR", ["w15", "w16"], "w20"),
    ("and8", "AND", ["w9", "w13"], "w21"),
    ("or6", "OR", ["w10", "w12"], "w22"),
    ("not3", "NOT", ["w11"], "w23"),
    ("xor8", "XOR", ["w14", "w16"], "w24"),
    # Layer 4
    ("and9", "AND", ["w17", "w18"], "w25"),
    ("or7", "OR", ["w19", "w20"], "w26"),
    ("xor9", "XOR", ["w21", "w22"], "w27"),
    ("and10", "AND", ["w23", "w24"], "w28"),
    ("or8", "OR", ["w25", "w26"], "w29"),
    ("xor10", "XOR", ["w27", "w28"], "w30"),
    ("and11", "AND", ["w22", "w24"], "w31"),
    ("or9", "OR", ["w21", "w23"], "w32"),
    # Final Stage
    ("xor11", "XOR", ["w29", "w30"], "u1"),
    ("and12", "AND", ["w31", "w32"], "u2"),
    ("or10", "OR", ["w17", "w29"], "u3"),
    ("not4", "NOT", ["u2"], "out2"),
    ("or11", "OR", ["u1", "u3"], "out1"),
    ("xor12", "XOR", ["w30", "w31"], "out3"),
]

# Test cases: (inputs_dict, observed_outputs_dict)
tests = [
    ({"in1":1,"in2":1,"in3":0,"in4":1,"in5":1,"in6":0,"in7":1,"in8":0,"in9":1,"in10":0}, {"out1":0,"out2":1,"out3":0}),
    ({"in1":0,"in2":1,"in3":1,"in4":0,"in5":1,"in6":1,"in7":0,"in8":1,"in9":1,"in10":1}, {"out1":0,"out2":1,"out3":0}),
    ({"in1":1,"in2":0,"in3":1,"in4":1,"in5":0,"in6":0,"in7":1,"in8":1,"in9":0,"in10":0}, {"out1":0,"out2":1,"out3":0}),
    ({"in1":0,"in2":0,"in3":0,"in4":1,"in5":1,"in6":1,"in7":1,"in8":0,"in9":0,"in10":1}, {"out1":0,"out2":1,"out3":0}),
    ({"in1":1,"in2":1,"in3":1,"in4":1,"in5":0,"in6":1,"in7":0,"in8":0,"in9":1,"in10":0}, {"out1":0,"out2":1,"out3":0}),
    ({"in1":0,"in2":1,"in3":0,"in4":0,"in5":1,"in6":0,"in7":1,"in8":1,"in9":0,"in10":1}, {"out1":0,"out2":1,"out3":0}),
    ({"in1":1,"in2":0,"in3":0,"in4":1,"in5":0,"in6":1,"in7":1,"in8":0,"in9":1,"in10":1}, {"out1":0,"out2":1,"out3":0}),
    ({"in1":0,"in2":0,"in3":1,"in4":0,"in5":1,"in6":0,"in7":0,"in8":1,"in9":1,"in10":0}, {"out1":0,"out2":1,"out3":0}),
]

# ============================================================
# Z3 Model
# ============================================================

opt = Optimize()

num_gates = len(gates)
num_tests = len(tests)

# Fault mode variables for each gate
# 0 = no fault, 1 = stuck0, 2 = stuck1, 3 = invert, 4 = open
fault_mode = [Int(f'fault_{i}') for i in range(num_gates)]
for i in range(num_gates):
    opt.add(fault_mode[i] >= 0, fault_mode[i] <= 4)

# Boolean: is gate i faulty?
is_faulty = [Bool(f'is_faulty_{i}') for i in range(num_gates)]
for i in range(num_gates):
    opt.add(is_faulty[i] == (fault_mode[i] != 0))
    opt.add(Implies(Not(is_faulty[i]), fault_mode[i] == 0))

# At most 3 faulty gates
opt.add(Sum([If(is_faulty[i], 1, 0) for i in range(num_gates)]) <= 3)

# Cost: stuck0=1, stuck1=1, invert=1, open=2
cost_per_gate = [If(fault_mode[i] == 0, 0,
                If(fault_mode[i] == 4, 2, 1)) for i in range(num_gates)]
total_cost = Sum(cost_per_gate)

# Wire values: for each test t, each wire w
# Collect all wire names
all_wires = set()
for gname, gtype, ginputs, goutput in gates:
    all_wires.add(goutput)
    for inp in ginputs:
        all_wires.add(inp)
# Add primary outputs explicitly
all_wires.update(["out1", "out2", "out3", "u1", "u2", "u3"])

# Create wire variables for each test
wire = {}
for t in range(num_tests):
    for w in all_wires:
        wire[(t, w)] = Bool(f'w_{t}_{w}')

# Set primary inputs for each test
for t in range(num_tests):
    for inp_name, inp_val in tests[t][0].items():
        opt.add(wire[(t, inp_name)] == (inp_val == 1))

# Gate evaluation constraints for each test
for g_idx, (gname, gtype, ginputs, goutput) in enumerate(gates):
    for t in range(num_tests):
        # Compute correct output based on gate type
        if gtype == "AND":
            correct = And(wire[(t, ginputs[0])], wire[(t, ginputs[1])])
        elif gtype == "OR":
            correct = Or(wire[(t, ginputs[0])], wire[(t, ginputs[1])])
        elif gtype == "XOR":
            correct = Xor(wire[(t, ginputs[0])], wire[(t, ginputs[1])])
        elif gtype == "NOT":
            correct = Not(wire[(t, ginputs[0])])
        
        # Apply fault mode
        fm = fault_mode[g_idx]
        
        # no fault: output = correct
        opt.add(Implies(fm == 0, wire[(t, goutput)] == correct))
        # stuck0: output = False
        opt.add(Implies(fm == 1, wire[(t, goutput)] == False))
        # stuck1: output = True
        opt.add(Implies(fm == 2, wire[(t, goutput)] == True))
        # invert: output = NOT(correct)
        opt.add(Implies(fm == 3, wire[(t, goutput)] == Not(correct)))
        # open: output is unconstrained (free Bool) - no constraint added

# Observed output constraints
for t in range(num_tests):
    for out_name, out_val in tests[t][1].items():
        opt.add(wire[(t, out_name)] == (out_val == 1))

# Minimize total cost
opt.minimize(total_cost)

# ============================================================
# Solve
# ============================================================

result = opt.check()
if result == sat:
    m = opt.model()
    print("STATUS: sat")
    
    # Extract fault details
    faults_found = []
    total_c = 0
    for i in range(num_gates):
        fm_val = m.evaluate(fault_mode[i]).as_long()
        if fm_val != 0:
            mode_name = {1: "stuck0", 2: "stuck1", 3: "invert", 4: "open"}[fm_val]
            c = 2 if fm_val == 4 else 1
            total_c += c
            faults_found.append((gates[i][0], mode_name, c))
    
    print(f"Total cost: {total_c}")
    print(f"Number of faulty gates: {len(faults_found)}")
    print("Faults:")
    for gname, mode, c in faults_found:
        print(f"  {gname}: {mode} (cost={c})")
    
    # Verify outputs for a couple of tests
    print("\nVerification (test 1 outputs):")
    t = 0
    for out in ["out1", "out2", "out3"]:
        val = m.evaluate(wire[(t, out)])
        print(f"  {out} = {val}")
    
    print("\nVerification (test 2 outputs):")
    t = 1
    for out in ["out1", "out2", "out3"]:
        val = m.evaluate(wire[(t, out)])
        print(f"  {out} = {val}")
    
    # Print diagnosis
    print(f"\nMinimal: True")
    print(f"Explanation: Found minimum-cost diagnosis with {len(faults_found)} fault(s) at total cost {total_c}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No valid diagnosis found within constraints")
else:
    print("STATUS: unknown")
    print("Solver returned unknown")