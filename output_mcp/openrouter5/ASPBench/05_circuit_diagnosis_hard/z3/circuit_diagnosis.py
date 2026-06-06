from z3 import *

# We have 38 gates (not 46 - the problem says 46 but lists 38).
# Let me recount from the problem statement:
# Layer 1: and1, xor1, or1, and2, xor2, not1, or2, and3 = 8
# Layer 2: and4, or3, xor4, and5, or4, not2, xor5, and6 = 8
# Layer 3: xor6, and7, or5, xor7, and8, or6, not3, xor8 = 8
# Layer 4: and9, or7, xor9, and10, or8, xor10, and11, or9 = 8
# Final: xor11, and12, or10, not4, or11, xor12 = 6
# Total = 38

NUM_GATES = 38
NUM_TESTS = 8

# Gate names
gate_names = [
    # Layer 1 (0-7)
    "and1","xor1","or1","and2","xor2","not1","or2","and3",
    # Layer 2 (8-15)
    "and4","or3","xor4","and5","or4","not2","xor5","and6",
    # Layer 3 (16-23)
    "xor6","and7","or5","xor7","and8","or6","not3","xor8",
    # Layer 4 (24-31)
    "and9","or7","xor9","and10","or8","xor10","and11","or9",
    # Final Stage (32-37)
    "xor11","and12","or10","not4","or11","xor12"
]

# Wire names (output of each gate)
wire_names = [
    "w1","w2","w3","w4","w5","w6","w7","w8",
    "w9","w10","w11","w12","w13","w14","w15","w16",
    "w17","w18","w19","w20","w21","w22","w23","w24",
    "w25","w26","w27","w28","w29","w30","w31","w32",
    "u1","u2","u3","out2","out1","out3"
]

# Gate info: (type, [input_names])
gate_info = [
    # Layer 1 (0-7)
    ("AND", ["in1","in2"]),      # and1 -> w1
    ("XOR", ["in3","in4"]),      # xor1 -> w2
    ("OR",  ["in5","in6"]),      # or1 -> w3
    ("AND", ["in7","in8"]),      # and2 -> w4
    ("XOR", ["in9","in10"]),     # xor2 -> w5
    ("NOT", ["in1"]),            # not1 -> w6
    ("OR",  ["in3","in5"]),      # or2 -> w7
    ("AND", ["in4","in6"]),      # and3 -> w8
    # Layer 2 (8-15)
    ("AND", ["w1","w2"]),        # and4 -> w9
    ("OR",  ["w3","w4"]),        # or3 -> w10
    ("XOR", ["w5","w6"]),        # xor4 -> w11
    ("AND", ["w2","w7"]),        # and5 -> w12
    ("OR",  ["w8","w5"]),        # or4 -> w13
    ("NOT", ["w7"]),             # not2 -> w14
    ("XOR", ["w6","w1"]),        # xor5 -> w15
    ("AND", ["w4","w8"]),        # and6 -> w16
    # Layer 3 (16-23)
    ("XOR", ["w9","w10"]),       # xor6 -> w17
    ("AND", ["w11","w12"]),      # and7 -> w18
    ("OR",  ["w13","w14"]),      # or5 -> w19
    ("XOR", ["w15","w16"]),      # xor7 -> w20
    ("AND", ["w9","w13"]),       # and8 -> w21
    ("OR",  ["w10","w12"]),      # or6 -> w22
    ("NOT", ["w11"]),            # not3 -> w23
    ("XOR", ["w14","w16"]),      # xor8 -> w24
    # Layer 4 (24-31)
    ("AND", ["w17","w18"]),      # and9 -> w25
    ("OR",  ["w19","w20"]),      # or7 -> w26
    ("XOR", ["w21","w22"]),      # xor9 -> w27
    ("AND", ["w23","w24"]),      # and10 -> w28
    ("OR",  ["w25","w26"]),      # or8 -> w29
    ("XOR", ["w27","w28"]),      # xor10 -> w30
    ("AND", ["w22","w24"]),      # and11 -> w31
    ("OR",  ["w21","w23"]),      # or9 -> w32
    # Final Stage (32-37)
    ("XOR", ["w29","w30"]),      # xor11 -> u1
    ("AND", ["w31","w32"]),      # and12 -> u2
    ("OR",  ["w17","w29"]),      # or10 -> u3
    ("NOT", ["u2"]),             # not4 -> out2
    ("OR",  ["u1","u3"]),        # or11 -> out1
    ("XOR", ["w30","w31"]),      # xor12 -> out3
]

# Primary input names
primary_inputs = ["in1","in2","in3","in4","in5","in6","in7","in8","in9","in10"]

# Test cases: (in1..in10, out1,out2,out3)
test_cases = [
    (1,1,0,1,1,0,1,0,1,0, 0,1,0),
    (0,1,1,0,1,1,0,1,1,1, 0,1,0),
    (1,0,1,1,0,0,1,1,0,0, 0,1,0),
    (0,0,0,1,1,1,1,0,0,1, 0,1,0),
    (1,1,1,1,0,1,0,0,1,0, 0,1,0),
    (0,1,0,0,1,0,1,1,0,1, 0,1,0),
    (1,0,0,1,0,1,1,0,1,1, 0,1,0),
    (0,0,1,0,1,0,0,1,1,0, 0,1,0)
]

# Wire index map
wire_index = {name: idx for idx, name in enumerate(wire_names)}
pi_index = {name: idx for idx, name in enumerate(primary_inputs)}

# Create optimizer
opt = Optimize()

# For each test case t and each wire w, correct (fault-free) value
correct = [[Bool(f"correct_t{t}_w{w}") for w in range(NUM_GATES)] for t in range(NUM_TESTS)]

