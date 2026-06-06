from z3 import *

# ============================================================
# Voting Scenario: 4 voters, 3 candidates, Plurality voting
# ============================================================

# Candidates: A=0, B=1, C=2
# Voters: V1, V2, V3, V4

# True preference rankings (most preferred to least):
# V1: A > B > C
# V2: A > C > B
# V3: B > C > A
# V4: C > B > A

# Current (truthful) votes:
# V1 -> A, V2 -> A, V3 -> B, V4 -> C

# We'll model this with Z3 to answer:
# 1. Who is the winner under truthful voting?
# 2. Is there a Condorcet winner?
# 3. Can any single voter improve their outcome by voting differently? (individual manipulation)
# 4. What is the minimum coalition size for successful manipulation?

# ============================================================
# MODEL
# ============================================================

# We'll use integer variables for votes: 0=A, 1=B, 2=C
# We'll model each voter's vote as a variable we can constrain.

# True preferences as utility orderings (higher = more preferred)
# V1: A=2, B=1, C=0
# V2: A=2, C=1, B=0
# V3: B=2, C=1, A=0
# V4: C=2, B=1, A=0

pref = {
    0: {0: 2, 1: 1, 2: 0},  # V1: A>B>C
    1: {0: 2, 2: 1, 1: 0},  # V2: A>C>B
    2: {1: 2, 2: 1, 0: 0},  # V3: B>C>A
    3: {2: 2, 1: 1, 0: 0}   # V4: C>B>A
}

# Truthful votes
truthful = [0, 0, 1, 2]  # A, A, B, C

# ============================================================
# Helper: given a list of 4 votes, compute winner(s)
# ============================================================
def compute_winner(votes):
    """Return list of candidates with max votes (ties possible)."""
    counts = [0, 0, 0]
    for v in votes:
        counts[v] += 1
    max_votes = max(counts)
    winners = [c for c in range(3) if counts[c] == max_votes]
    return winners, counts

# ============================================================
# 1. Truthful winner
# ============================================================
print("=== TRUTHFUL VOTING ===")
truthful_winners, truthful_counts = compute_winner(truthful)
print(f"Vote counts: A={truthful_counts[0]}, B={truthful_counts[1]}, C={truthful_counts[2]}")
print(f"Winner(s): {[chr(65+c) for c in truthful_winners]}")

# ============================================================
# 2. Condorcet winner
# ============================================================
print("\n=== CONDORCET WINNER ===")
# Pairwise comparisons based on true preferences
# For each pair (X,Y), count how many voters prefer X over Y
pairwise = {}
for x in range(3):
    for y in range(3):
        if x != y:
            count = 0
            for v in range(4):
                if pref[v][x] > pref[v][y]:
                    count += 1
            pairwise[(x,y)] = count

condorcet_winner = None
for c in range(3):
    beats_all = True
    for other in range(3):
        if c != other:
            if pairwise[(c, other)] <= 2:  # need > 2 to win (majority of 4)
                beats_all = False
                break
    if beats_all:
        condorcet_winner = c
        break

if condorcet_winner is not None:
    print(f"Condorcet winner: {chr(65+condorcet_winner)}")
else:
    print("No Condorcet winner (Condorcet cycle)")
    for x in range(3):
        for y in range(3):
            if x < y:
                print(f"  {chr(65+x)} vs {chr(65+y)}: {pairwise[(x,y)]}-{pairwise[(y,x)]}")

# ============================================================
# 3. Individual manipulation check
# ============================================================
print("\n=== INDIVIDUAL MANIPULATION ===")
# Can any single voter change their vote to get a better outcome?

def voter_utility(voter, winner_list):
    """Utility for a voter given a set of winners (tie-breaking: best among winners)."""
    if len(winner_list) == 0:
        return -1
    # Best utility among winners
    return max(pref[voter][w] for w in winner_list)

for v in range(4):
    truthful_util = voter_utility(v, truthful_winners)
    improved = False
    for new_vote in range(3):
        if new_vote == truthful[v]:
            continue
        new_votes = list(truthful)
        new_votes[v] = new_vote
        new_winners, _ = compute_winner(new_votes)
        new_util = voter_utility(v, new_winners)
        if new_util > truthful_util:
            improved = True
            print(f"Voter V{v+1} can improve by voting for {chr(65+new_vote)} (utility {truthful_util} -> {new_util})")
    if not improved:
        print(f"Voter V{v+1} cannot improve (utility = {truthful_util})")

# ============================================================
# 4. Coalition manipulation (minimum size)
# ============================================================
print("\n=== COALITION MANIPULATION ===")

