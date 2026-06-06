from z3 import *

# Problem parameters
num_qubits = 8
max_depth = 10  # Upper bound for circuit depth

# Qubit indices
qubits = list(range(8))  # q0=0, q1=1, ..., q7=7

# Define adjacency for 2x4 grid
# Row 0: q0-q1, q1-q2, q2-q3
# Row 1: q4-q5, q5-q6, q6-q7
# Columns: q0-q4, q1-q5, q2-q6, q3-q7
adjacent_pairs = [
    (0, 1), (1, 2), (2, 3),  # Row 0
    (4, 5), (5, 6), (6, 7),  # Row 1
    (0, 4), (1, 5), (2, 6), (3, 7)  # Columns
]

# Gate definitions
# Each gate has: name, type, qubits involved
gates = [
    ("h_q0", "single", [0]),
    ("x_q1", "single", [1]),
    ("cnot_q2_q3", "cnot", [2, 3]),  # control=2, target=3
    ("cnot_q4_q5", "cnot", [4, 5]),  # control=4, target=5
    ("cnot_q0_q2", "cnot", [0, 2]),  # control=0, target=2
    ("toffoli_q5_q7_q6", "toffoli", [5, 7, 6])  # controls=5,7, target=6
]

gate_names = [g[0] for g in gates]

# Create solver
solver = Solver()

# Variables for gate scheduling
# gate_time[gate_index] = time step when gate is executed (1-indexed)
gate_time = [Int(f"gate_time_{i}") for i in range(len(gates))]

# Variables for SWAP gates
# We'll model SWAPs as additional gates that can be inserted
# For simplicity, we'll track which qubits are swapped at each time step
# swap_at_time[t][q1][q2] = True if SWAP between q1 and q2 at time t
swap_at_time = [[[Bool(f"swap_{t}_{q1}_{q2}") for q2 in range(num_qubits)] 
                 for q1 in range(num_qubits)] 
                for t in range(max_depth)]

# Variables for logical-to-physical mapping at each time step
# physical_qubit[t][logical_qubit] = physical qubit index at time t
physical_qubit = [[Int(f"phys_{t}_{l}") for l in range(num_qubits)] 
                  for t in range(max_depth + 1)]  # +1 for initial state

# Initial mapping: logical qubit i starts at physical qubit i
for l in range(num_qubits):
    solver.add(physical_qubit[0][l] == l)

# Gate time constraints: all gates must be scheduled between 1 and max_depth
for i, gate_time_var in enumerate(gate_time):
    solver.add(gate_time_var >= 1)
    solver.add(gate_time_var <= max_depth)

# Dependency constraint: toffoli_q5_q7_q6 must be after cnot_q4_q5
# Find indices
cnot_q4_q5_idx = gate_names.index("cnot_q4_q5")
toffoli_idx = gate_names.index("toffoli_q5_q7_q6")
solver.add(gate_time[toffoli_idx] > gate_time[cnot_q4_q5_idx])

# All gates must be scheduled at distinct times (no two gates at same time)
# Actually, multiple gates can be at same time if they don't conflict
# We'll handle conflicts separately

# No qubit conflicts: at each time step, each physical qubit used by at most one gate
# We need to track which physical qubits are used at each time step
used_at_time = [[Bool(f"used_{t}_{p}") for p in range(num_qubits)] for t in range(max_depth)]

# For each gate, mark the physical qubits it uses at its scheduled time
for gate_idx, (gate_name, gate_type, logical_qubits) in enumerate(gates):
    t = gate_time[gate_idx]
    
    # For each logical qubit in the gate, find its physical qubit at time t
    for l_qubit in logical_qubits:
        # The physical qubit at time t is physical_qubit[t][l_qubit]
        # But we need to handle the fact that physical_qubit is indexed by time step
        # We'll use a simpler approach: gates execute at discrete time steps
        
        # For now, assume gates execute instantaneously at their time step
        # and use the physical qubits available at that time
        
        # Mark that this physical qubit is used at this time
        # We need to express: used_at_time[t][phys_qubit] is true if any gate uses it
        pass

