from z3 import *

# Circuit structure definition
gates = {
    # Layer 1
    'and1': ('AND', ['in1', 'in2'], 'w1'),
    'xor1': ('XOR', ['in3', 'in4'], 'w2'),
    'or1': ('OR', ['in5', 'in6'], 'w3'),
    'and2': ('AND', ['in7', 'in8'], 'w4'),
    'xor2': ('XOR', ['in9', 'in10'], 'w5'),
    'not1': ('NOT', ['in1'], 'w6'),
    'or2': ('OR', ['in3', 'in5'], 'w7'),
    'and3': ('AND', ['in4', 'in6'], 'w8'),
    
    # Layer 2
    'and4': ('AND', ['w1', 'w2'], 'w9'),
    'or3': ('OR', ['w3', 'w4'], 'w10'),
    'xor4': ('XOR', ['w5', 'w6'], 'w11'),
    'and5': ('AND', ['w2', 'w7'], 'w12'),
    'or4': ('OR', ['w8', 'w5'], 'w13'),
    'not2': ('NOT', ['w7'], 'w14'),
    'xor5': ('XOR', ['w6', 'w1'], 'w15'),
    'and6': ('AND', ['w4', 'w8'], 'w16'),
    
    # Layer 3
    'xor6': ('XOR', ['w9', 'w10'], 'w17'),
    'and7': ('AND', ['w11', 'w12'], 'w18'),
    'or5': ('OR', ['w13', 'w14'], 'w19'),
    'xor7': ('XOR', ['w15', 'w16'], 'w20'),
    'and8': ('AND', ['w9', 'w13'], 'w21'),
    'or6': ('OR', ['w10', 'w12'], 'w22'),
    'not3': ('NOT', ['w11'], 'w23'),
    'xor8': ('XOR', ['w14', 'w16'], 'w24'),
    
    # Layer 4
    'and9': ('AND', ['w17', 'w18'], 'w25'),
    'or7': ('OR', ['w19', 'w20'], 'w26'),
    'xor9': ('XOR', ['w21', 'w22'], 'w27'),
    'and10': ('AND', ['w23', 'w24'], 'w28'),
    'or8': ('OR', ['w25', 'w26'], 'w29'),
    'xor10': ('XOR', ['w27', 'w28'], 'w30'),
    'and11': ('AND', ['w22', 'w24'], 'w31'),
    'or9': ('OR', ['w21', 'w23'], 'w32'),
    
    # Final Stage
    'xor11': ('XOR', ['w29', 'w30'], 'u1'),
    'and12': ('AND', ['w31', 'w32'], 'u2'),
    'or10': ('OR', ['w17', 'w29'], 'u3'),
    'not4': ('NOT', ['u2'], 'out2'),
    'or11': ('OR', ['u1', 'u3'], 'out1'),
    'xor12': ('XOR', ['w30', 'w31'], 'out3')
}

# Test cases
test_cases = [
    {'in1':1, 'in2':1, 'in3':0, 'in4':1, 'in5':1, 'in6':0, 'in7':1, 'in8':0, 'in9':1, 'in10':0, 'out1':0, 'out2':1, 'out3':0},
    {'in1':0, 'in2':1, 'in3':1, 'in4':0, 'in5':1, 'in6':1, 'in7':0, 'in8':1, 'in9':1, 'in10':1, 'out1':0, 'out2':1, 'out3':0},
    {'in1':1, 'in2':0, 'in3':1, 'in4':1, 'in5':0, 'in6':0, 'in7':1, 'in8':1, 'in9':0, 'in10':0, 'out1':0, 'out2':1, 'out3':0},
    {'in1':0, 'in2':0, 'in3':0, 'in4':1, 'in5':1, 'in6':1, 'in7':1, 'in8':0, 'in9':0, 'in10':1, 'out1':0, 'out2':1, 'out3':0},
    {'in1':1, 'in2':1, 'in3':1, 'in4':1, 'in5':0, 'in6':1, 'in7':0, 'in8':0, 'in9':1, 'in10':0, 'out1':0, 'out2':1, 'out3':0},
    {'in1':0, 'in2':1, 'in3':0, 'in4':0, 'in5':1, 'in6':0, 'in7':1, 'in8':1, 'in9':0, 'in10':1, 'out1':0, 'out2':1, 'out3':0},
    {'in1':1, 'in2':0, 'in3':0, 'in4':1, 'in5':0, 'in6':1, 'in7':1, 'in8':0, 'in9':1, 'in10':1, 'out1':0, 'out2':1, 'out3':0},
    {'in1':0, 'in2':0, 'in3':1, 'in4':0, 'in5':1, 'in6':0, 'in7':0, 'in8':1, 'in9':1, 'in10':0, 'out1':0, 'out2':1, 'out3':0}
]

