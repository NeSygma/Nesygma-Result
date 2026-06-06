from z3 import *

# Problem setup
voters = ['V1', 'V2', 'V3', 'V4']
candidates = ['A', 'B', 'C']

# True preferences (ordinal rankings)
# Higher number = more preferred
true_prefs = {
    'V1': {'A': 3, 'B': 2, 'C': 1},
    'V2': {'A': 3, 'B': 1, 'C': 2},
    'V3': {'A': 1, 'B': 3, 'C': 2},
    'V4': {'A': 1, 'B': 2, 'C': 3}
}

# Current votes (truthful voting)
current_votes = {
    'V1': 'A',
    'V2': 'A', 
    'V3': 'B',
    'V4': 'C'
}

# Current vote counts
current_counts = {c: 0 for c in candidates}
for v in voters:
    current_counts[current_votes[v]] += 1

print("Current vote counts:", current_counts)
print("Current winner:", max(current_counts, key=current_counts.get))

# Define symbolic variables for strategic voting
# For each voter, which candidate they vote for (0=A, 1=B, 2=C)
vote_vars = {}
for v in voters:
    vote_vars[v] = Int(f'vote_{v}')

# Constraints: each voter votes for exactly one candidate
solver = Solver()
for v in voters:
    solver.add(Or([vote_vars[v] == i for i, c in enumerate(candidates)]))

# Function to get vote count for a candidate
def get_vote_count(candidate, votes_dict):
    idx = candidates.index(candidate)
    return Sum([If(votes_dict[v] == idx, 1, 0) for v in voters])

# Current outcome: A wins with 2 votes, B with 1, C with 1
current_winner = 'A'

# Check if any single voter can change the outcome to benefit themselves
print("\n=== Checking individual strategic opportunities ===")
for voter in voters:
    print(f"\nChecking {voter}:")
    print(f"  True preferences: {true_prefs[voter]}")
    
    # Try each possible vote change
    for new_vote in candidates:
        if new_vote != current_votes[voter]:
            # Create a solver for this specific scenario
            s = Solver()
            
            # Add base constraints
            for v in voters:
                s.add(Or([vote_vars[v] == i for i, c in enumerate(candidates)]))
            
            # Set current votes for others
            for other in voters:
                if other != voter:
                    s.add(vote_vars[other] == candidates.index(current_votes[other]))
            
            # Set the new vote for this voter
            s.add(vote_vars[voter] == candidates.index(new_vote))
            
            # Calculate new vote counts
            new_counts = {c: get_vote_count(c, vote_vars) for c in candidates}
            
            # Determine new winner (candidate with highest count)
            # We need to check if this change leads to a better outcome
            # For each possible new winner, check if it's better for the voter
            
            # Check if new vote changes the winner
            for possible_winner in candidates:
                # Constraint: possible_winner has highest count
                s2 = Solver()
                s2.add(s.assertions())
                
                # Add constraints that possible_winner has more votes than others
                for c in candidates:
                    if c != possible_winner:
                        s2.add(new_counts[possible_winner] >= new_counts[c])
                
                # Check if this scenario is possible
                if s2.check() == sat:
                    # Check if this winner is better for the voter
                    if true_prefs[voter][possible_winner] > true_prefs[voter][current_winner]:
                        print(f"  Can change vote to {new_vote} to make {possible_winner} win (better than {current_winner})")
                        print(f"    Benefit: {true_prefs[voter][possible_winner]} > {true_prefs[voter][current_winner]}")

# Check Condorcet winner
print("\n=== Checking Condorcet winner ===")
for c1 in candidates:
    wins_all = True
    for c2 in candidates:
        if c1 != c2:
            # Count pairwise comparisons
            s = Solver()
            # For each voter, determine preference between c1 and c2
            pref_counts = {c1: 0, c2: 0}
            for v in voters:
                if true_prefs[v][c1] > true_prefs[v][c2]:
                    pref_counts[c1] += 1
                else:
                    pref_counts[c2] += 1
            
            if pref_counts[c1] <= pref_counts[c2]:
                wins_all = False
                break
    
    if wins_all:
        print(f"{c1} is a Condorcet winner")
        break
else:
    print("No Condorcet winner")

# Check coalition manipulation
print("\n=== Checking coalition manipulation ===")
min_coalition_size = 5  # Start with impossible size

# Try all possible coalition sizes from 1 to 4
for coalition_size in range(1, 5):
    print(f"\nChecking coalition size {coalition_size}:")
    
    # Try all possible coalitions of this size
    from itertools import combinations
    for coalition in combinations(voters, coalition_size):
        coalition = list(coalition)
        
        # Try different manipulation strategies
        # Strategy: coalition votes for a candidate to make them win
        for target_candidate in candidates:
            # Check if coalition can make target_candidate win
            s = Solver()
            
            # Add base constraints
            for v in voters:
                s.add(Or([vote_vars[v] == i for i, c in enumerate(candidates)]))
            
            # Coalition votes for target
            for v in coalition:
                s.add(vote_vars[v] == candidates.index(target_candidate))
            
            # Others vote truthfully
            for v in voters:
                if v not in coalition:
                    s.add(vote_vars[v] == candidates.index(current_votes[v]))
            
            # Calculate vote counts
            counts = {c: get_vote_count(c, vote_vars) for c in candidates}
            
            # Check if target wins
            for c in candidates:
                if c != target_candidate:
                    s.add(counts[target_candidate] >= counts[c])
            
            if s.check() == sat:
                # Check if this is better for coalition members
                better_for_all = True
                for v in coalition:
                    if true_prefs[v][target_candidate] <= true_prefs[v][current_winner]:
                        better_for_all = False
                        break
                
                if better_for_all:
                    print(f"  Coalition {coalition} can make {target_candidate} win (better for all)")
                    min_coalition_size = min(min_coalition_size, coalition_size)

print(f"\nMinimum coalition size for successful manipulation: {min_coalition_size}")
if min_coalition_size <= 4:
    print("STATUS: sat")
else:
    print("STATUS: unsat")