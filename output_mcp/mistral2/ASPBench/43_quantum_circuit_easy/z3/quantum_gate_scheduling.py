from z3 import *

# Gate names and their qubit operands
GATES = {
    'h_q0': ['q0'],
    'h_q1': ['q1'],
    'x_q2': ['q2'],
    'cnot_q0_q1': ['q0', 'q1'],
    'cnot_q1_q2': ['q1', 'q2'],
    'cnot_q0_q3': ['q0', 'q3']
}

# Qubits involved
QUBITS = ['q0', 'q1', 'q2', 'q3']

# Create a solver
solver = Optimize()

# Decision variables: time step for each gate
time_vars = {gate: Int(f'time_{gate}') for gate in GATES}

# Constraint: Each gate must be scheduled at exactly one time step
for gate in GATES:
    solver.add(time_vars[gate] >= 1)

# Constraint: Two gates cannot execute at the same time if they share any qubit
for i, gate1 in enumerate(GATES):
    for gate2 in list(GATES)[i+1:]:
        # If gates share any qubit, they cannot be scheduled at the same time
        shared_qubits = set(GATES[gate1]) & set(GATES[gate2])
        if shared_qubits:
            solver.add(time_vars[gate1] != time_vars[gate2])

# Objective: Minimize the maximum time step used
max_time = Int('max_time')
solver.add(max_time >= time_vars[gate] for gate in GATES)
solver.minimize(max_time)

# Check if a solution exists
result = solver.check()

if result == sat:
    model = solver.model()
    circuit_depth = model[max_time].as_long()
    
    # Extract gate schedule per time step
    gate_schedule = {}
    for gate in GATES:
        t = model[time_vars[gate]].as_long()
        if t not in gate_schedule:
            gate_schedule[t] = []
        gate_schedule[t].append(gate)
    
    # Sort time steps
    sorted_times = sorted(gate_schedule.keys())
    
    print("STATUS: sat")
    print(f"circuit_depth = {circuit_depth}")
    print("gate_schedule = [")
    for t in sorted_times:
        print(f"  {{'time': {t}, 'gates': {gate_schedule[t]}}},")
    print("]")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")