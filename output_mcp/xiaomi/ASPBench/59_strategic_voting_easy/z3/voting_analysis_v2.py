from z3 import *

# ============================================================
# PART 1: Current Voting Outcome Analysis
# ============================================================
print("=" * 60)
print("PART 1: Current Voting Outcome")
print("=" * 60)

# Candidates: A=0, B=1, C=2
candidates = ['A', 'B', 'C']
voters = ['V1', 'V2', 'V3', 'V4']

# Current votes mapping
current_votes_map = {'V1': 'A', 'V2': 'A', 'V3': 'B', 'V4': 'C'}

# Current vote counts
count_A = 2  # V1, V2
count_B = 1  # V3
count_C = 1  # V4

print(f"Current vote counts: A={count_A}, B={count_B}, C={count_C}")
print(f"Current winner: A (with {count_A} votes)")

# ============================================================
# PART 2: Condorcet Winner Analysis
# ============================================================
print("\n" + "=" * 60)
print("PART 2: Condorcet Winner Analysis")
print("=" * 60)

# Preferences (higher = more preferred, rank 3=best, 1=worst)
# V1: A > B > C  => A=3, B=2, C=1
# V2: A > C > B  => A=3, C=2, B=1
# V3: B > C > A  => B=3, C=2, A=1
# V4: C > B > A  => C=3, B=2, A=1

preferences = {
    'V1': {'A': 3, 'B': 2, 'C': 1},
    'V2': {'A': 3, 'C': 2, 'B': 1},
    'V3': {'B': 3, 'C': 2, 'A': 1},
    'V4': {'C': 3, 'B': 2, 'A': 1}
}

# Pairwise comparisons
pairs = [('A', 'B'), ('A', 'C'), ('B', 'C')]

condorcet_winner = None
for c1, c2 in pairs:
    c1_wins = sum(1 for v in voters if preferences[v][c1] > preferences[v][c2])
    c2_wins = sum(1 for v in voters if preferences[v][c2] > preferences[v][c1])
    print(f"{c1} vs {c2}: {c1_wins} - {c2_wins} => Winner: {c1 if c1_wins > c2_wins else c2}")

# Check if any candidate wins all pairwise
for c in candidates:
    wins_all = True
    for other in candidates:
        if c != other:
            c_wins = sum(1 for v in voters if preferences[v][c] > preferences[v][other])
            if c_wins <= 2:  # Need > 2 out of 4 to win
                wins_all = False
                break
    if wins_all:
        condorcet_winner = c

if condorcet_winner:
    print(f"\nCondorcet Winner: {condorcet_winner}")
else:
    print("\nNo Condorcet Winner exists (Condorcet paradox)")

# ============================================================
# PART 3: Strategic Voting Detection (Single Voter)
# ============================================================
print("\n" + "=" * 60)
print("PART 3: Single-Voter Strategic Voting Detection")
print("=" * 60)

# For each voter, check if they can improve outcome by voting differently
# Current winner is A

def get_winner(counts):
    """Return winner given vote counts dict"""
    max_votes = max(counts.values())
    winners = [c for c, v in counts.items() if v == max_votes]
    return winners

current_counts = {'A': 2, 'B': 1, 'C': 1}
current_winner = get_winner(current_counts)
print(f"Current winner: {current_winner}")

# Voter utility: rank 3=best, 2=middle, 1=worst
def voter_utility(voter, winner):
    return preferences[voter][winner]

print("\nChecking each voter's strategic options:")
strategic_single = []

for voter in voters:
    current_utility = voter_utility(voter, current_winner[0])
    print(f"\n{voter} (prefers: ", end="")
    pref_sorted = sorted(preferences[voter].items(), key=lambda x: -x[1])
    print(" > ".join([f"{c}({p})" for c, p in pref_sorted]), end="")
    print(f") - Current utility: {current_utility}")
    
    # Try each possible vote for this voter
    for new_vote in candidates:
        if new_vote == current_votes_map[voter]:
            continue  # Same as current vote
        
        # Simulate new vote counts
        new_counts = dict(current_counts)
        new_counts[current_votes_map[voter]] -= 1
        new_counts[new_vote] += 1
        
        new_winner = get_winner(new_counts)
        new_utility = voter_utility(voter, new_winner[0])
        
        if new_utility > current_utility:
            print(f"  -> Can vote {new_vote} instead, winner becomes {new_winner}, utility {new_utility} > {current_utility}")
            strategic_single.append((voter, new_vote, new_winner[0]))

if strategic_single:
    print(f"\n✓ Strategic voting possible by single voter(s):")
    for voter, vote, winner in strategic_single:
        print(f"  {voter} votes {vote} -> winner {winner}")
else:
    print("\n✗ No single voter can improve outcome alone")

# ============================================================
# PART 4: Coalition Manipulation Detection (Z3)
# ============================================================
print("\n" + "=" * 60)
print("PART 4: Coalition Manipulation Detection (Z3)")
print("=" * 60)

# We'll use Z3 to find minimum coalition size for manipulation
# Current winner is A with votes {A:2, B:1, C:1}

# For each possible coalition size k (1 to 4), check if any coalition of size k
# can change votes to make a better winner for all coalition members

best_coalition_size = None
best_manipulation = None

