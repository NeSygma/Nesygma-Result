from z3 import *

# ============================================================================
# Problem Constants
# ============================================================================

# Generals: names, ranks, weights, and initial proposals
# Rank order: commander (highest) > lieutenant > sergeant (lowest)
# Weights are used for weighted majority
# Order is for rank comparison (higher order = higher rank)

GENERALS = [
    ("G1", "commander", 3, 3, 1),  # (name, rank, weight, order, initial_belief)
    ("G2", "lieutenant", 2, 2, 1),
    ("G3", "lieutenant", 2, 2, 0),
    ("G4", "sergeant", 1, 1, 0),
    ("G5", "sergeant", 1, 1, 1),
    ("G6", "sergeant", 1, 1, 1),
]

# Trust network: pairs with high trust (+1 bonus)
TRUST_PAIRS = [("G1", "G2"), ("G2", "G1")]

# Protocol parameters
NUM_TRAITORS = 2
NUM_ROUNDS = 2

# ============================================================================
# Z3 Model
# ============================================================================

solver = Solver()

# ----------------------------------------------------------------------------
# Decision Variables
# ----------------------------------------------------------------------------

# is_traitors[g]: True if general g is a traitor
is_traitors = {name: Bool(f"is_traitor_{name}") for name, _, _, _, _ in GENERALS}

# beliefs[g][r]: belief of general g at round r (0 or 1)
# We'll use Int for beliefs to allow arithmetic in weighted sums
beliefs = {}
for name, _, _, _, init_belief in GENERALS:
    beliefs[name] = [Int(f"belief_{name}_r{r}") for r in range(NUM_ROUNDS + 1)]

# ----------------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------------

def get_rank_order(name):
    """Return the rank order of a general."""
    for g_name, _, _, order, _ in GENERALS:
        if g_name == name:
            return order
    raise ValueError(f"Unknown general: {name}")

def get_weight(name):
    """Return the base weight of a general."""
    for g_name, _, weight, _, _ in GENERALS:
        if g_name == name:
            return weight
    raise ValueError(f"Unknown general: {name}")

def is_higher_rank(sender, receiver):
    """Return True if sender has higher rank than receiver."""
    s_order = get_rank_order(sender)
    r_order = get_rank_order(receiver)
    return s_order > r_order

def has_trust_bonus(sender, receiver):
    """Return True if the pair has a trust bonus."""
    return (sender, receiver) in TRUST_PAIRS or (receiver, sender) in TRUST_PAIRS

# ----------------------------------------------------------------------------
# Initial Beliefs (Round 0)
# ----------------------------------------------------------------------------

for name, _, _, _, init_belief in GENERALS:
    solver.add(beliefs[name][0] == init_belief)

# ----------------------------------------------------------------------------
# Exactly 2 Traitors
# ----------------------------------------------------------------------------

solver.add(Sum([If(is_traitors[name], 1, 0) for name, _, _, _, _ in GENERALS]) == NUM_TRAITORS)

# ----------------------------------------------------------------------------
# Message Passing and Belief Update for Each Round
# ----------------------------------------------------------------------------

# We need to model the message each sender sends to each receiver in each round
# For honest receivers, we compute the weighted sum of received messages
# For traitor receivers, we don't care about their belief updates

