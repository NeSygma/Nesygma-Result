from z3 import *

# ============================================================================
# Quantum Circuit Scheduling with Topology Constraints
# ============================================================================

# Initialize solver with optimization
opt = Optimize()

# ============================================================================
# Parameters and Constants
# ============================================================================

# Qubits
qubits = [f'q{i}' for i in range(8)]

# Gate names
gates = [
    'h_q0',
    'x_q1',
    'cnot_q2_q3',
    'cnot_q4_q5',
    'cnot_q0_q2',
    'toffoli_q5_q7_q6'
]

# Gate types (single-qubit, two-qubit, three-qubit)
gate_types = {
    'h_q0': 'single',
    'x_q1': 'single',
    'cnot_q2_q3': 'two',
    'cnot_q4_q5': 'two',
    'cnot_q0_q2': 'two',
    'toffoli_q5_q7_q6': 'three'
}

# Gate dependencies: (dependent_gate, required_gate)
dependencies = [('toffoli_q5_q7_q6', 'cnot_q4_q5')]

# Adjacency in 2x4 grid (linear indices 0-7)
# Positions: 0 1 2 3
#            4 5 6 7
adjacency = {
    0: [1, 4],
    1: [0, 2, 5],
    2: [1, 3, 6],
    3: [2, 7],
    4: [0, 5],
    5: [1, 4, 6],
    6: [2, 5, 7],
    7: [3, 6]
}

# Precompute all adjacent pairs (i,j) with i < j
adjacent_pairs = []
for i in range(8):
    for j in adjacency[i]:
        if i < j:
            adjacent_pairs.append((i, j))

# Helper: convert qubit name to index
def qubit_to_idx(q):
    return int(q[1:])

# Helper: get qubits involved in a gate
def gate_qubits(gate):
    if gate == 'h_q0':
        return ['q0']
    elif gate == 'x_q1':
        return ['q1']
    elif gate == 'cnot_q2_q3':
        return ['q2', 'q3']
    elif gate == 'cnot_q4_q5':
        return ['q4', 'q5']
    elif gate == 'cnot_q0_q2':
        return ['q0', 'q2']
    elif gate == 'toffoli_q5_q7_q6':
        return ['q5', 'q7', 'q6']
    else:
        raise ValueError(f"Unknown gate: {gate}")

# ============================================================================
# Decision Variables
# ============================================================================

# Circuit depth (number of time steps)
circuit_depth = Int('circuit_depth')
opt.add(circuit_depth >= 1)

# Gate scheduling: time step for each gate
# gate_time[g] = time step (1-indexed)
gate_time = {g: Int(f'gate_time_{g}') for g in gates}

# SWAP count
swaps_used = Int('swaps_used')
opt.add(swaps_used >= 0)

# Qubit positions over time: pos[q][t] = physical qubit index at time t
# We model this as a Z3 array for each logical qubit
# pos[q] is an array from time to physical position
pos = {q: Array(f'pos_q{q}', IntSort(), IntSort()) for q in range(8)}

# Initial positions: at time 0, logical qubit q is at physical position q
for q in range(8):
    opt.add(pos[q][0] == q)

# ============================================================================
# Constraints
# ============================================================================

# 1. All gates must be scheduled exactly once
for g in gates:
    opt.add(gate_time[g] >= 1)
    opt.add(gate_time[g] <= circuit_depth)

# 2. Gate dependencies must be respected
for dep_gate, req_gate in dependencies:
    opt.add(gate_time[dep_gate] > gate_time[req_gate])

# 3. Multi-qubit gates can only operate on adjacent qubits
# For each gate at its scheduled time, check adjacency of involved qubits' positions
for g in gates:
    q_list = gate_qubits(g)
    q_idxs = [qubit_to_idx(q) for q in q_list]
    t_gate = gate_time[g]
    
    if gate_types[g] == 'single':
        # Single-qubit gate: no adjacency constraint
        pass
    elif gate_types[g] == 'two':
        # Two-qubit gate: controls and targets must be adjacent
        # Get the physical positions of the two qubits at time t_gate
        p0 = pos[q_idxs[0]][t_gate]
        p1 = pos[q_idxs[1]][t_gate]
        # They must be adjacent
        opt.add(Or([And(p0 == i, p1 == j) for (i, j) in adjacent_pairs]))
    elif gate_types[g] == 'three':
        # Three-qubit gate (Toffoli): both controls must be adjacent to target
        # For toffoli_q5_q7_q6: controls q5, q7; target q6
        p5 = pos[5][t_gate]
        p7 = pos[7][t_gate]
        p6 = pos[6][t_gate]
        # Both p5 and p7 must be adjacent to p6
        # p5 adjacent to p6
        opt.add(Or([And(p5 == i, p6 == j) for (i, j) in adjacent_pairs]))
        # p7 adjacent to p6
        opt.add(Or([And(p7 == i, p6 == j) for (i, j) in adjacent_pairs]))

# 4. No qubit conflicts at each time step
# For each time step t, and for each pair of logical qubits, their physical positions must be distinct
max_t = circuit_depth
for t in range(1, 10):  # Up to 10 time steps
    for q1 in range(8):
        for q2 in range(q1+1, 8):
            opt.add(pos[q1][t] != pos[q2][t])

# 5. SWAP operations: count the number of times a qubit's position changes
# We count the number of "swaps" as the number of times a qubit's position changes between time steps
# This is a proxy for the number of SWAP gates
swap_events = []
for q in range(8):
    for t in range(1, 10):
        change = Bool(f'change_{q}_{t}')
        opt.add(Implies(change, pos[q][t] != pos[q][t-1]))
        opt.add(Implies(Not(change), pos[q][t] == pos[q][t-1]))
        swap_events.append(change)
opt.add(swaps_used == Sum(swap_events))

# 6. All gates must be scheduled
# This is already enforced by the gate_time constraints

# ============================================================================
# Objective: Minimize circuit depth, then minimize SWAPs
# ============================================================================

# We want to find the minimal circuit_depth such that all constraints are satisfied
# Then, among those, minimize swaps_used

# Add soft constraints for optimization
# First, minimize circuit_depth
opt.minimize(circuit_depth)

# Second, minimize swaps_used
opt.minimize(swaps_used)

# ============================================================================
# Check and Output
# ============================================================================

result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print(f"circuit_depth = {model[circuit_depth]}")
    print(f"swaps_used = {model[swaps_used]}")
    
    # Print gate schedule
    print("gate_schedule:")
    for t in range(1, int(str(model[circuit_depth])) + 1):
        gates_at_t = []
        for g in gates:
            if model[gate_time[g]] == t:
                gates_at_t.append(g)
        gates_at_t.sort()
        print(f"  time {t}: gates = {gates_at_t}")
    
    # Print qubit positions over time (first few steps)
    print("qubit_positions_over_time:")
    for t in range(0, min(4, int(str(model[circuit_depth])) + 1)):
        pos_at_t = []
        for q in range(8):
            p = model.eval(pos[q][t], model_completion=True)
            pos_at_t.append(f"q{q}@p{p}")
        print(f"  time {t}: {' '.join(pos_at_t)}")
    
elif result == unsat:
    print("STATUS: unsat")
    if True:  # BENCHMARK_MODE
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")