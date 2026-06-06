from z3 import *

# BENCHMARK_MODE: ON (since the problem is guaranteed solvable)
BENCHMARK_MODE = True

# Number of test cases
num_tests = 8

# Number of gates
num_gates = 46

# Gate names (for reference)
# We will fill this list with 46 entries, some named, some unnamed.
gate_names = []

# Layer 1 (8 gates)
named_gates_layer1 = [
    "and1", "xor1", "or1", "and2", 
    "xor2", "not1", "or2", "and3"
]
gate_names.extend(named_gates_layer1)

# Layer 2 (8 gates): fill with placeholders
for i in range(8):
    gate_names.append(f"layer2_gate_{i+1}")

# Layer 3 (8 gates): fill with placeholders
for i in range(8):
    gate_names.append(f"layer3_gate_{i+1}")

# Layer 4 (8 gates): fill with placeholders
for i in range(8):
    gate_names.append(f"layer4_gate_{i+1}")

# Final Stage (6 gates): fill with placeholders
for i in range(6):
    gate_names.append(f"final_stage_gate_{i+1}")

# Verify length
assert len(gate_names) == num_gates, f"gate_names length {len(gate_names)} != num_gates {num_gates}"

# Fault modes and their costs
fault_modes = ["none", "stuck0", "stuck1", "invert", "open"]
fault_costs = {"none": 0, "stuck0": 1, "stuck1": 1, "invert": 1, "open": 2}

# Circuit structure: for each gate, define its type and inputs
# Format: (gate_type, [input1, input2]) for binary gates, (gate_type, [input1]) for unary gates
gate_structure = [
    ("and", ["in1", "in2"]),  # and1
    ("xor", ["in3", "in4"]),  # xor1
    ("or", ["in5", "in6"]),   # or1
    ("and", ["in7", "in8"]),  # and2
    ("xor", ["in9", "in10"]), # xor2
    ("not", ["in1"]),         # not1
    ("or", ["in3", "in5"]),   # or2
    ("and", ["in4", "in6"]),  # and3
    
    # Layer 2 (8 gates)
    ("and", ["w1", "w2"]),    # layer2_gate_1
    ("or", ["w3", "w4"]),     # layer2_gate_2
    ("xor", ["w5", "w6"]),    # layer2_gate_3
    ("and", ["w2", "w7"]),    # layer2_gate_4
    ("or", ["w8", "w5"]),     # layer2_gate_5
    ("not", ["w7"]),          # layer2_gate_6
    ("xor", ["w6", "w1"]),    # layer2_gate_7
    ("and", ["w4", "w8"]),    # layer2_gate_8
    
    # Layer 3 (8 gates)
    ("xor", ["w9", "w10"]),   # layer3_gate_1
    ("and", ["w11", "w12"]),  # layer3_gate_2
    ("or", ["w13", "w14"]),   # layer3_gate_3
    ("xor", ["w15", "w16"]),  # layer3_gate_4
    ("and", ["w9", "w13"]),   # layer3_gate_5
    ("or", ["w10", "w12"]),   # layer3_gate_6
    ("not", ["w11"]),         # layer3_gate_7
    ("xor", ["w14", "w16"]),  # layer3_gate_8
    
    # Layer 4 (8 gates)
    ("and", ["w17", "w18"]),  # layer4_gate_1
    ("or", ["w19", "w20"]),   # layer4_gate_2
    ("xor", ["w21", "w22"]),  # layer4_gate_3
    ("and", ["w23", "w24"]),  # layer4_gate_4
    ("or", ["w25", "w26"]),   # layer4_gate_5
    ("xor", ["w27", "w28"]),  # layer4_gate_6
    ("and", ["w22", "w24"]),  # layer4_gate_7
    ("or", ["w21", "w23"]),   # layer4_gate_8
    
    # Final Stage (6 gates)
    ("xor", ["w29", "w30"]),  # final_stage_gate_1
    ("and", ["w31", "w32"]),  # final_stage_gate_2
    ("or", ["w17", "w29"]),   # final_stage_gate_3
    ("not", ["u2"]),          # final_stage_gate_4
    ("or", ["u1", "u3"]),     # final_stage_gate_5
    ("xor", ["w30", "w31"]),  # final_stage_gate_6
]

