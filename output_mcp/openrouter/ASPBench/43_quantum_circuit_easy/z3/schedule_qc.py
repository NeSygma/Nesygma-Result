from z3 import *

# Define gates
gates = ['h_q0', 'h_q1', 'x_q2', 'cnot_q0_q1', 'cnot_q1_q2', 'cnot_q0_q3']
# Create time variables for each gate
times = {g: Int(f't_{g}') for g in gates}

opt = Optimize()
# Each gate scheduled at time >=1
for g in gates:
    opt.add(times[g] >= 1)

# Define qubit usage per gate
qubits = {
    'h_q0': {'q0'},
    'h_q1': {'q1'},
    'x_q2': {'q2'},
    'cnot_q0_q1': {'q0', 'q1'},
    'cnot_q1_q2': {'q1', 'q2'},
    'cnot_q0_q3': {'q0', 'q3'}
}

# Add conflict constraints: overlapping qubits cannot share same time
for i in range(len(gates)):
    for j in range(i+1, len(gates)):
        g1 = gates[i]
        g2 = gates[j]
        if qubits[g1] & qubits[g2]:
            opt.add(times[g1] != times[g2])

# Define max_time variable
max_time = Int('max_time')
opt.add(max_time >= 1)
for g in gates:
    opt.add(times[g] <= max_time)

# Minimize max_time
opt.minimize(max_time)

if opt.check() == sat:
    m = opt.model()
    depth = m[max_time].as_long()
    # Build schedule dictionary
    schedule = {t: [] for t in range(1, depth+1)}
    for g in gates:
        t = m[times[g]].as_long()
        schedule[t].append(g)
    print("STATUS: sat")
    print(f"circuit_depth = {depth}")
    for t in range(1, depth+1):
        gates_at_t = schedule[t]
        print(f"time {t}: {gates_at_t}")
else:
    print("STATUS: unsat")