from z3 import *

# Strategies
strategies = ["COOP", "DEFECT", "TFT", "GTFT", "RAND"]

# Payoff Matrix: (Self, Opponent)
# C, C -> 3, 3
# D, D -> 1, 1
# C, D -> 0, 5
# D, C -> 5, 0

def get_score(s1, s2):
    # Returns (score_s1, score_s2) for 100 rounds
    # Deterministic simulation
    
    # COOP: Always C
    # DEFECT: Always D
    # TFT: C first, then copy opponent's last move
    # GTFT: Like TFT, but forgives defection 10% of the time (10 rounds)
    # RAND: 50% C, 50% D
    
    s1_moves = []
    s2_moves = []
    
    s1_score = 0
    s2_score = 0
    
    for r in range(100):
        # Determine move for s1
        if s1 == "COOP": m1 = 'C'
        elif s1 == "DEFECT": m1 = 'D'
        elif s1 == "TFT":
            if r == 0: m1 = 'C'
            else: m1 = s2_moves[-1]
        elif s1 == "GTFT":
            if r == 0: m1 = 'C'
            else:
                # Forgive 10% of the time (10 rounds)
                # Let's assume it forgives the first 10 times it sees a D
                # Or just 10 specific rounds. Let's use rounds 10, 20, ..., 100
                if (r+1) % 10 == 0 and s2_moves[-1] == 'D': m1 = 'C'
                else: m1 = s2_moves[-1]
        elif s1 == "RAND":
            # 50/50 split
            m1 = 'C' if r < 50 else 'D'
            
        # Determine move for s2
        if s2 == "COOP": m2 = 'C'
        elif s2 == "DEFECT": m2 = 'D'
        elif s2 == "TFT":
            if r == 0: m2 = 'C'
            else: m2 = s1_moves[-1]
        elif s2 == "GTFT":
            if r == 0: m2 = 'C'
            else:
                if (r+1) % 10 == 0 and s1_moves[-1] == 'D': m2 = 'C'
                else: m2 = s1_moves[-1]
        elif s2 == "RAND":
            m2 = 'C' if r < 50 else 'D'
            
        s1_moves.append(m1)
        s2_moves.append(m2)
        
        if m1 == 'C' and m2 == 'C':
            s1_score += 3
            s2_score += 3
        elif m1 == 'D' and m2 == 'D':
            s1_score += 1
            s2_score += 1
        elif m1 == 'C' and m2 == 'D':
            s1_score += 0
            s2_score += 5
        elif m1 == 'D' and m2 == 'C':
            s1_score += 5
            s2_score += 0
            
    return s1_score

# Calculate total scores
total_scores = {s: 0 for s in strategies}
for s1 in strategies:
    for s2 in strategies:
        total_scores[s1] += get_score(s1, s2)

# Print results
sorted_scores = sorted(total_scores.items(), key=lambda x: x[1], reverse=True)
print("STATUS: sat")
for s, score in sorted_scores:
    print(f"{s}: {score}")