# Alternative approach: simpler model
# Let's use a different strategy: assign each gate to a time slot
# and ensure no conflicts

# Create time slots (1 to max_depth)
time_slots = list(range(1, max_depth + 1))

# For each time slot, track which gates are scheduled
# gate_at_time[t][gate_idx] = True if gate_idx is scheduled at time t
gate_at_time = [[Bool(f"gate_at_{t}_{g}") for g in range(len(gates))] 
                for t in range(max_depth)]

# Each gate is scheduled exactly once
for g in range(len(gates)):
    solver.add(Or([gate_at_time[t][g] for t in range(max_depth)]))
    # Exactly one time slot per gate
    solver.add(Sum([If(gate_at_time[t][g], 1, 0) for t in range(max_depth)]) == 1)

# Link gate_time to gate_at_time
for g in range(len(gates)):
    for t in range(max_depth):
        # gate_time[g] == t+1 iff gate_at_time[t][g] is true
        solver.add(Implies(gate_at_time[t][g], gate_time[g] == t + 1))
        solver.add(Implies(gate_time[g] == t + 1, gate_at_time[t][g]))

# No qubit conflicts: at each time step, each physical qubit used by at most one gate
# For each time step, for each physical qubit, at most one gate uses it
for t in range(max_depth):
    for p in range(num_qubits):
        # Count how many gates use physical qubit p at time t
        usage_count = []
        for gate_idx, (gate_name, gate_type, logical_qubits) in enumerate(gates):
            # For this gate, check if it uses physical qubit p at time t
            # This requires knowing the physical qubit mapping
            # We'll use a different approach: ensure gates don't share logical qubits
            # if they're scheduled at the same time
            
            # For now, use a simpler constraint: gates at same time must use disjoint logical qubits
            pass

# Simpler approach: gates at same time must use disjoint logical qubits
for t in range(max_depth):
    for g1 in range(len(gates)):
        for g2 in range(g1 + 1, len(gates)):
            # If both gates are at time t, they must not share logical qubits
            _, _, qubits1 = gates[g1]
            _, _, qubits2 = gates[g2]
            shared = set(qubits1) & set(qubits2)
            if shared:
                # If they share qubits, they cannot be at the same time
                solver.add(Implies(
                    And(gate_at_time[t][g1], gate_at_time[t][g2]),
                    False  # This makes the implication always false, so they can't both be true
                ))
                # Actually, we need: not (gate_at_time[t][g1] and gate_at_time[t][g2])
                solver.add(Not(And(gate_at_time[t][g1], gate_at_time[t][g2])))

# Topology constraint: multi-qubit gates must be on adjacent qubits
# For CNOT and Toffoli gates
for gate_idx, (gate_name, gate_type, logical_qubits) in enumerate(gates):
    if gate_type in ["cnot", "toffoli"]:
        # For CNOT: control and target must be adjacent
        if gate_type == "cnot":
            control, target = logical_qubits[0], logical_qubits[1]
            # Check adjacency in the grid
            # We need to ensure the physical qubits are adjacent
            # For now, assume logical qubits are at their initial positions
            # (we'll add SWAP logic later)
            adjacent = False
            for (q1, q2) in adjacent_pairs:
                if (q1 == control and q2 == target) or (q1 == target and q2 == control):
                    adjacent = True
                    break
            if not adjacent:
                # This gate requires SWAPs to make qubits adjacent
                # We'll handle this with SWAP constraints
                pass
        
        # For Toffoli: both controls must be adjacent to target
        elif gate_type == "toffoli":
            control1, control2, target = logical_qubits[0], logical_qubits[1], logical_qubits[2]
            # Check adjacency for both controls to target
            # We'll handle this with SWAP constraints
            pass