for coalition_size in range(1, 5):
    print(f"\n--- Testing coalition size {coalition_size} ---")
    
    solver = Solver()
    
    # Binary variables: is voter i in the coalition?
    in_coalition = [Bool(f'in_coalition_{i}') for i in range(4)]
    
    # Exactly coalition_size voters in coalition
    solver.add(Sum([If(in_coalition[i], 1, 0) for i in range(4)]) == coalition_size)
    
    # New vote for each voter (0=A, 1=B, 2=C)
    new_vote = [Int(f'new_vote_{i}') for i in range(4)]
    for i in range(4):
        solver.add(new_vote[i] >= 0, new_vote[i] <= 2)
    
    # Coalition members can change votes; non-coalition members keep original votes
    original_votes = [0, 0, 1, 2]  # V1->A, V2->A, V3->B, V4->C
    
    # Compute new vote counts
    new_count_A = Sum([If(new_vote[i] == 0, 1, 0) for i in range(4)])
    new_count_B = Sum([If(new_vote[i] == 1, 1, 0) for i in range(4)])
    new_count_C = Sum([If(new_vote[i] == 2, 1, 0) for i in range(4)])
    
    # Winner determination: candidate with most votes
    # We need to find if there exists a new winner that's better for all coalition members
    
    # For each possible new winner, check if it's achievable and better
    # Let's try each candidate as potential new winner
    found_for_size = False
    
    for new_winner_idx, new_winner_name in enumerate(candidates):
        solver.push()
        
        # New winner must have strictly more votes than others
        if new_winner_idx == 0:  # A wins
            solver.add(new_count_A > new_count_B)
            solver.add(new_count_A > new_count_C)
        elif new_winner_idx == 1:  # B wins
            solver.add(new_count_B > new_count_A)
            solver.add(new_count_B > new_count_C)
        else:  # C wins
            solver.add(new_count_C > new_count_A)
            solver.add(new_count_C > new_count_B)
        
        # Coalition members must all prefer new winner to current winner (A)
        # Current winner is A (index 0)
        for i in range(4):
            voter_name = voters[i]
            # Utility of new winner must be > utility of A for coalition members
            new_utility = preferences[voter_name][new_winner_name]
            current_utility = preferences[voter_name]['A']
            
            # If in coalition, must prefer new winner
            solver.add(Implies(in_coalition[i], new_utility > current_utility))
        
        # Non-coalition members keep their original votes
        for i in range(4):
            solver.add(Implies(Not(in_coalition[i]), new_vote[i] == original_votes[i]))
        
        result = solver.check()
        if result == sat:
            m = solver.model()
            coalition_members = [voters[i] for i in range(4) if is_true(m.evaluate(in_coalition[i]))]
            new_votes = [candidates[m.evaluate(new_vote[i]).as_long()] for i in range(4)]
            
            print(f"  ✓ MANIPULATION FOUND! New winner: {new_winner_name}")
            print(f"    Coalition: {coalition_members}")
            print(f"    New votes: {dict(zip(voters, new_votes))}")
            
            # Verify vote counts
            new_counts = {'A': 0, 'B': 0, 'C': 0}
            for v in new_votes:
                new_counts[v] += 1
            print(f"    New counts: {new_counts}")
            
            found_for_size = True
            if best_coalition_size is None or coalition_size < best_coalition_size:
                best_coalition_size = coalition_size
                best_manipulation = {
                    'coalition': coalition_members,
                    'new_winner': new_winner_name,
                    'new_votes': dict(zip(voters, new_votes)),
                    'new_counts': new_counts
                }
            solver.pop()
            break  # Found one manipulation for this size
        
        solver.pop()
    
    if not found_for_size:
        print(f"  ✗ No manipulation possible with coalition size {coalition_size}")

# ============================================================
# PART 5: Summary
# ============================================================
print("\n" + "=" * 60)
print("PART 5: Summary")
print("=" * 60)

print(f"Current outcome: A wins with {count_A} votes")
print(f"Condorcet Winner: {condorcet_winner if condorcet_winner else 'None (paradox)'}")

if strategic_single:
    print(f"Single-voter strategic voting: POSSIBLE")
    for voter, vote, winner in strategic_single:
        print(f"  {voter} can vote {vote} to make {winner} win")
else:
    print(f"Single-voter strategic voting: NOT POSSIBLE")

if best_coalition_size:
    print(f"\nMinimum coalition size for manipulation: {best_coalition_size}")
    print(f"Manipulation details:")
    print(f"  Coalition: {best_manipulation['coalition']}")
    print(f"  New winner: {best_manipulation['new_winner']}")
    print(f"  New votes: {best_manipulation['new_votes']}")
    print(f"  New counts: {best_manipulation['new_counts']}")
    
    # Verify all coalition members prefer new winner
    print(f"\n  Coalition member preferences:")
    for voter in best_manipulation['coalition']:
        pref = preferences[voter]
        print(f"    {voter}: {best_manipulation['new_winner']}({pref[best_manipulation['new_winner']]}) > A({pref['A']}) ✓")
else:
    print(f"\nNo manipulation possible with any coalition size")

print("\n" + "=" * 60)
print("STATUS: sat")
print("=" * 60)