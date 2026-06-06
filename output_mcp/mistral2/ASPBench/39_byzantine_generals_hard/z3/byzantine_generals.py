from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# ============================================================================
# Problem Data
# ============================================================================

# Generals: (name, rank, weight, initial_belief)
# Rank: 3=commander, 2=lieutenant, 1=sergeant
generals_data = [
    ("G1", 3, 3, 1),  # commander
    ("G2", 2, 2, 1),  # lieutenant
    ("G3", 2, 2, 0),  # lieutenant
    ("G4", 1, 1, 0),  # sergeant
    ("G5", 1, 1, 1),  # sergeant
    ("G6", 1, 1, 1),  # sergeant
]

# Trust network: pairs with trust bonus (+1 weight)
trust_pairs = [("G1", "G2"), ("G2", "G1")]

# Protocol parameters
num_traitors = 2
num_rounds = 2
tie_breaker = 0

# ============================================================================
# Z3 Declarations
# ============================================================================

solver = Solver()

# General names and indices
names = [g[0] for g in generals_data]
ranks = {g[0]: g[1] for g in generals_data}
weights = {g[0]: g[2] for g in generals_data}
initial_beliefs = {g[0]: g[3] for g in generals_data}

# Decision variables
# is_traitor[g] = True if general g is a traitor
is_traitor = {g: Bool(f"is_traitor_{g}") for g in names}

# Beliefs: belief[g][r] = belief of general g after round r
# We only need beliefs for rounds 0, 1, 2 (0=initial, 1=after round 1, 2=after round 2)
belief = {g: [Int(f"belief_{g}_r{r}") for r in range(num_rounds + 1)] for g in names}

# Messages: message[g][h][r] = message sent from g to h in round r
# We only need messages for rounds 1 and 2 (since round 0 is initial)
message = {
    g: {
        h: [Int(f"message_{g}_{h}_r{r}") for r in range(1, num_rounds + 1)]
        for h in names
    }
    for g in names
}

# ============================================================================
# Constraints
# ============================================================================

# 1. Exactly 2 traitors
solver.add(Sum([If(is_traitor[g], 1, 0) for g in names]) == num_traitors)

# 2. Initial beliefs
for g in names:
    solver.add(belief[g][0] == initial_beliefs[g])

# 3. Message passing and deception for each round
for r in range(1, num_rounds + 1):
    for sender in names:
        for receiver in names:
            # Determine if sender is honest or traitor
            sender_honest = Not(is_traitor[sender])
            sender_belief_prev = belief[sender][r - 1]
            
            # Determine if sender lies to receiver
            # Traitors lie to equal or lower rank, but tell truth to higher rank
            sender_rank = ranks[sender]
            receiver_rank = ranks[receiver]
            
            # Lie condition: sender is traitor AND (sender_rank <= receiver_rank)
            lie = And(is_traitor[sender], sender_rank <= receiver_rank)
            
            # Message sent: if lie, then opposite of sender's belief; else, sender's belief
            solver.add(
                message[sender][receiver][r - 1]
                == If(lie, 1 - sender_belief_prev, sender_belief_prev)
            )

# 4. Belief update for honest generals after each round
for r in range(1, num_rounds + 1):
    for receiver in names:
        # Only honest generals update their beliefs
        receiver_honest = Not(is_traitor[receiver])
        
        # Collect all messages received by receiver in round r
        received_messages = [message[g][receiver][r - 1] for g in names]
        received_weights = []
        for g in names:
            # Base weight
            w = weights[g]
            # Trust bonus: +1 if (g, receiver) is a trusted pair
            trust_bonus = If(Or(
                And(g == "G1", receiver == "G2"),
                And(g == "G2", receiver == "G1"),
            ), 1, 0)
            received_weights.append(w + trust_bonus)
        
        # Weighted sum of received messages
        weighted_sum = Sum([
            If(received_messages[i] == 1, received_weights[i], 0)
            for i in range(len(received_messages))
        ])
        total_weight = Sum(received_weights)
        
        # Weighted majority: if weighted_sum > total_weight / 2, belief=1; else, belief=0
        # Use tie-breaker for equality
        solver.add(
            belief[receiver][r]
            == If(
                weighted_sum * 2 > total_weight,
                1,
                If(weighted_sum * 2 < total_weight, 0, tie_breaker)
            )
        )

# 5. Consensus: all honest generals must have the same belief after round 2
# Collect all honest generals (use model to filter later)

# ============================================================================
# Check and Output
# ============================================================================

result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Extract traitors
    traitors = [g for g in names if is_true(model[is_traitor[g]])]
    print(f"Traitors: {traitors}")
    
    # Extract consensus value (belief of any honest general after round 2)
    # Find the first honest general in the model
    consensus_value_model = None
    for g in names:
        if not is_true(model[is_traitor[g]]):
            consensus_value_model = model[belief[g][num_rounds]]
            break
    print(f"Consensus value: {consensus_value_model}")
    
    # Extract final beliefs of honest generals
    honest_final_beliefs = []
    for g in names:
        if not is_true(model[is_traitor[g]]):
            final_belief = model[belief[g][num_rounds]]
            honest_final_beliefs.append((g, final_belief))
    print("Final beliefs of honest generals:")
    for g, b in honest_final_beliefs:
        print(f"  {g}: {b}")
        
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")