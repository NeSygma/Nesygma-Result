from z3 import *

# Candidates: 0:A, 1:B, 2:C, 3:D
# Voters: 0:V1, 1:V2, 2:V3, 3:V4, 4:V5, 5:V6
# Preferences (rankings, lower is better):
# V1: A(0), B(1), C(2), D(3)
# V2: A(0), C(1), B(2), D(3)
# V3: A(0), D(1), B(2), C(3)
# V4: B(0), C(1), D(2), A(3)
# V5: B(0), A(1), D(2), C(3)
# V6: B(0), D(1), A(2), C(3)

prefs = [
    [0, 1, 2, 3], # V1
    [0, 2, 1, 3], # V2
    [0, 3, 1, 2], # V3
    [3, 0, 1, 2], # V4
    [1, 0, 2, 3], # V5
    [2, 1, 0, 3]  # V6
]

# Initial votes:
# V1: A(0), V2: B(1), V3: B(1), V4: B(1), V5: A(0), V6: A(0)
initial_votes = [0, 1, 1, 1, 0, 0]

# Original counts: A=3, B=3, C=0, D=0
# Tie-break: A < B < C < D (A wins)

def get_winner_and_counts(votes):
    # votes is a list of Z3 Ints
    counts = [Sum([If(votes[i] == c, 1, 0) for i in range(6)]) for c in range(4)]
    
    # Tie-break: A(0) < B(1) < C(2) < D(3)
    # Winner is the one with max votes, tie-break by index
    # This is a bit complex in Z3.
    # Let's use a simple comparison.
    winner = Int('winner')
    
    # Winner is c such that counts[c] is max, and for all c' < c, counts[c'] < counts[c]
    # Actually, simpler:
    # winner = c iff counts[c] >= counts[c'] for all c' != c
    # AND if counts[c] == counts[c'], then c < c'
    
    # Let's define a condition for each candidate to be the winner
    is_winner = [Bool(f'is_winner_{c}') for c in range(4)]
    for c in range(4):
        # c is winner if for all other c', counts[c] > counts[c'] OR (counts[c] == counts[c'] and c < c')
        conds = [Or(counts[c] > counts[c_other], And(counts[c] == counts[c_other], c < c_other)) for c_other in range(4) if c_other != c]
        opt.add(is_winner[c] == And(*conds))
    
    opt.add(Or(*is_winner))
    
    # Return the winner index and the counts
    winner_idx = Int('winner_idx')
    opt.add(Or([And(is_winner[c], winner_idx == c) for c in range(4)]))
    
    return winner_idx, counts

opt = Optimize()
coalition = [Bool(f'c_{i}') for i in range(6)]
new_votes = [If(coalition[i], 1, initial_votes[i]) for i in range(6)]

new_winner, new_counts = get_winner_and_counts(new_votes)

# Original winner: A(0)
orig_winner = 0
condorcet_winner = 1

# Manipulation success
opt.add(new_winner == condorcet_winner)
opt.add(new_winner != orig_winner)

# Individual Rationality:
# No coalition member worse off.
# Worse off means the new winner is ranked lower than the original winner in their preference.
for i in range(6):
    # Rank of candidate c for voter i:
    def get_rank_expr(voter_idx, cand_idx):
        # prefs[voter_idx] is a list of candidates in order of preference
        # We need to return the rank (0-3)
        rank = Int(f'rank_{voter_idx}_{cand_idx}')
        for r in range(4):
            opt.add(Implies(cand_idx == prefs[voter_idx][r], rank == r))
        return rank
    
    orig_rank = get_rank_expr(i, orig_winner)
    new_rank = get_rank_expr(i, new_winner)
    
    # If in coalition, they must not be worse off
    # "Worse off" means new_rank > orig_rank
    opt.add(Implies(coalition[i], new_rank <= orig_rank))

# Only dissatisfied voters can be in the coalition?
# The problem says "The coalition consists of dissatisfied voters".
# Dissatisfied: V5, V6.
for i in range(6):
    if i not in [4, 5]:
        opt.add(Not(coalition[i]))

# Minimize coalition size
opt.minimize(Sum([If(coalition[i], 1, 0) for i in range(6)]))

res = opt.check()
if res == sat:
    m = opt.model()
    print("STATUS: sat")
    coalition_members = [i for i in range(6) if is_true(m[coalition[i]])]
    print(f"Coalition: {coalition_members}")
    print(f"New winner: {m.evaluate(new_winner)}")
    print(f"New counts: {[m.evaluate(new_counts[c]) for c in range(4)]}")
else:
    print("STATUS: unsat")