for r in range(1, NUM_ROUNDS + 1):  # For rounds 1 and 2
    for receiver, _, _, _, _ in GENERALS:
        # Only honest receivers update their beliefs based on received messages
        # Traitors may keep arbitrary beliefs
        solver.add(Implies(Not(is_traitors[receiver]), 
                           beliefs[receiver][r] == beliefs[receiver][r-1]))  # Placeholder for actual update
        
        # For honest receivers, compute weighted sum of received messages
        # We need to model what message each sender sends to this receiver
        received_values = []  # Will hold Int expressions for weighted sum
        
        for sender, _, _, _, _ in GENERALS:
            # Determine what message sender sends to receiver in this round
            # If sender is honest, they send their true belief from previous round
            # If sender is traitor, they lie to equal/lower rank, tell truth to higher rank
            
            # Convert Int belief to Bool for logical operations
            sender_belief_r0 = beliefs[sender][r-1] == 1
            sender_belief_r0_bool = sender_belief_r0  # This is already a Bool expression
            
            # Traitors lie to equal or lower rank, tell truth to higher rank
            sender_is_traitors = is_traitors[sender]
            sender_lies = And(sender_is_traitors, 
                              Not(is_higher_rank(sender, receiver)))
            
            # Message sent: If sender lies, send opposite of belief; else send true belief
            # We need to convert the Int belief to a Bool for Not operation
            sender_belief_bool = beliefs[sender][r-1] == 1
            opposite_belief_bool = Not(sender_belief_bool)
            true_belief_bool = sender_belief_bool
            
            message_sent = If(sender_lies, 
                              If(opposite_belief_bool, 1, 0),  # Convert Bool to Int
                              If(true_belief_bool, 1, 0))  # Convert Bool to Int
            
            # Weight: base weight + trust bonus if applicable
            base_weight = get_weight(sender)
            trust_bonus = If(has_trust_bonus(sender, receiver), 1, 0)
            total_weight = base_weight + trust_bonus
            
            # Only count if receiver is honest (traitors don't update beliefs)
            # We add the weighted message to the sum
            received_values.append(If(Not(is_traitors[receiver]), 
                                      message_sent * total_weight, 
                                      0))
        
        # Honest receiver updates belief based on weighted majority
        # We model this as: belief = 1 if weighted sum of 1s >= weighted sum of 0s
        total_weighted_sum = Sum(received_values)
        # For honest receivers, set the new belief based on weighted majority
        solver.add(Implies(Not(is_traitors[receiver]), 
                           beliefs[receiver][r] == If(total_weighted_sum >= 0, 1, 0)))

# ----------------------------------------------------------------------------
# Consensus: All honest generals have the same final belief
# ----------------------------------------------------------------------------

# Enforce pairwise equality for honest generals
for i in range(len(GENERALS)):
    for j in range(i+1, len(GENERALS)):
        name_i, _, _, _, _ = GENERALS[i]
        name_j, _, _, _, _ = GENERALS[j]
        solver.add(Implies(And(Not(is_traitors[name_i]), Not(is_traitors[name_j])),
                           beliefs[name_i][NUM_ROUNDS] == beliefs[name_j][NUM_ROUNDS]))

# ----------------------------------------------------------------------------
# BENCHMARK_MODE: ON (problem is guaranteed solvable)
# ----------------------------------------------------------------------------
BENCHMARK_MODE = True

# ----------------------------------------------------------------------------
# Solve
# ----------------------------------------------------------------------------
result = solver.check()

# ----------------------------------------------------------------------------
# Output Results
# ----------------------------------------------------------------------------

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Extract traitors
    traitors = []
    for name, _, _, _, _ in GENERALS:
        if is_true(model[is_traitors[name]]):
            traitors.append(name)
    print(f"Traitors: {traitors}")
    
    # Extract final beliefs of honest generals
    final_beliefs_dict = {}
    for name, _, _, _, _ in GENERALS:
        if name not in traitors:
            final_beliefs_dict[name] = model[beliefs[name][NUM_ROUNDS]]
    
    print("Final beliefs of honest generals:")
    for name, belief in final_beliefs_dict.items():
        print(f"  {name}: {belief}")
    
    # Extract consensus value (value agreed upon by all honest generals)
    # Since all honest generals have the same final belief, we can use any
    consensus_value = model[beliefs[list(final_beliefs_dict.keys())[0]][NUM_ROUNDS]]
    print(f"Consensus value: {consensus_value}")
    
    # Print final_beliefs in required format
    print("final_beliefs:")
    for name in final_beliefs_dict.keys():
        print(f"  - general: {name}")
        print(f"    belief: {model[beliefs[name][NUM_ROUNDS]]}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")