from z3 import *

# Problem: 2x4 grid topology
adj = [
    (0,1), (1,0), (1,2), (2,1), (2,3), (3,2),
    (4,5), (5,4), (5,6), (6,5), (6,7), (7,6),
    (0,4), (4,0), (1,5), (5,1), (2,6), (6,2), (3,7), (7,3)
]

def is_adj(u, v):
    return (u, v) in adj

def solve(T):
    opt = Optimize()
    
    # map[L][t] = physical position of logical qubit L at time t
    mapping = [[Int(f"map_{l}_{t}") for t in range(T+1)] for l in range(8)]
    
    for t in range(T+1):
        opt.add(Distinct([mapping[l][t] for l in range(8)]))
        for l in range(8):
            opt.add(mapping[l][t] >= 0, mapping[l][t] <= 7)
            
    for l in range(8):
        opt.add(mapping[l][0] == l)
        
    # swaps[p1][p2][t] = true if swap between p1 and p2 at time t
    swaps = [[[Bool(f"swap_{p1}_{p2}_{t}") for t in range(T)] for p2 in range(8)] for p1 in range(8)]
    
    for t in range(T):
        for p1 in range(8):
            for p2 in range(8):
                if p1 >= p2: continue
                if not is_adj(p1, p2):
                    opt.add(Not(swaps[p1][p2][t]))
        
        for p in range(8):
            opt.add(Sum([If(Or(swaps[p][p2][t] if p < p2 else swaps[p2][p][t]), 1, 0) for p2 in range(8) if p != p2]) <= 1)
            
    # Mapping update
    for t in range(T):
        for l in range(8):
            p_prev = mapping[l][t]
            p_next = mapping[l][t+1]
            
            # p_next = p_prev + sum_{p2 != p_prev} (If(swap(p_prev, p2) or swap(p2, p_prev), p2 - p_prev, 0))
            # To avoid symbolic indexing, use Or-loop
            
            # p_next is p_prev if no swap involving p_prev
            # p_next is p2 if swap(p_prev, p2)
            
            # Let's define p_next using a sum over all possible physical positions
            # p_next = sum_{p in 0..7} (If(p_prev == p, (p + sum_{p2 != p} (If(swap(p, p2) or swap(p2, p), p2 - p, 0))), 0))
            
            delta = Sum([If(p_prev == p, Sum([If(Or(swaps[p][p2][t] if p < p2 else swaps[p2][p][t]), p2 - p, 0) for p2 in range(8) if p2 != p]), 0) for p in range(8)])
            opt.add(p_next == p_prev + delta)

    # Gates
    gate_list = [
        ("h", [0], 1),
        ("x", [1], 1),
        ("cnot", [2, 3], 2),
        ("cnot", [4, 5], 2),
        ("cnot", [0, 2], 2),
        ("toffoli", [5, 7, 6], 3)
    ]
    
    gate_times = [Int(f"gate_time_{i}") for i in range(len(gate_list))]
    for t_g in gate_times:
        opt.add(t_g >= 1, t_g <= T)
        
    opt.add(gate_times[3] < gate_times[5])
    
    for i, (g_type, q_list, _) in enumerate(gate_list):
        t_g = gate_times[i]
        for t in range(1, T+1):
            is_at_t = (t_g == t)
            
            if len(q_list) == 2:
                p1 = mapping[q_list[0]][t]
                p2 = mapping[q_list[1]][t]
                opt.add(Implies(is_at_t, Or([And(p1 == u, p2 == v) for (u, v) in adj])))
            elif len(q_list) == 3:
                p1 = mapping[q_list[0]][t]
                p2 = mapping[q_list[1]][t]
                p3 = mapping[q_list[2]][t]
                opt.add(Implies(is_at_t, And(Or([And(p1 == u, p3 == v) for (u, v) in adj]),
                                            Or([And(p2 == u, p3 == v) for (u, v) in adj]))))
                                            
    for t in range(1, T+1):
        used_qubits = []
        for i, (g_type, q_list, _) in enumerate(gate_list):
            is_at_t = (gate_times[i] == t)
            for q in q_list:
                used_qubits.append(If(is_at_t, mapping[q][t], -1))
        
        for i in range(len(used_qubits)):
            for j in range(i + 1, len(used_qubits)):
                opt.add(Implies(And(used_qubits[i] != -1, used_qubits[j] != -1), used_qubits[i] != used_qubits[j]))
                
    total_swaps = Sum([If(swaps[p1][p2][t], 1, 0) for p1 in range(8) for p2 in range(8) for t in range(T) if p1 < p2])
    opt.minimize(total_swaps)
    
    if opt.check() == sat:
        return opt.model(), total_swaps
    return None, None

for T in range(3, 6):
    model, swaps = solve(T)
    if model:
        print(f"STATUS: sat")
        print(f"Depth: {T}")
        print(f"Swaps: {model.evaluate(swaps)}")
        break