from z3 import *

# Define the problem parameters
N = 6  # number of generals
ROUNDS = 2  # number of message exchange rounds (1 and 2)

# Generals: G1, G2, G3, G4, G5, G6
# Index mapping: 0=G1, 1=G2, 2=G3, 3=G4, 4=G5, 5=G6
generals = ["G1", "G2", "G3", "G4", "G5", "G6"]

# Ranks and weights (higher rank = higher authority)
# G1: commander, rank 3, weight 3
# G2, G3: lieutenant, rank 2, weight 2  
# G4, G5, G6: sergeant, rank 1, weight 1
ranks = [3, 2, 2, 1, 1, 1]
weights = [3, 2, 2, 1, 1, 1]

# Initial proposals (round 0)
initial_beliefs = [1, 1, 0, 0, 1, 1]

# Trust network: (G1, G2) and (G2, G1) have high trust
# Trust bonus: +1 weight
trust_pairs = [(0, 1), (1, 0)]  # indices for (G1, G2) and (G2, G1)

# Create solver
solver = Solver()

# ===== VARIABLES =====

# is_traitor[i] = True if general i is a traitor
is_traitor = [Bool(f"is_traitor_{i}") for i in range(N)]

# belief[i][r] = belief of general i at round r (0, 1, 2)
# Round 0 is fixed (initial proposals)
belief = [[Int(f"belief_{i}_r{r}") for r in range(ROUNDS + 1)] for i in range(N)]

# message_sent[i][j][r] = message sent from i to j at round r (1 or 2)
message_sent = [[[Int(f"msg_sent_{i}_{j}_r{r}") for r in range(1, ROUNDS + 1)] 
                 for j in range(N)] for i in range(N)]

# ===== CONSTRAINTS =====

# 1. Exactly 2 traitors
solver.add(Sum([If(is_traitor[i], 1, 0) for i in range(N)]) == 2)

# 2. Initial beliefs are fixed
for i in range(N):
    solver.add(belief[i][0] == initial_beliefs[i])

# 3. Message passing and belief update for each round
for r in range(1, ROUNDS + 1):
    # For each sender i
    for i in range(N):
        # For each receiver j (j != i)
        for j in range(N):
            if i == j:
                continue
                
            # Determine what message i sends to j at round r
            # Based on whether i is traitor and rank comparison
            
            # Rank comparison: is i higher/equal rank than j?
            rank_i_ge_j = (ranks[i] >= ranks[j])
            
            # If honest: send true belief from previous round
            # If traitor: send lie (opposite) to equal/lower rank, truth to higher rank
            honest_msg = belief[i][r-1]
            traitor_lie = 1 - belief[i][r-1]  # opposite of belief
            
            # Message is honest_msg if (not traitor) OR (traitor AND rank_i < rank_j)
            # Message is traitor_lie if (traitor AND rank_i >= rank_j)
            msg_value = If(Or(Not(is_traitor[i]), 
                             And(is_traitor[i], Not(rank_i_ge_j))),
                          honest_msg,
                          traitor_lie)
            
            solver.add(message_sent[i][j][r-1] == msg_value)
    
    # For each receiver j, update belief based on weighted majority of received messages
    for j in range(N):
        # Calculate weighted sum of messages that are 1 and 0
        weighted_sum_1 = 0
        weighted_sum_0 = 0
        
        for i in range(N):
            if i == j:
                continue
                
            # Weight for message from i to j
            weight = weights[i]
            # Add trust bonus if (j, i) is a trust pair
            if (j, i) in trust_pairs:
                weight += 1
            
            msg = message_sent[i][j][r-1]
            
            # Add to weighted sums
            weighted_sum_1 += If(msg == 1, weight, 0)
            weighted_sum_0 += If(msg == 0, weight, 0)
        
        # Update belief based on weighted majority
        # If weighted_sum_1 > weighted_sum_0: belief = 1
        # If weighted_sum_1 < weighted_sum_0: belief = 0  
        # If equal: tie-breaking rule says default to 0
        new_belief = If(weighted_sum_1 > weighted_sum_0, 1, 0)
        solver.add(belief[j][r] == new_belief)

# 4. Consensus requirement: all honest generals must agree on same final value
final_value = Int("final_consensus_value")
for i in range(N):
    solver.add(Implies(Not(is_traitor[i]), belief[i][ROUNDS] == final_value))

# ===== CHECK AND PRINT RESULTS =====
print("Solving Byzantine Generals problem...")
result = solver.check()

if result == sat:
    print("STATUS: sat")
    model = solver.model()
    
    # Identify traitors using model evaluation
    traitors = []
    honest = []
    for i in range(N):
        is_traitor_val = model.eval(is_traitor[i])
        if is_traitor_val:
            traitors.append(generals[i])
        else:
            honest.append(generals[i])
    
    print(f"Traitors: {traitors}")
    print(f"Honest: {honest}")
    
    # Get final consensus value
    consensus = model.eval(final_value)
    print(f"Consensus value: {consensus}")
    
    # Get final beliefs of honest generals
    print("Final beliefs of honest generals:")
    final_beliefs = []
    for i in range(N):
        is_traitor_val = model.eval(is_traitor[i])
        if not is_traitor_val:
            belief_val = model.eval(belief[i][ROUNDS])
            print(f"  {generals[i]}: {belief_val}")
            final_beliefs.append({"general": generals[i], "belief": int(str(belief_val))})
    
    # Print in required format
    print(f"\nconsensus_value: {consensus}")
    print(f"final_beliefs: {final_beliefs}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No solution found - problem may be unsatisfiable")
else:
    print("STATUS: unknown")
    print("Solver returned unknown result")