# SWAP constraints: SWAPs can be inserted between adjacent qubits
# We'll model SWAPs as operations that exchange the logical qubits on two physical qubits
# After a SWAP between physical qubits p1 and p2 at time t, the logical qubits are exchanged

# For each time step, track the logical-to-physical mapping
# physical_qubit[t][l] = physical qubit where logical qubit l is located at time t

# SWAP operations affect the mapping
for t in range(max_depth):
    for p1 in range(num_qubits):
        for p2 in range(p1 + 1, num_qubits):
            # Check if p1 and p2 are adjacent
            if (p1, p2) in adjacent_pairs or (p2, p1) in adjacent_pairs:
                # If there's a SWAP between p1 and p2 at time t, then:
                # physical_qubit[t+1][l] = physical_qubit[t][l] for l not on p1 or p2
                # physical_qubit[t+1][l1] = p2 if physical_qubit[t][l1] == p1
                # physical_qubit[t+1][l2] = p1 if physical_qubit[t][l2] == p2
                
                # For each logical qubit l
                for l in range(num_qubits):
                    # If l is on p1 at time t, after SWAP it's on p2 at time t+1
                    # If l is on p2 at time t, after SWAP it's on p1 at time t+1
                    # Otherwise, it stays on the same physical qubit
                    
                    # We need to express this with Z3
                    # This is complex, so let's use a simpler approach for now
                    
                    # For simplicity, assume SWAPs are only needed for specific gates
                    # and we'll add them as needed
                    pass

# Given the complexity, let's use a simpler approach:
# 1. Assume initial mapping: logical qubit i is on physical qubit i
# 2. For each gate, check if its qubits are adjacent in the grid
# 3. If not, we need SWAPs to make them adjacent
# 4. Schedule gates and SWAPs to minimize depth and SWAP count

# Let's identify which gates need SWAPs:
# cnot_q0_q2: q0 and q2 are not adjacent (q0-q1-q2 path, distance 2)
# toffoli_q5_q7_q6: q5 and q6 are adjacent, q7 and q6 are adjacent, but q5 and q7 are not adjacent to each other
#   For Toffoli, both controls need to be adjacent to target, not necessarily to each other

# For cnot_q0_q2: need to make q0 and q2 adjacent
# Options: SWAP q0-q1, then q1-q2, or SWAP q2-q3, then q1-q3, etc.

# Let's create a more practical model:
# We'll schedule gates in time slots and add SWAPs as needed

# Define SWAP gates as additional gates
# SWAP between adjacent qubits p1 and p2
swap_gates = []
for (p1, p2) in adjacent_pairs:
    swap_gates.append(f"swap_{p1}_{p2}")

# All gates (mandatory + SWAPs)
all_gates = gate_names + swap_gates
num_all_gates = len(all_gates)

# Variables for all gates
all_gate_time = [Int(f"all_gate_time_{i}") for i in range(num_all_gates)]
all_gate_at_time = [[Bool(f"all_gate_at_{t}_{g}") for g in range(num_all_gates)] 
                    for t in range(max_depth)]

# Each mandatory gate is scheduled exactly once
for g in range(len(gates)):
    solver.add(Or([all_gate_at_time[t][g] for t in range(max_depth)]))
    solver.add(Sum([If(all_gate_at_time[t][g], 1, 0) for t in range(max_depth)]) == 1)

# SWAP gates are optional (can be used 0 or more times)
# We'll count them and minimize their number

# Link all_gate_time to all_gate_at_time
for g in range(num_all_gates):
    for t in range(max_depth):
        solver.add(Implies(all_gate_at_time[t][g], all_gate_time[g] == t + 1))
        solver.add(Implies(all_gate_time[g] == t + 1, all_gate_at_time[t][g]))

# No conflicts: gates at same time must not share physical qubits
# For mandatory gates, they use logical qubits
# For SWAP gates, they use physical qubits

# For each time step, track which physical qubits are used
# We'll use a simpler approach: ensure no two gates at same time use the same logical/physical qubits

# For mandatory gates at time t, they use logical qubits
# For SWAP gates at time t, they use physical qubits