# Create solver
solver = Solver()

# Declare fault mode variables for each gate
# 0 = no fault, 1 = stuck0, 2 = stuck1, 3 = invert, 4 = open
fault_mode = {}
for gate_name in gates:
    fault_mode[gate_name] = Int(f'fault_{gate_name}')
    solver.add(fault_mode[gate_name] >= 0, fault_mode[gate_name] <= 4)

# Cost variables
cost_vars = {}
for gate_name in gates:
    cost_vars[gate_name] = Int(f'cost_{gate_name}')
    # Cost depends on fault mode
    solver.add(Implies(fault_mode[gate_name] == 0, cost_vars[gate_name] == 0))  # no fault
    solver.add(Implies(fault_mode[gate_name] == 1, cost_vars[gate_name] == 1))  # stuck0
    solver.add(Implies(fault_mode[gate_name] == 2, cost_vars[gate_name] == 1))  # stuck1
    solver.add(Implies(fault_mode[gate_name] == 3, cost_vars[gate_name] == 1))  # invert
    solver.add(Implies(fault_mode[gate_name] == 4, cost_vars[gate_name] == 2))  # open

# Total cost
total_cost = Int('total_cost')
solver.add(total_cost == Sum([cost_vars[gate] for gate in gates]))

# At most 3 faulty gates
faulty_count = Int('faulty_count')
solver.add(faulty_count == Sum([If(fault_mode[gate] > 0, 1, 0) for gate in gates]))
solver.add(faulty_count <= 3)