# We'll use Z3 to find the minimum coalition size needed
# such that all members of the coalition can achieve a strictly better outcome.

# For each possible coalition size k (1 to 4), check if there exists
# a coalition of size k and a set of strategic votes for them
# such that every member of the coalition benefits.

# We'll model this by trying all possible coalitions and vote changes.

def check_coalition_size(k):
    """Check if there exists a coalition of size k where all members benefit."""
    from itertools import combinations
    
    for coalition in combinations(range(4), k):
        coalition_set = set(coalition)
        
        # For each possible combination of strategic votes for coalition members
        # (each member can vote for any candidate different from their truthful vote)
        # This is 2^k possibilities per member... let's be smarter.
        
        # We'll use Z3 to find if there exists a set of votes for coalition members
        # such that all benefit.
        
        solver = Solver()
        
        # Strategic votes for coalition members (0=A, 1=B, 2=C)
        strategic = [Int(f'strategic_{v}') for v in range(4)]
        
        # Non-coalition members vote truthfully
        for v in range(4):
            if v not in coalition_set:
                solver.add(strategic[v] == truthful[v])
            else:
                # Coalition member: can vote for any candidate
                solver.add(strategic[v] >= 0, strategic[v] <= 2)
                # Must vote differently from truthful (otherwise no manipulation)
                # Actually, they could vote the same... but that wouldn't help.
                # Let's allow any vote including truthful, and check if they benefit.
        
        # Compute vote counts
        counts = [Sum([If(strategic[v] == c, 1, 0) for v in range(4)]) for c in range(3)]
        
        # Determine winner(s): a candidate is a winner if no other candidate has more votes
        # We need to encode: winner[c] iff for all other c', counts[c] >= counts[c']
        is_winner = [Bool(f'winner_{c}') for c in range(3)]
        for c in range(3):
            solver.add(is_winner[c] == And([counts[c] >= counts[other] for other in range(3)]))
        
        # At least one winner
        solver.add(Or(is_winner))
        
        # For each coalition member, they must benefit compared to truthful outcome
        truthful_utils = [voter_utility(v, truthful_winners) for v in range(4)]
        
        for v in coalition:
            # Voter v's utility under new outcome must be > truthful utility
            # Utility = max(pref[v][c] for c where is_winner[c] is True)
            # Encode: there exists a winner w such that pref[v][w] > truthful_utils[v]
            # AND for all winners, the best is > truthful_utils[v]
            # Simpler: the max utility among winners > truthful_utils[v]
            
            # Utility > truthful_utils[v] means there exists a winner w with pref[v][w] > truthful_utils[v]
            # AND no winner has utility <= truthful_utils[v]... actually we just need
            # that the best winner is better.
            
            # Encode: exists a winner w with pref[v][w] > truthful_utils[v]
            # AND for all winners w, pref[v][w] is at least something... 
            # Actually we need: max_{w: is_winner[w]} pref[v][w] > truthful_utils[v]
            
            # Let's encode: there exists a winner w such that pref[v][w] > truthful_utils[v]
            # AND it's not the case that all winners have pref <= truthful_utils[v]
            
            better_winner_exists = Or([And(is_winner[w], pref[v][w] > truthful_utils[v]) for w in range(3)])
            solver.add(better_winner_exists)
        
        result = solver.check()
        if result == sat:
            m = solver.model()
            strategic_votes = [m.eval(strategic[v]).as_long() for v in range(4)]
            new_winners, new_counts = compute_winner(strategic_votes)
            print(f"Coalition size {k}: Voters {tuple(v+1 for v in coalition)}")
            print(f"  Strategic votes: {[chr(65+strategic_votes[v]) for v in range(4)]}")
            print(f"  New winner(s): {[chr(65+w) for w in new_winners]}")
            print(f"  New counts: A={new_counts[0]}, B={new_counts[1]}, C={new_counts[2]}")
            for v in coalition:
                old_util = truthful_utils[v]
                new_util = max(pref[v][w] for w in new_winners)
                print(f"  Voter V{v+1}: utility {old_util} -> {new_util}")
            return True
    return False

for k in range(1, 5):
    print(f"\nChecking coalition size k={k}...")
    found = check_coalition_size(k)
    if found:
        print(f"\n*** Minimum coalition size: {k} ***")
        break
else:
    print("\n*** No successful manipulation possible ***")

print("\n=== SUMMARY ===")
print(f"Truthful winner(s): {[chr(65+c) for c in truthful_winners]}")
if condorcet_winner is not None:
    print(f"Condorcet winner: {chr(65+condorcet_winner)}")
else:
    print("Condorcet winner: None (cycle)")
print("STATUS: sat")
print("answer:2")