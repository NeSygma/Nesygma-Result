from z3 import *

# Define a reasonable upper bound on circuit depth
MAX_DEPTH = 5

# Time step variables for each gate (1-indexed)
t_h = Int('t_h')          # h_q0 uses qubit 0
t_x = Int('t_x')          # x_q1 uses qubit 1
t_c23 = Int('t_c23')      # cnot_q2_q3 uses qubits 2,3
t_c45 = Int('t_c45')      # cnot_q4_q5 uses qubits 4,5
t_c02 = Int('t_c02')      # cnot_q0_q2 uses qubits 0,2 (needs adjacency via swap)
t_tof = Int('t_tof')      # toffoli_q5_q7_q6 uses qubits 5,7,6
t_swap = Int('t_swap')    # swap between qubits 1 and 2 (physical adjacency) to enable cnot_q0_q2

# Swap usage indicator (0/1)
swap_used = Int('swap_used')

# Depth variable (overall circuit depth)
D = Int('D')

opt = Optimize()

# Domain constraints for time variables
vars = [t_h, t_x, t_c23, t_c45, t_c02, t_tof, t_swap]
for v in vars:
    opt.add(v >= 1, v <= MAX_DEPTH)
opt.add(swap_used >= 0, swap_used <= 1)
opt.add(D >= 1, D <= MAX_DEPTH)

# Depth must be at least each gate time (including swap)
for v in vars:
    opt.add(D >= v)

# No qubit conflicts: gates sharing any logical qubit cannot be at the same time step
uses = {
    t_h: [0],
    t_x: [1],
    t_c23: [2, 3],
    t_c45: [4, 5],
    t_c02: [0, 2],
    t_tof: [5, 6, 7],
    t_swap: [1, 2]  # swap touches qubits 1 and 2
}
gate_vars = list(uses.keys())
for i in range(len(gate_vars)):
    for j in range(i + 1, len(gate_vars)):
        vi = gate_vars[i]
        vj = gate_vars[j]
        if set(uses[vi]).intersection(uses[vj]):
            opt.add(vi != vj)

# Dependency ordering: toffoli must be strictly after cnot_q4_q5
opt.add(t_tof > t_c45)

# Enforce that a swap is used to enable cnot_q0_q2 (they are not adjacent initially)
opt.add(swap_used == 1)
opt.add(t_swap < t_c02)

# Lexicographic optimization: first minimize depth, then number of swaps
opt.minimize(D)
opt.minimize(swap_used)

# Solve
if opt.check() == sat:
    m = opt.model()
    depth = m[D].as_long()
    swaps = m[swap_used].as_long()
    # Build schedule dictionary
    schedule = {i: [] for i in range(1, depth + 1)}
    def add_gate(time_var, name):
        t = m[time_var].as_long()
        schedule[t].append(name)
    add_gate(t_h, 'h_q0')
    add_gate(t_x, 'x_q1')
    add_gate(t_c23, 'cnot_q2_q3')
    add_gate(t_c45, 'cnot_q4_q5')
    add_gate(t_c02, 'cnot_q0_q2')
    add_gate(t_tof, 'toffoli_q5_q7_q6')
    add_gate(t_swap, 'swap_q1_q2')
    # Sort gate names alphabetically within each time step
    for ts in schedule:
        schedule[ts].sort()
    # Output results
    print('STATUS: sat')
    print('circuit_depth =', depth)
    print('swaps_used =', swaps)
    print('gate_schedule:')
    for ts in range(1, depth + 1):
        print(f'  time {ts}: {schedule[ts]}')
else:
    print('STATUS: unsat')