# Primary inputs
primary_inputs = ["in1", "in2", "in3", "in4", "in5", "in6", "in7", "in8", "in9", "in10"]

# Primary outputs
primary_outputs = ["out1", "out2", "out3"]

# Test cases: list of dictionaries with input values and observed outputs
test_cases = [
    {"inputs": {"in1": 1, "in2": 1, "in3": 0, "in4": 1, "in5": 1, "in6": 0, "in7": 1, "in8": 0, "in9": 1, "in10": 0}, "outputs": {"out1": 0, "out2": 1, "out3": 0}},
    {"inputs": {"in1": 0, "in2": 1, "in3": 1, "in4": 0, "in5": 1, "in6": 1, "in7": 0, "in8": 1, "in9": 1, "in10": 1}, "outputs": {"out1": 0, "out2": 1, "out3": 0}},
    {"inputs": {"in1": 1, "in2": 0, "in3": 1, "in4": 1, "in5": 0, "in6": 0, "in7": 1, "in8": 1, "in9": 0, "in10": 0}, "outputs": {"out1": 0, "out2": 1, "out3": 0}},
    {"inputs": {"in1": 0, "in2": 0, "in3": 0, "in4": 1, "in5": 1, "in6": 1, "in7": 1, "in8": 0, "in9": 0, "in10": 1}, "outputs": {"out1": 0, "out2": 1, "out3": 0}},
    {"inputs": {"in1": 1, "in2": 1, "in3": 1, "in4": 1, "in5": 0, "in6": 1, "in7": 0, "in8": 0, "in9": 1, "in10": 0}, "outputs": {"out1": 0, "out2": 1, "out3": 0}},
    {"inputs": {"in1": 0, "in2": 1, "in3": 0, "in4": 0, "in5": 1, "in6": 0, "in7": 1, "in8": 1, "in9": 0, "in10": 1}, "outputs": {"out1": 0, "out2": 1, "out3": 0}},
    {"inputs": {"in1": 1, "in2": 0, "in3": 0, "in4": 1, "in5": 0, "in6": 1, "in7": 1, "in8": 0, "in9": 1, "in10": 1}, "outputs": {"out1": 0, "out2": 1, "out3": 0}},
    {"inputs": {"in1": 0, "in2": 0, "in3": 1, "in4": 0, "in5": 1, "in6": 0, "in7": 0, "in8": 1, "in9": 1, "in10": 0}, "outputs": {"out1": 0, "out2": 1, "out3": 0}},
]

# Create a solver
solver = Optimize()

# Declare symbolic variables for gate outputs per test case
# gate_outputs[gate_idx][test_idx] = output value
gate_outputs = [[Int(f"gate_{gate_names[g]}_test_{t}") for t in range(num_tests)] for g in range(num_gates)]

# Declare symbolic variables for primary outputs per test case
primary_outputs_vars = [[Int(f"{po}_test_{t}") for t in range(num_tests)] for po in primary_outputs]

# Declare symbolic variables for fault modes per gate
# fault_mode[gate_idx] is a symbolic value representing the fault mode
none, stuck0, stuck1, invert, open = 0, 1, 2, 3, 4
fault_mode = [Int(f"fault_mode_{gate_names[g]}") for g in range(num_gates)]

# Declare symbolic variables for fault costs per gate
fault_cost = [Int(f"fault_cost_{gate_names[g]}") for g in range(num_gates)]

# Helper function to get the correct output of a gate given its inputs and type
def get_correct_output(gate_type, inputs):
    if gate_type == "and":
        return inputs[0] & inputs[1]
    elif gate_type == "or":
        return inputs[0] | inputs[1]
    elif gate_type == "xor":
        return inputs[0] ^ inputs[1]
    elif gate_type == "not":
        return 1 - inputs[0]
    else:
        raise ValueError(f"Unknown gate type: {gate_type}")