# For each test case, model circuit propagation
for test_idx, test in enumerate(test_cases):
    # Create wire variables for this test
    wire_vars = {}
    # Primary inputs
    for inp in ['in1', 'in2', 'in3', 'in4', 'in5', 'in6', 'in7', 'in8', 'in9', 'in10']:
        wire_vars[inp] = Int(f'{inp}_test{test_idx}')
        solver.add(wire_vars[inp] == test[inp])
    
    # Wires and outputs
    all_wires = set()
    for gate_name, (gate_type, inputs, output) in gates.items():
        all_wires.add(output)
        wire_vars[output] = Int(f'{output}_test{test_idx}')
    
    # Process gates in topological order (layers)
    # Layer 1
    for gate_name in ['and1', 'xor1', 'or1', 'and2', 'xor2', 'not1', 'or2', 'and3']:
        gate_type, inputs, output = gates[gate_name]
        fault = fault_mode[gate_name]
        
        # Correct output based on gate type
        if gate_type == 'AND':
            correct = And(wire_vars[inputs[0]] == 1, wire_vars[inputs[1]] == 1)
        elif gate_type == 'OR':
            correct = Or(wire_vars[inputs[0]] == 1, wire_vars[inputs[1]] == 1)
        elif gate_type == 'XOR':
            correct = (wire_vars[inputs[0]] != wire_vars[inputs[1]])
        elif gate_type == 'NOT':
            correct = (wire_vars[inputs[0]] == 0)
        
        # Faulty output
        # stuck0: output = 0
        # stuck1: output = 1
        # invert: output = 1 - correct
        # open: output can be anything (we'll model as unconstrained)
        faulty_output = If(fault == 1, 0,
                          If(fault == 2, 1,
                            If(fault == 3, If(correct, 0, 1),
                              If(fault == 4, wire_vars[output],  # open: keep original
                                If(correct, 1, 0)))))  # no fault
        
        solver.add(wire_vars[output] == faulty_output)
    
    # Layer 2
    for gate_name in ['and4', 'or3', 'xor4', 'and5', 'or4', 'not2', 'xor5', 'and6']:
        gate_type, inputs, output = gates[gate_name]
        fault = fault_mode[gate_name]
        
        if gate_type == 'AND':
            correct = And(wire_vars[inputs[0]] == 1, wire_vars[inputs[1]] == 1)
        elif gate_type == 'OR':
            correct = Or(wire_vars[inputs[0]] == 1, wire_vars[inputs[1]] == 1)
        elif gate_type == 'XOR':
            correct = (wire_vars[inputs[0]] != wire_vars[inputs[1]])
        elif gate_type == 'NOT':
            correct = (wire_vars[inputs[0]] == 0)
        
        faulty_output = If(fault == 1, 0,
                          If(fault == 2, 1,
                            If(fault == 3, If(correct, 0, 1),
                              If(fault == 4, wire_vars[output],
                                If(correct, 1, 0)))))
        
        solver.add(wire_vars[output] == faulty_output)
    
    # Layer 3
    for gate_name in ['xor6', 'and7', 'or5', 'xor7', 'and8', 'or6', 'not3', 'xor8']:
        gate_type, inputs, output = gates[gate_name]
        fault = fault_mode[gate_name]
        
        if gate_type == 'AND':
            correct = And(wire_vars[inputs[0]] == 1, wire_vars[inputs[1]] == 1)
        elif gate_type == 'OR':
            correct = Or(wire_vars[inputs[0]] == 1, wire_vars[inputs[1]] == 1)
        elif gate_type == 'XOR':
            correct = (wire_vars[inputs[0]] != wire_vars[inputs[1]])
        elif gate_type == 'NOT':
            correct = (wire_vars[inputs[0]] == 0)
        
        faulty_output = If(fault == 1, 0,
                          If(fault == 2, 1,
                            If(fault == 3, If(correct, 0, 1),
                              If(fault == 4, wire_vars[output],
                                If(correct, 1, 0)))))
        
        solver.add(wire_vars[output] == faulty_output)
    
    # Layer 4
    for gate_name in ['and9', 'or7', 'xor9', 'and10', 'or8', 'xor10', 'and11', 'or9']:
        gate_type, inputs, output = gates[gate_name]
        fault = fault_mode[gate_name]
        
        if gate_type == 'AND':
            correct = And(wire_vars[inputs[0]] == 1, wire_vars[inputs[1]] == 1)
        elif gate_type == 'OR':
            correct = Or(wire_vars[inputs[0]] == 1, wire_vars[inputs[1]] == 1)
        elif gate_type == 'XOR':
            correct = (wire_vars[inputs[0]] != wire_vars[inputs[1]])
        elif gate_type == 'NOT':
            correct = (wire_vars[inputs[0]] == 0)
        
        faulty_output = If(fault == 1, 0,
                          If(fault == 2, 1,
                            If(fault == 3, If(correct, 0, 1),
                              If(fault == 4, wire_vars[output],
                                If(correct, 1, 0)))))
        
        solver.add(wire_vars[output] == faulty_output)
    
    # Final Stage
    for gate_name in ['xor11', 'and12', 'or10', 'not4', 'or11', 'xor12']:
        gate_type, inputs, output = gates[gate_name]
        fault = fault_mode[gate_name]
        
        if gate_type == 'AND':
            correct = And(wire_vars[inputs[0]] == 1, wire_vars[inputs[1]] == 1)
        elif gate_type == 'OR':
            correct = Or(wire_vars[inputs[0]] == 1, wire_vars[inputs[1]] == 1)
        elif gate_type == 'XOR':
            correct = (wire_vars[inputs[0]] != wire_vars[inputs[1]])
        elif gate_type == 'NOT':
            correct = (wire_vars[inputs[0]] == 0)
        
        faulty_output = If(fault == 1, 0,
                          If(fault == 2, 1,
                            If(fault == 3, If(correct, 0, 1),
                              If(fault == 4, wire_vars[output],
                                If(correct, 1, 0)))))
        
        solver.add(wire_vars[output] == faulty_output)
    
    # Enforce observed outputs
    solver.add(wire_vars['out1'] == test['out1'])
    solver.add(wire_vars['out2'] == test['out2'])
    solver.add(wire_vars['out3'] == test['out3'])

# Minimize total cost
opt = Optimize()
opt.add(solver.assertions())
h = opt.minimize(total_cost)

# Check
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print(f"Total cost: {model[total_cost]}")
    print(f"Faulty gates: {model[faulty_count]}")
    
    # Find which gates are faulty
    faulty_gates = []
    for gate_name in gates:
        mode = model[fault_mode[gate_name]]
        if mode > 0:
            fault_modes = {1: 'stuck0', 2: 'stuck1', 3: 'invert', 4: 'open'}
            faulty_gates.append((gate_name, fault_modes[int(mode)]))
    
    print("Faulty gates:")
    for gate, fault in faulty_gates:
        print(f"  {gate}: {fault}")
    
    # Verify the diagnosis works for all test cases
    print("\nVerification:")
    for test_idx, test in enumerate(test_cases):
        # Check outputs match
        out1_val = model[Int(f'out1_test{test_idx}')]
        out2_val = model[Int(f'out2_test{test_idx}')]
        out3_val = model[Int(f'out3_test{test_idx}')]
        print(f"Test {test_idx+1}: out1={out1_val}, out2={out2_val}, out3={out3_val} (expected: 0,1,0)")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")