from z3 import *

# Candidates as integers for simplicity
candidates = {'A':0, 'B':1, 'C':2, 'D':3}
rev_cand = {v:k for k,v in candidates.items()}

# Voters list
voters = ['V1','V2','V3','V4','V5','V6']
# Original votes (as ints)
orig_votes = {
    'V1': candidates['A'],
    'V2': candidates['B'],
    'V3': candidates['B'],
    'V4': candidates['B'],
    'V5': candidates['A'],
    'V6': candidates['A'],
}
# Dissatisfied voters (prefer B over A)
# They are V5 and V6
dissatisfied = ['V5','V6']

opt = Optimize()
# Decision: for each dissatisfied voter, whether they join coalition (switch to B)
join = {v: Bool(f'join_{v}') for v in dissatisfied}
# Final vote for each voter (int sort)
final_vote = {v: Int(f'vote_{v}') for v in voters}

# Constraints for final votes
for v in voters:
    if v in dissatisfied:
        # If join then vote B else original
        opt.add(If(join[v], final_vote[v] == candidates['B'], final_vote[v] == orig_votes[v]))
    else:
        # Non-dissatisfied keep original vote
        opt.add(final_vote[v] == orig_votes[v])

# Compute vote counts for each candidate
vote_counts = {c: Int(f'count_{c}') for c in candidates.values()}
for c_val in candidates.values():
    opt.add(vote_counts[c_val] == Sum([If(final_vote[v] == c_val, 1, 0) for v in voters]))

# Determine winner by plurality (max count, tie broken alphabetically i.e., lower int wins)
# We need B to be winner after manipulation
# Enforce B count strictly greater than any other candidate's count
for c_val in candidates.values():
    if c_val != candidates['B']:
        opt.add(vote_counts[candidates['B']] > vote_counts[c_val])

# Coalition size
coalition_size = Sum([If(join[v], 1, 0) for v in dissatisfied])
opt.minimize(coalition_size)

# Solve
if opt.check() == sat:
    m = opt.model()
    # Extract coalition members
    members = [v for v in dissatisfied if m.eval(join[v])]
    size = m.eval(coalition_size).as_long()
    # Vote counts
    counts = {rev_cand[c]: m.eval(vote_counts[c]).as_long() for c in vote_counts}
    # Determine winner (should be B)
    winner = 'B'
    print('STATUS: sat')
    print('coalition_size =', size)
    print('coalition_members =', members)
    print('manipulated_vote_counts =', counts)
    print('winner =', winner)
else:
    print('STATUS: unsat')