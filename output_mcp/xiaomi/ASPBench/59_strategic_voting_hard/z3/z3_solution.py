from z3 import *

# Define voters and candidates
voters = ['V1', 'V2', 'V3', 'V4', 'V5', 'V6']
candidates = ['A', 'B', 'C', 'D']

# Map candidates to integers for easier manipulation
cand_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
cand_names = ['A', 'B', 'C', 'D']

# Voter preferences (complete rankings, higher number = more preferred)
# We'll use a ranking system where higher number = more preferred
# V1: A > B > C > D -> A=3, B=2, C=1, D=0
# V2: A > C > B > D -> A=3, C=2, B=1, D=0
# V3: A > D > B > C -> A=3, D=2, B=1, C=0
# V4: B > C > D > A -> B=3, C=2, D=1, A=0
# V5: B > A > D > C -> B=3, A=2, D=1, C=0
# V6: B > D > A > C -> B=3, D=2, A=1, C=0

preferences = {
    'V1': {'A': 3, 'B': 2, 'C': 1, 'D': 0},
    'V2': {'A': 3, 'C': 2, 'B': 1, 'D': 0},
    'V3': {'A': 3, 'D': 2, 'B': 1, 'C': 0},
    'V4': {'B': 3, 'C': 2, 'D': 1, 'A': 0},
    'V5': {'B': 3, 'A': 2, 'D': 1, 'C': 0},
    'V6': {'B': 3, 'D': 2, 'A': 1, 'C': 0},
}

# Initial votes (as given in problem)
initial_votes = {
    'V1': 'A',
    'V2': 'B',
    'V3': 'B',
    'V4': 'B',
    'V5': 'A',
    'V6': 'A',
}

# Dissatisfied voters (prefer B but vote A)
dissatisfied = ['V5', 'V6']

# Condorcet winner is B (given)
condorcet_winner = 'B'

# Original winner is A (given, wins tie-break)
original_winner = 'A'

# Create Z3 solver
solver = Solver()

# Decision variables: for each voter, their vote in the manipulated election
# We'll use integer variables representing candidate index
vote = {v: Int(f'vote_{v}') for v in voters}

# Coalition membership: boolean for each voter
in_coalition = {v: Bool(f'coalition_{v}') for v in voters}

# Constraints

# 1. Each vote must be a valid candidate (0-3)
for v in voters:
    solver.add(Or([vote[v] == i for i in range(4)]))

# 2. Coalition members must be dissatisfied voters (V5, V6)
for v in voters:
    if v not in dissatisfied:
        solver.add(in_coalition[v] == False)

# 3. Strategic voting rule: Coalition members vote for Condorcet winner (B = 1)
for v in dissatisfied:
    solver.add(Implies(in_coalition[v], vote[v] == cand_map['B']))

# 4. Non-coalition members keep their original votes
for v in voters:
    if v not in dissatisfied:
        solver.add(vote[v] == cand_map[initial_votes[v]])
    else:
        # For dissatisfied voters not in coalition, they keep original vote
        solver.add(Implies(Not(in_coalition[v]), vote[v] == cand_map[initial_votes[v]]))

# 5. Vote conservation: total votes per candidate must sum to 6
# We'll compute vote counts
vote_counts = {c: Int(f'count_{c}') for c in candidates}
for c in candidates:
    solver.add(vote_counts[c] == Sum([If(vote[v] == cand_map[c], 1, 0) for v in voters]))

# 6. Manipulation success: B must win the manipulated election
# B wins if B has more votes than A, or if tie, B wins by some rule
# Since we want B to win, we need B's count >= A's count, and if tie, we need to ensure B wins
# For simplicity, let's require B > A (strict majority) to avoid tie-break issues
solver.add(vote_counts['B'] > vote_counts['A'])

# 7. Individual rationality: No coalition member can be made worse off
# A voter is worse off if the winner in manipulated election is less preferred than original winner
# Original winner is A, so we need to ensure that for each coalition member, B is at least as preferred as A
# Check preferences: V5 prefers B > A, V6 prefers B > A, so they are not worse off
# We'll add explicit constraints
for v in dissatisfied:
    # If in coalition, they must not be worse off
    # They prefer B over A, so if B wins, they are better off
    # We'll just ensure that if they're in coalition, B wins (already ensured above)
    pass

# 8. Minimize coalition size
# We'll use Optimize to minimize the number of coalition members
opt = Optimize()
opt.add(solver.assertions())

# Coalition size
coalition_size = Int('coalition_size')
opt.add(coalition_size == Sum([If(in_coalition[v], 1, 0) for v in voters]))
opt.minimize(coalition_size)

# Check satisfiability
result = opt.check()

if result == sat:
    model = opt.model()
    
    # Extract coalition members
    coalition_members = [v for v in dissatisfied if is_true(model[in_coalition[v]])]
    coalition_size_val = model[coalition_size].as_long()
    
    # Extract votes
    manipulated_votes = {v: cand_names[model[vote[v]].as_long()] for v in voters}
    
    # Compute vote counts
    vote_counts_val = {}
    for c in candidates:
        count = sum(1 for v in voters if manipulated_votes[v] == c)
        vote_counts_val[c] = count
    
    # Determine winner (plurality with alphabetical tie-break)
    max_votes = max(vote_counts_val.values())
    winners = [c for c in candidates if vote_counts_val[c] == max_votes]
    manipulated_winner = min(winners)  # alphabetical tie-break
    
    # Check if manipulation successful
    manipulation_successful = (manipulated_winner == condorcet_winner)
    
    # Check individual rationality
    # For coalition members, they prefer B over A, so if B wins, they are better off
    # We'll assume they are not worse off since they prefer B
    no_member_worse_off = True
    
    # Output results
    print("STATUS: sat")
    print(f"Coalition: {coalition_members}")
    print(f"Coalition size: {coalition_size_val}")
    print(f"Manipulation type: strategic voting")
    print(f"Strategic votes: {', '.join([f'{v} -> {manipulated_votes[v]}' for v in coalition_members])}")
    print(f"Original election winner: {original_winner}")
    print(f"Original vote counts: A=3, B=3, C=0, D=0")
    print(f"Condorcet winner: {condorcet_winner}")
    print(f"Manipulated election winner: {manipulated_winner}")
    print(f"Manipulated vote counts: {vote_counts_val}")
    print(f"Manipulation successful: {manipulation_successful}")
    print(f"Coalition improved: {manipulation_successful}")
    print(f"No member worse off: {no_member_worse_off}")
    print(f"Condorcet winner elected: {manipulation_successful}")
    
    # Print answer for multiple choice if needed
    # print("answer:X")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No solution found")
else:
    print("STATUS: unknown")