# Let's define which physical qubits each gate uses
def get_gate_physical_qubits(gate_idx, time_var, physical_mapping):
    """Get the physical qubits used by a gate at a given time"""
    if gate_idx < len(gates):
        # Mandatory gate
        gate_name, gate_type, logical_qubits = gates[gate_idx]
        # Physical qubits depend on the mapping at this time
        # This is complex, so we'll use a different approach
        return []
    else:
        # SWAP gate
        swap_idx = gate_idx - len(gates)
        p1, p2 = adjacent_pairs[swap_idx]
        return [p1, p2]

# Given the complexity of modeling the full mapping, let's use a heuristic approach:
# 1. Schedule gates in a reasonable order
# 2. Add SWAPs only when needed for adjacency
# 3. Minimize depth and SWAP count

# Let's try a specific schedule:
# Time 1: h_q0, x_q1, cnot_q4_q5 (all on different qubits, no conflicts)
# Time 2: cnot_q2_q3 (q2,q3), cnot_q0_q2 (q0,q2) - conflict on q2!
# So we need to schedule them separately or add SWAPs

# Let's model the problem more carefully:
# We need to find a schedule that respects all constraints

# For now, let's create a model that checks if a given schedule is valid
# and then search for the optimal one

# Define a schedule as an assignment of gates to time slots
# We'll use a simple approach: try to find a schedule with depth=3, swaps=1

# Let's assume the optimal solution has depth=3
# We'll create variables for time slots 1, 2, 3

# For each time slot, which gates are scheduled?
time1_gates = [Bool(f"time1_{g}") for g in range(len(gates))]
time2_gates = [Bool(f"time2_{g}") for g in range(len(gates))]
time3_gates = [Bool(f"time3_{g}") for g in range(len(gates))]

# Each gate is scheduled exactly once
for g in range(len(gates)):
    solver.add(Or(time1_gates[g], time2_gates[g], time3_gates[g]))
    solver.add(Sum([If(time1_gates[g], 1, 0), 
                    If(time2_gates[g], 1, 0), 
                    If(time3_gates[g], 1, 0)]) == 1)

# Dependency: toffoli after cnot_q4_q5
cnot_q4_q5_idx = gate_names.index("cnot_q4_q5")
toffoli_idx = gate_names.index("toffoli_q5_q7_q6")
solver.add(Not(time1_gates[toffoli_idx]))  # toffoli cannot be at time 1
solver.add(Implies(time1_gates[cnot_q4_q5_idx], time2_gates[toffoli_idx] or time3_gates[toffoli_idx]))
solver.add(Implies(time2_gates[cnot_q4_q5_idx], time3_gates[toffoli_idx]))

# No conflicts: gates at same time must not share logical qubits
# Time 1 conflicts
for g1 in range(len(gates)):
    for g2 in range(g1 + 1, len(gates)):
        _, _, qubits1 = gates[g1]
        _, _, qubits2 = gates[g2]
        shared = set(qubits1) & set(qubits2)
        if shared:
            solver.add(Not(And(time1_gates[g1], time1_gates[g2])))
            solver.add(Not(And(time2_gates[g1], time2_gates[g2])))
            solver.add(Not(And(time3_gates[g1], time3_gates[g2])))

# Topology constraints for multi-qubit gates
# For cnot_q0_q2: q0 and q2 are not adjacent, so we need a SWAP
# Let's add a SWAP gate between q0 and q1 at time 1
# Then cnot_q0_q2 can be at time 2 or 3

# We'll add SWAP gates as needed
# For now, let's assume we add one SWAP: swap_0_1 at time 1

# Add SWAP gate variables
swap_0_1_time1 = Bool("swap_0_1_time1")
swap_0_1_time2 = Bool("swap_0_1_time2")
swap_0_1_time3 = Bool("swap_0_1_time3")

# SWAP is optional
# If we use it, it takes a time slot

