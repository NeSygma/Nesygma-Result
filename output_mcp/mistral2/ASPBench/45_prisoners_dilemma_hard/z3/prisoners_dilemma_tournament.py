from z3 import *

# Payoff matrix: payoff[ego_move][opponent_move]
payoff = {
    'C': {'C': 3, 'D': 0},
    'D': {'C': 5, 'D': 1}
}

# Opponent types and their counts
opponent_types = {
    'type_A': 5,  # Always Defect
    'type_B': 3,  # Tit-for-Tat
    'type_C': 2   # Forgiving Tit-for-Tat
}

# Strategy definitions
def get_ego_moves(strategy, opponent_type):
    # Returns a list of Ego's moves for rounds 1 and 2
    if strategy == 'COOP':
        return ['C', 'C']
    elif strategy == 'DEFECT':
        return ['D', 'D']
    elif strategy == 'TFT':
        # Round 1: 'C'
        # Round 2: copy opponent's round 1 move
        if opponent_type == 'type_A':
            opponent_round1 = 'D'
        elif opponent_type == 'type_B':
            opponent_round1 = 'C'
        elif opponent_type == 'type_C':
            opponent_round1 = 'C'
        return ['C', opponent_round1]
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

def get_opponent_moves(opponent_type, ego_round1):
    # Returns a list of opponent's moves for rounds 1 and 2
    if opponent_type == 'type_A':
        return ['D', 'D']
    elif opponent_type == 'type_B':
        # Tit-for-Tat: round 1 is 'C', round 2 copies Ego's round 1
        return ['C', ego_round1]
    elif opponent_type == 'type_C':
        # Forgiving TFT: always 'C'
        return ['C', 'C']
    else:
        raise ValueError(f"Unknown opponent type: {opponent_type}")

def compute_score(ego_moves, opponent_moves):
    # Compute the total score for the two rounds
    score = 0
    for e_move, o_move in zip(ego_moves, opponent_moves):
        score += payoff[e_move][o_move]
    return score

# Compute expected total score for a given Ego strategy
def compute_expected_score(strategy):
    total_score = 0
    for opponent_type, count in opponent_types.items():
        ego_moves = get_ego_moves(strategy, opponent_type)
        opponent_moves = get_opponent_moves(opponent_type, ego_moves[0])
        score = compute_score(ego_moves, opponent_moves)
        total_score += score * count
    return total_score

# Compute scores for all strategies
strategies = ['COOP', 'DEFECT', 'TFT']
expected_scores = []
for strategy in strategies:
    score = compute_expected_score(strategy)
    expected_scores.append((strategy, score))

# Sort by score in descending order
expected_scores.sort(key=lambda x: x[1], reverse=True)

# Find the best strategy
best_strategy = expected_scores[0][0]
best_score = expected_scores[0][1]

# Print results
print("STATUS: sat")
for strategy, score in expected_scores:
    print(f"strategy={strategy}, expected_total_score={score}")
print(f"best_strategy_choice={best_strategy}")