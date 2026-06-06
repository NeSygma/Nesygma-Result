from z3 import *

# ============================================================
# Byzantine Generals with Hierarchy and Deception
# ============================================================

# Generals data
generals = ["G1", "G2", "G3", "G4", "G5", "G6"]
N = len(generals)

# Ranks: commander=3, lieutenant=2, sergeant=1
rank = {"G1": 3, "G2": 2, "G3": 2, "G4": 1, "G5": 1, "G6": 1}

# Weights (rank weight)
weight = {"G1": 3, "G2": 2, "G3": 2, "G4": 1, "G5": 1, "G6": 1}

# Initial proposals (Round 0)
initial = {"G1": 1, "G2": 1, "G3": 0, "G4": 0, "G5": 1, "G6": 1}

# Trust network: high trust pairs
trust_pairs = [("G1", "G2"), ("G2", "G1")]
trust_bonus = 1

# Number of traitors = 2
# Number of rounds = 2
# Tie-breaking: defaults to 0

solver = Solver()

# ============================================================
# Variables
# ============================================================

# traitor[i] = True if general i is a traitor
traitor = [Bool(f"traitor_{g}") for g in generals]

# belief[i][r] = belief of general i at round r (0 = initial, 1 = after round 1, 2 = after round 2)
belief = [[Int(f"belief_{g}_r{r}") for r in range(3)] for g in generals]

# ============================================================
# Constraints
# ============================================================

# Beliefs are binary (0 or 1)
for i in range(N):
    for r in range(3):
        solver.add(Or(belief[i][r] == 0, belief[i][r] == 1))

# Initial beliefs (Round 0)
for i, g in enumerate(generals):
    solver.add(belief[i][0] == initial[g])

# Exactly 2 traitors
solver.add(Sum([If(traitor[i], 1, 0) for i in range(N)]) == 2)

# ============================================================
# Message passing and belief update for Round 1 and Round 2
# ============================================================

for r in range(2):  # rounds: 0->1, 1->2
    for j_idx, j in enumerate(generals):
        weight_sum_1 = []
        weight_sum_0 = []
        
        for i_idx, i in enumerate(generals):
            base_w = weight[i]
            if (i, j) in trust_pairs:
                w = base_w + trust_bonus
            else:
                w = base_w
            
            # Message value from i to j
            # honest case: msg = belief[i][r]
            # traitor case: if rank[i] <= rank[j]: msg = 1 - belief[i][r]; else: msg = belief[i][r]
            
            honest_msg = belief[i_idx][r]
            traitor_msg = If(rank[i] <= rank[j], 1 - belief[i_idx][r], belief[i_idx][r])
            msg = If(traitor[i_idx], traitor_msg, honest_msg)
            
            # Add weight to appropriate sum
            weight_sum_1.append(If(msg == 1, w, 0))
            weight_sum_0.append(If(msg == 0, w, 0))
        
        total_w1 = Sum(weight_sum_1)
        total_w0 = Sum(weight_sum_0)
        
        # Honest general j updates belief based on weighted majority
        # If total_w1 > total_w0: belief = 1
        # If total_w0 > total_w1: belief = 0
        # If tie: defaults to 0
        
        solver.add(Implies(Not(traitor[j_idx]),
            Or(
                And(total_w1 > total_w0, belief[j_idx][r+1] == 1),
                And(total_w0 > total_w1, belief[j_idx][r+1] == 0),
                And(total_w1 == total_w0, belief[j_idx][r+1] == 0)
            )
        ))

# ============================================================
# Consensus requirement: All honest generals must agree on the same final value after round 2
# ============================================================

for i in range(N):
    for j in range(i+1, N):
        solver.add(Implies(And(Not(traitor[i]), Not(traitor[j])), belief[i][2] == belief[j][2]))

# ============================================================
# Solve
# ============================================================

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    
    # Identify traitors
    traitors_list = []
    for i, g in enumerate(generals):
        if is_true(m[traitor[i]]):
            traitors_list.append(g)
    
    # Get final beliefs of honest generals
    honest_beliefs = []
    for i, g in enumerate(generals):
        if not is_true(m[traitor[i]]):
            b = m[belief[i][2]].as_long()
            honest_beliefs.append((g, b))
    
    # Consensus value
    consensus = honest_beliefs[0][1] if honest_beliefs else None
    
    print("STATUS: sat")
    print(f"Traitors: {traitors_list}")
    print(f"Consensus value: {consensus}")
    print("Final beliefs (honest generals):")
    for g, b in honest_beliefs:
        print(f"  {g}: {b}")
    
    # Also print all beliefs for debugging
    print("\nAll beliefs:")
    for i, g in enumerate(generals):
        is_t = is_true(m[traitor[i]])
        b0 = m[belief[i][0]].as_long()
        b1 = m[belief[i][1]].as_long()
        b2 = m[belief[i][2]].as_long()
        print(f"  {g} (traitor={is_t}): r0={b0}, r1={b1}, r2={b2}")
        
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")