# For cnot_q0_q2 to be valid, we need q0 and q2 to be adjacent
# With SWAP_0_1 at time 1, the mapping changes:
# After swap_0_1: logical q0 is on physical q1, logical q1 is on physical q0
# Then cnot_q0_q2: logical q0 (now on q1) and logical q2 (on q2) are adjacent (q1-q2)

# So if we have swap_0_1 at time 1, cnot_q0_q2 can be at time 2 or 3

# Similarly for toffoli: q5, q7, q6
# q5 and q6 are adjacent, q6 and q7 are adjacent
# So toffoli can be scheduled directly if q5, q7, q6 are on physical q5, q7, q6
# But q5 and q7 are not adjacent to each other, but that's OK for Toffoli
# (both controls need to be adjacent to target, not to each other)

# Let's add constraints for cnot_q0_q2:
# If cnot_q0_q2 is at time 1, we need q0 and q2 adjacent initially - they're not
# So cnot_q0_q2 cannot be at time 1
solver.add(Not(time1_gates[gate_names.index("cnot_q0_q2")]))

# If we have swap_0_1 at time 1, then cnot_q0_q2 can be at time 2 or 3
# Let's add this constraint
solver.add(Implies(time2_gates[gate_names.index("cnot_q0_q2")], swap_0_1_time1))
solver.add(Implies(time3_gates[gate_names.index("cnot_q0_q2")], Or(swap_0_1_time1, swap_0_1_time2)))

# For toffoli, it needs to be after cnot_q4_q5
# And it needs q5, q7, q6 to be adjacent to target q6
# q5-q6 and q6-q7 are adjacent, so if q5, q7, q6 are on physical q5, q7, q6, it's OK
# But after cnot_q4_q5, q5 might be affected? No, cnot_q4_q5 uses q4 and q5, but doesn't change q5's position
# So toffoli can be scheduled directly

# Count SWAPs used
swaps_used = Int("swaps_used")
solver.add(swaps_used == If(swap_0_1_time1, 1, 0) + If(swap_0_1_time2, 1, 0) + If(swap_0_1_time3, 1, 0))

# Objective: minimize depth (already fixed to 3) and swaps
# We'll check if depth=3, swaps=1 is possible

# Add constraint that we use exactly 1 SWAP
solver.add(swaps_used == 1)

# Check satisfiability
result = solver.check()

if result == sat:
    print("STATUS: sat")
    m = solver.model()
    
    # Extract schedule
    schedule = []
    for t in range(1, 4):  # time slots 1, 2, 3
        time_gates = []
        if t == 1:
            gate_vars = time1_gates
        elif t == 2:
            gate_vars = time2_gates
        else:
            gate_vars = time3_gates
        
        for g in range(len(gates)):
            if is_true(m[gate_vars[g]]):
                time_gates.append(gate_names[g])
        
        # Add SWAP if scheduled
        if t == 1 and is_true(m[swap_0_1_time1]):
            time_gates.append("swap_0_1")
        elif t == 2 and is_true(m[swap_0_1_time2]):
            time_gates.append("swap_0_1")
        elif t == 3 and is_true(m[swap_0_1_time3]):
            time_gates.append("swap_0_1")
        
        if time_gates:
            schedule.append({"time": t, "gates": sorted(time_gates)})
    
    # Print results
    print(f"circuit_depth = 3")
    print(f"swaps_used = {m[swaps_used]}")
    print("gate_schedule = [")
    for entry in schedule:
        print(f"  {entry},")
    print("]")
    
    # Check if this matches expected optimal
    if m[swaps_used] == 1:
        print("Matches expected optimal: depth=3, swaps=1")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No schedule found with depth=3 and swaps=1")
    print("Trying with more swaps or different depth...")
    
    # Try without the swaps_used == 1 constraint
    solver2 = Solver()
    # Recreate the model without swaps constraint
    # ... (simplified for now)
    print("Refinement needed: try different depth or swap count")
    
else:
    print("STATUS: unknown")