# Add constraints for each test case
for t in range(num_tests):
    # Set primary input values for this test case
    for pi in primary_inputs:
        pi_idx = primary_inputs.index(pi)
        solver.add(gate_outputs[pi_idx][t] == test_cases[t]["inputs"][pi])

    # Compute gate outputs in topological order
    for g in range(num_gates):
        gate_type, inputs = gate_structure[g]
        input_indices = []
        for inp in inputs:
            # Map input to its corresponding gate or primary input index
            if inp in gate_names:
                input_indices.append(gate_names.index(inp))
            elif inp in primary_inputs:
                input_indices.append(primary_inputs.index(inp))
            else:
                # This input is a wire (e.g., w1, w2) from a previous gate
                # We need to find its index in the gate_names list
                input_indices.append(gate_names.index(inp))

        # Get the correct output for this gate (without faults)
        correct_output = get_correct_output(gate_type, [gate_outputs[i][t] for i in input_indices])

        # Define the output based on the fault mode
        solver.add(
            If(fault_mode[g] == none, gate_outputs[g][t] == correct_output,
            If(fault_mode[g] == stuck0, gate_outputs[g][t] == 0,
            If(fault_mode[g] == stuck1, gate_outputs[g][t] == 1,
            If(fault_mode[g] == invert, gate_outputs[g][t] == 1 - correct_output,
            # open: no constraint
            True
            ))))
        )

        # Define the cost based on the fault mode
        solver.add(
            If(fault_mode[g] == none, fault_cost[g] == 0,
            If(fault_mode[g] == stuck0, fault_cost[g] == 1,
            If(fault_mode[g] == stuck1, fault_cost[g] == 1,
            If(fault_mode[g] == invert, fault_cost[g] == 1,
            fault_cost[g] == 2  # open
            ))))
        )

    # Compute primary outputs
    # From the circuit structure:
    # u1 = xor11: xor(w29, w30)
    # u2 = and12: and(w31, w32)
    # u3 = or10: or(w17, w29)
    # out1 = or11: or(u1, u3)
    # out2 = not4: not(u2)
    # out3 = xor12: xor(w30, w31)
    
    # Find the indices for the final stage gates
    xor11_idx = gate_names.index("final_stage_gate_1")
    and12_idx = gate_names.index("final_stage_gate_2")
    or10_idx = gate_names.index("final_stage_gate_3")
    not4_idx = gate_names.index("final_stage_gate_4")
    or11_idx = gate_names.index("final_stage_gate_5")
    xor12_idx = gate_names.index("final_stage_gate_6")
    
    # Assign u1, u2, u3 based on the final stage gate outputs
    u1 = gate_outputs[xor11_idx][t]
    u2 = gate_outputs[and12_idx][t]
    u3 = gate_outputs[or10_idx][t]
    
    # out2 = not4: not(u2)
    solver.add(gate_outputs[not4_idx][t] == 1 - u2)
    
    # Assign primary outputs
    for po_idx, po in enumerate(primary_outputs):
        if po == "out1":
            solver.add(primary_outputs_vars[po_idx][t] == gate_outputs[or11_idx][t])
        elif po == "out2":
            solver.add(primary_outputs_vars[po_idx][t] == gate_outputs[not4_idx][t])
        elif po == "out3":
            solver.add(primary_outputs_vars[po_idx][t] == gate_outputs[xor12_idx][t])

# Fault budget: at most 3 gates can be faulty in total (across all test cases)
# We need to count the number of gates with a non-"none" fault mode.
solver.add(Sum([If(fault_mode[g] != none, 1, 0) for g in range(num_gates)]) <= 3)

# Minimize the total cost
total_cost = Sum(fault_cost)
solver.minimize(total_cost)

# Check for a solution
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Total cost:", model.eval(total_cost))
    print("Faulty gates and modes:")
    for g in range(num_gates):
        mode = model.eval(fault_mode[g])
        if mode != none:
            print(f"{gate_names[g]}: {fault_modes[mode]} (cost: {model.eval(fault_cost[g])})")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")