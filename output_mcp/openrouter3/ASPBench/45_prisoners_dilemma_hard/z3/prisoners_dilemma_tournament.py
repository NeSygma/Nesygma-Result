from z3 import *

# Problem parameters
ROUNDS = 2
OPPONENT_POOL = {
    'type_A': 5,  # Always Defect
    'type_B': 3,  # Tit-for-Tat
    'type_C': 2   # Forgiving Tit-for-Tat
}

# Payoff matrix for Ego (row: Ego's action, column: Opponent's action)
# C = Cooperate, D = Defect
PAYOFF = {
    ('C', 'C'): 3,
    ('C', 'D'): 0,
    ('D', 'C'): 5,
    ('D', 'D'): 1
}

# Strategy definitions
def get_ego_actions(strategy, opponent_type, round_num, prev_ego_action=None, prev_opp_action=None):
    """Get Ego's action for a given round based on strategy"""
    if strategy == 'COOP':
        return 'C'
    elif strategy == 'DEFECT':
        return 'D'
    elif strategy == 'TFT':
        if round_num == 1:
            return 'C'
        else:
            # Copy opponent's previous move
            return prev_opp_action if prev_opp_action else 'C'
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

def get_opponent_actions(opponent_type, round_num, prev_ego_action=None, prev_opp_action=None):
    """Get opponent's action for a given round based on opponent type"""
    if opponent_type == 'type_A':
        return 'D'  # Always Defect
    elif opponent_type == 'type_B':
        if round_num == 1:
            return 'C'  # Tit-for-Tat starts with Cooperate
        else:
            # Copy Ego's previous move
            return prev_ego_action if prev_ego_action else 'C'
    elif opponent_type == 'type_C':
        # Forgiving Tit-for-Tat: always Cooperate
        return 'C'
    else:
        raise ValueError(f"Unknown opponent type: {opponent_type}")

def calculate_score(ego_strategy, opponent_type):
    """Calculate total score for 2 rounds against a specific opponent type"""
    total_score = 0
    
    # Round 1
    ego_action_1 = get_ego_actions(ego_strategy, opponent_type, 1)
    opp_action_1 = get_opponent_actions(opponent_type, 1)
    total_score += PAYOFF[(ego_action_1, opp_action_1)]
    
    # Round 2
    ego_action_2 = get_ego_actions(ego_strategy, opponent_type, 2, 
                                   prev_ego_action=ego_action_1, 
                                   prev_opp_action=opp_action_1)
    opp_action_2 = get_opponent_actions(opponent_type, 2, 
                                       prev_ego_action=ego_action_1, 
                                       prev_opp_action=opp_action_1)
    total_score += PAYOFF[(ego_action_2, opp_action_2)]
    
    return total_score

# Calculate expected scores for each strategy
strategies = ['COOP', 'DEFECT', 'TFT']
expected_scores = {}

for strategy in strategies:
    total_expected_score = 0
    for opp_type, count in OPPONENT_POOL.items():
        score_per_matchup = calculate_score(strategy, opp_type)
        total_expected_score += score_per_matchup * count
    expected_scores[strategy] = total_expected_score

# Find the optimal strategy
best_strategy = max(expected_scores, key=expected_scores.get)
best_score = expected_scores[best_strategy]

# Sort strategies by score (descending)
sorted_strategies = sorted(expected_scores.items(), key=lambda x: x[1], reverse=True)

# Print results
print("STATUS: sat")
print(f"best_strategy_choice: {best_strategy}")
print(f"expected_scores: [")
for strategy, score in sorted_strategies:
    print(f"  {{'strategy': '{strategy}', 'expected_total_score': {score}}},")
print("]")

# Additional verification
print("\nDetailed breakdown:")
for strategy in strategies:
    print(f"\n{strategy}:")
    for opp_type, count in OPPONENT_POOL.items():
        score = calculate_score(strategy, opp_type)
        print(f"  vs {opp_type} ({count} opponents): {score} points each = {score * count} total")