from z3 import *

# Generals: G1, G2, G3, G4, G5, G6
# Ranks: G1:3, G2:2, G3:2, G4:1, G5:1, G6:1
# Weights: G1:3, G2:2, G3:2, G4:1, G5:1, G6:1
# Trust: (G1, G2), (G2, G1) -> +1 weight
# Initial Proposals (Round 0): G1:1, G2:1, G3:0, G4:0, G5:1, G6:1

# Traitors: Exactly 2
# Rounds: 2
# Tie-breaking: 0

# Let's model this
# Traitor status: is_traitor[i] (0-indexed, 0 to 5)
# Beliefs: belief[round][general] (round 0, 1, 2)
# Messages: msg[round][sender][receiver] (round 0, 1)

# Ranks:
ranks = [3, 2, 2, 1, 1, 1]
weights = [3, 2, 2, 1, 1, 1]
trust = [[False for _ in range(6)] for _ in range(6)]
trust[0][1] = True
trust[1][0] = True

def get_weight(sender, receiver):
    w = weights[sender]
    if trust[sender][receiver]:
        w += 1
    return w

solver = Solver()
is_traitor = [Bool(f'is_traitor_{i}') for i in range(6)]
solver.add(Sum([If(is_traitor[i], 1, 0) for i in range(6)]) == 2)

# Initial beliefs (Round 0)
initial_proposals = [1, 1, 0, 0, 1, 1]
belief = [[Int(f'belief_{r}_{g}') for g in range(6)] for r in range(3)]

for g in range(6):
    solver.add(belief[0][g] == initial_proposals[g])

# Round 1:
# Honest: send true belief (belief[0][sender])
# Traitor: send lie (1 - belief[0][sender]) to equal/lower rank, truth to higher
# Belief update: weighted majority of received messages
# Received messages in round 1: msg[0][sender][receiver]
msg = [[[Int(f'msg_{r}_{s}_{r_cv}') for r_cv in range(6)] for s in range(6)] for r in range(2)]

for s in range(6):
    for r_cv in range(6):
        if s == r_cv: continue
        # Honest behavior
        is_lie = And(is_traitor[s], ranks[s] <= ranks[r_cv])
        solver.add(msg[0][s][r_cv] == If(is_lie, 1 - belief[0][s], belief[0][s]))

# Update belief[1]
for g in range(6):
    # Weighted majority
    # Sum of weights of messages with value 1
    sum_w1 = Sum([If(msg[0][s][g] == 1, get_weight(s, g), 0) for s in range(6) if s != g])
    sum_w0 = Sum([If(msg[0][s][g] == 0, get_weight(s, g), 0) for s in range(6) if s != g])
    # Tie-breaking: 0
    solver.add(belief[1][g] == If(sum_w1 > sum_w0, 1, 0))

# Round 2:
# Honest: send true belief (belief[1][sender])
# Traitor: send lie (1 - belief[1][sender]) to equal/lower rank, truth to higher
for s in range(6):
    for r_cv in range(6):
        if s == r_cv: continue
        is_lie = And(is_traitor[s], ranks[s] <= ranks[r_cv])
        solver.add(msg[1][s][r_cv] == If(is_lie, 1 - belief[1][s], belief[1][s]))

# Update belief[2]
for g in range(6):
    sum_w1 = Sum([If(msg[1][s][g] == 1, get_weight(s, g), 0) for s in range(6) if s != g])
    sum_w0 = Sum([If(msg[1][s][g] == 0, get_weight(s, g), 0) for s in range(6) if s != g])
    solver.add(belief[2][g] == If(sum_w1 > sum_w0, 1, 0))

# Consensus requirement: All honest generals must agree on the same final value
consensus_val = Int('consensus_val')
for g in range(6):
    solver.add(Implies(Not(is_traitor[g]), belief[2][g] == consensus_val))

if solver.check() == sat:
    m = solver.model()
    print("STATUS: sat")
    traitors = [i+1 for i in range(6) if m.evaluate(is_traitor[i])]
    print(f"Traitors: G{traitors[0]}, G{traitors[1]}")
    print(f"Consensus value: {m.evaluate(consensus_val)}")
    for g in range(6):
        if not m.evaluate(is_traitor[g]):
            print(f"G{g+1} final belief: {m.evaluate(belief[2][g])}")
else:
    print("STATUS: unsat")