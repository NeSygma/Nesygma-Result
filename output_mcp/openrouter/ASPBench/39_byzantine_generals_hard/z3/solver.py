from z3 import *

# Data
names = ['G1','G2','G3','G4','G5','G6']
order = {'G1':3,'G2':2,'G3':2,'G4':1,'G5':1,'G6':1}
weight = {'G1':3,'G2':2,'G3':2,'G4':1,'G5':1,'G6':1}
trust_pairs = {('G1','G2'),('G2','G1')}  # bidirectional trust

def trust_bonus(i,j):
    return 1 if (i,j) in trust_pairs else 0

# Variables
traitor = {n: Bool(f"traitor_{n}") for n in names}
# belief[n][r] for r=0,1,2
belief = {(n,r): Int(f"belief_{n}_{r}") for n in names for r in range(3)}

s = Solver()
# Initial proposals round 0
init = {'G1':1,'G2':1,'G3':0,'G4':0,'G5':1,'G6':1}
for n in names:
    s.add(belief[(n,0)] == init[n])
    for r in range(3):
        s.add(Or(belief[(n,r)] == 0, belief[(n,r)] == 1))

# Exactly two traitors
s.add(Sum([If(traitor[n],1,0) for n in names]) == 2)

# Precompute total incoming weight for each receiver (excluding self)
total_in_weight = {}
for i in names:
    total = sum(weight[j] + trust_bonus(j,i) for j in names if j != i)
    total_in_weight[i] = total

# Message function: message from i to j at round r (r=1,2) based on belief at r-1
message = {}
for r in [1,2]:
    for i in names:
        for j in names:
            if i == j:
                continue
            b_prev = belief[(i, r-1)]
            # Determine if i lies to j (traitor case)
            # Lie when j's rank <= i's rank (equal or lower rank)
            lie_expr = If(order[j] <= order[i], 1 - b_prev, b_prev)
            msg = If(traitor[i], lie_expr, b_prev)
            message[(i,j,r)] = msg

# Update beliefs for honest generals for rounds 1 and 2
for r in [1,2]:
    for i in names:
        # Only constrain honest generals' belief update
        # Compute weighted sum of received 1 messages
        weighted_one_sum = Sum([
            (weight[j] + trust_bonus(j,i)) * If(message[(j,i,r)] == 1, 1, 0)
            for j in names if j != i
        ])
        # Apply majority rule with tie-breaking to 0
        new_belief = If(2*weighted_one_sum > total_in_weight[i], 1, 0)
        s.add(Implies(Not(traitor[i]), belief[(i,r)] == new_belief))
        # Traitors' belief can be anything (no constraint)

# Consensus requirement: all honest generals have same belief after round 2
for i in names:
    for j in names:
        if i < j:
            s.add(Implies(And(Not(traitor[i]), Not(traitor[j])), belief[(i,2)] == belief[(j,2)]))

# Solve
res = s.check()
if res == sat:
    m = s.model()
    traitors = [n for n in names if is_true(m.eval(traitor[n]))]
    # consensus value from any honest general
    consensus = None
    for n in names:
        if not is_true(m.eval(traitor[n])):
            consensus = m.eval(belief[(n,2)])
            break
    print("STATUS: sat")
    print("traitors =", traitors)
    print("consensus_value =", consensus)
    for n in names:
        if not is_true(m.eval(traitor[n])):
            print(f"{n}: belief = {m.eval(belief[(n,2)])}")
else:
    print("STATUS: unsat")