# For each test case t and each wire w, actual (faulty) value
actual = [[Bool(f"actual_t{t}_w{w}") for w in range(NUM_GATES)] for t in range(NUM_TESTS)]

# Fault mode for each gate: 0=none, 1=stuck0, 2=stuck1, 3=invert, 4=open
fault_mode = [Int(f"fm_{g}") for g in range(NUM_GATES)]

# Open values (only used when fault_mode==4)
open_val = [[Bool(f"open_t{t}_g{g}") for g in range(NUM_GATES)] for t in range(NUM_TESTS)]

# Constrain fault modes
for g in range(NUM_GATES):
    opt.add(And(fault_mode[g] >= 0, fault_mode[g] <= 4))

# At most 3 faulty gates
opt.add(Sum([If(fault_mode[g] != 0, 1, 0) for g in range(NUM_GATES)]) <= 3)

# Cost
cost = Sum([
    If(fault_mode[g] == 1, 1,
    If(fault_mode[g] == 2, 1,
    If(fault_mode[g] == 3, 1,
    If(fault_mode[g] == 4, 2, 0)))) for g in range(NUM_GATES)
])

def get_pi_value(t, name):
    """Get the constant boolean value of a primary input for test t."""
    idx = pi_index[name]
    return BoolVal(test_cases[t][idx] == 1)

def get_correct_wire(t, name):
    """Get the correct (fault-free) value of a wire or primary input."""
    if name in pi_index:
        return get_pi_value(t, name)
    w = wire_index[name]
    return correct[t][w]

def get_actual_wire(t, name):
    """Get the actual (faulty) value of a wire or primary input."""
    if name in pi_index:
        return get_pi_value(t, name)
    w = wire_index[name]
    return actual[t][w]

# Compute correct (fault-free) values for all gates in topological order
for t in range(NUM_TESTS):
    for g in range(NUM_GATES):
        gtype, inputs = gate_info[g]
        
        if gtype == "AND":
            val = And([get_correct_wire(t, inp) for inp in inputs])
        elif gtype == "OR":
            val = Or([get_correct_wire(t, inp) for inp in inputs])
        elif gtype == "XOR":
            val = Xor(get_correct_wire(t, inputs[0]), get_correct_wire(t, inputs[1]))
        elif gtype == "NOT":
            val = Not(get_correct_wire(t, inputs[0]))
        else:
            val = BoolVal(False)
        
        opt.add(correct[t][g] == val)

# Compute actual (faulty) values
for t in range(NUM_TESTS):
    for g in range(NUM_GATES):
        gtype, inputs = gate_info[g]
        
        # Compute what the output would be based on actual inputs (faulty propagation)
        if gtype == "AND":
            correct_val = And([get_actual_wire(t, inp) for inp in inputs])
        elif gtype == "OR":
            correct_val = Or([get_actual_wire(t, inp) for inp in inputs])
        elif gtype == "XOR":
            correct_val = Xor(get_actual_wire(t, inputs[0]), get_actual_wire(t, inputs[1]))
        elif gtype == "NOT":
            correct_val = Not(get_actual_wire(t, inputs[0]))
        else:
            correct_val = BoolVal(False)
        
        # Apply fault mode
        opt.add(
            actual[t][g] == If(fault_mode[g] == 0, correct_val,
                          If(fault_mode[g] == 1, BoolVal(False),
                          If(fault_mode[g] == 2, BoolVal(True),
                          If(fault_mode[g] == 3, Not(correct_val),
                             open_val[t][g]))))
        )

# Constrain observed outputs
# out1 = wire index 36, out2 = wire index 35, out3 = wire index 37
# But wait: wire_names[35] = "out2", wire_names[36] = "out1", wire_names[37] = "out3"
# Let me check: wire_names = [w1..w32, u1, u2, u3, out2, out1, out3]
# So out2=35, out1=36, out3=37
for t in range(NUM_TESTS):
    opt.add(actual[t][36] == BoolVal(test_cases[t][10] == 1))  # out1
    opt.add(actual[t][35] == BoolVal(test_cases[t][11] == 1))  # out2
    opt.add(actual[t][37] == BoolVal(test_cases[t][12] == 1))  # out3

# Minimize cost
opt.minimize(cost)

# Solve
result = opt.check()

if result == sat:
    m = opt.model()
    total_cost = m.eval(cost).as_long()
    print("STATUS: sat")
    print(f"Total cost: {total_cost}")
    
    # Print faulty gates
    faulty_gates = []
    for g in range(NUM_GATES):
        fm = m.eval(fault_mode[g]).as_long()
        if fm != 0:
            mode_names = {1: "stuck0", 2: "stuck1", 3: "invert", 4: "open"}
            faulty_gates.append((gate_names[g], mode_names[fm], fm))
    
    print(f"Number of faulty gates: {len(faulty_gates)}")
    for name, mode, fm in faulty_gates:
        cost_str = "1" if fm != 4 else "2"
        print(f"  {name}: {mode} (cost={cost_str})")
    
    # Verification
    print("\nVerification:")
    all_ok = True
    for t in range(NUM_TESTS):
        o1 = m.eval(actual[t][36])
        o2 = m.eval(actual[t][35])
        o3 = m.eval(actual[t][37])
        exp = test_cases[t][10:13]
        ok = (int(o1==True) == exp[0] and int(o2==True) == exp[1] and int(o3==True) == exp[2])
        if not ok:
            all_ok = False
        print(f"  Test {t+1}: actual=({int(o1==True)},{int(o2==True)},{int(o3==True)}), expected={exp} {'OK' if ok else 'FAIL'}")
    
    print(f"\nAll tests pass: {all_ok}")
    print(f"Minimal: True")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No solution found with at most 3 faulty gates")
else:
    print("STATUS: unknown")