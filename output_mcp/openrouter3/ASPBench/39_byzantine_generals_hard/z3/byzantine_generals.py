from z3 import *

# Problem parameters
generals = ["G1", "G2", "G3", "G4", "G5", "G6"]
weights = {"G1": 3, "G2": 2, "G3": 2, "G4": 1, "G5": 1, "G6": 1}
orders = {"G1": 3, "G2": 2, "G3": 2, "G4": 1, "G5": 1, "G6": 1}
initial_proposals = {"G1": 1, "G2": 1, "G3": 0, "G4": 0, "G5": 1, "G6": 1}

# Trust network: high trust pairs with +1 bonus
trust_pairs = [("G1", "G2"), ("G2", "G1")]
trust_bonus = 1

# Number of rounds
ROUNDS = 2

# Create solver
solver = Solver()

# 1. Traitor identification variables
traitors = {g: Bool(f"traitor_{g}") for g in generals}

# Exactly 2 traitors
solver.add(Sum([If(traitors[g], 1, 0) for g in generals]) == 2)

# 2. Belief variables for each round and each general
# beliefs[round][general] = belief value (0 or 1)
beliefs = {}
for r in range(ROUNDS + 1):  # Round 0 to ROUNDS
    beliefs[r] = {}
    for g in generals:
        beliefs[r][g] = Int(f"belief_r{r}_{g}")
        solver.add(Or(beliefs[r][g] == 0, beliefs[r][g] == 1))

# Initial beliefs (Round 0) are the initial proposals
for g in generals:
    solver.add(beliefs[0][g] == initial_proposals[g])

# 3. Message passing simulation for each round
for r in range(ROUNDS):
    # For each receiver, collect messages from all senders
    for receiver in generals:
        # List of (message_value, weight) pairs
        messages = []
        
        for sender in generals:
            if sender == receiver:
                continue  # Skip self-messages
                
            # Determine what message is sent based on sender's traitor status and rank comparison
            sender_traitor = traitors[sender]
            sender_order = orders[sender]
            receiver_order = orders[receiver]
            
            # Truth value: sender's belief in previous round
            truth_value = beliefs[r][sender]
            
            # Lie value: opposite of truth
            lie_value = If(truth_value == 0, 1, 0)
            
            # Deception rule: traitors lie to equal/lower rank, tell truth to higher rank
            # Higher rank means higher order value
            is_higher_rank = receiver_order > sender_order
            
            # Message sent: if traitor and not higher rank, send lie; otherwise truth
            message_value = If(sender_traitor, 
                               If(is_higher_rank, truth_value, lie_value),
                               truth_value)
            
            # Calculate weight: rank weight + trust bonus if trusted
            base_weight = weights[sender]
            is_trusted = Or([And(sender == s, receiver == r) for s, r in trust_pairs])
            total_weight = If(is_trusted, base_weight + trust_bonus, base_weight)
            
            messages.append((message_value, total_weight))
        
        # Calculate weighted majority
        # We need to sum weights for value 0 and value 1 separately
        weight_0 = Sum([If(msg_val == 0, w, 0) for msg_val, w in messages])
        weight_1 = Sum([If(msg_val == 1, w, 0) for msg_val, w in messages])
        
        # Update belief: if receiver is honest, take weighted majority
        # If receiver is traitor, they can choose any belief (we'll model this as unconstrained)
        receiver_honest = Not(traitors[receiver])
        
        # For honest receivers: belief becomes 1 if weight_1 > weight_0, else 0
        # For tie-breaking: defaults to 0
        # We'll use: belief = 1 if weight_1 > weight_0, else 0
        solver.add(Implies(receiver_honest,
                          beliefs[r+1][receiver] == If(weight_1 > weight_0, 1, 0)))

# 4. Consensus requirement: all honest generals must agree on final belief
final_round = ROUNDS
honest_generals = [g for g in generals]
consensus_value = Int("consensus_value")
solver.add(Or(consensus_value == 0, consensus_value == 1))

for g in generals:
    solver.add(Implies(Not(traitors[g]), 
                      beliefs[final_round][g] == consensus_value))

# 5. Additional constraints to ensure meaningful solution
# Traitors can have any belief (no constraints on their final beliefs)

# Check and print results
print("Solving Byzantine Generals Problem...")
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Identify traitors
    traitor_list = []
    honest_list = []
    for g in generals:
        if is_true(model[traitors[g]]):
            traitor_list.append(g)
        else:
            honest_list.append(g)
    
    print(f"Traitors: {traitor_list}")
    print(f"Honest generals: {honest_list}")
    
    # Get consensus value
    consensus = model[consensus_value]
    print(f"Consensus value: {consensus}")
    
    # Get final beliefs of honest generals
    print("Final beliefs of honest generals:")
    final_beliefs = []
    for g in honest_list:
        belief = model[beliefs[final_round][g]]
        print(f"  {g}: {belief}")
        final_beliefs.append({"general": g, "belief": int(str(belief))})
    
    # Verify consensus
    all_agree = all(belief["belief"] == int(str(consensus)) for belief in final_beliefs)
    print(f"All honest generals agree: {all_agree}")
    
    # Print in required format
    print(f"\nconsensus_value: {int(str(consensus))}")
    print("final_beliefs:")
    for belief in final_beliefs:
        print(f"  - general: {belief['general']}, belief: {belief['belief']}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No valid assignment found - problem may be unsatisfiable")
else:
    print("STATUS: unknown")
    print("Solver returned unknown result")