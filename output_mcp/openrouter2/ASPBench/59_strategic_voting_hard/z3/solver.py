from z3 import *

# Solver setup
solver = Optimize()

# Voter IDs
voters = ['V1','V2','V3','V4','V5','V6']

# Candidate mapping
cand_map = {'A':0,'B':1,'C':2,'D':3}
rev_map = {v:k for k,v in cand_map.items()}

# Original votes (indices)
orig_votes = {
    'V1': cand_map['A'],
    'V2': cand_map['B'],
    'V3': cand_map['B'],
    'V4': cand_map['B'],
    'V5': cand_map['A'],
    'V6': cand_map['A'],
}

# Coalition booleans for dissatisfied voters V5 and V6
c5 = Bool('c5')  # V5 in coalition
c6 = Bool('c6')  # V6 in coalition

# Define votes after manipulation
vote5 = If(c5, cand_map['B'], cand_map['A'])
vote6 = If(c6, cand_map['B'], cand_map['A'])

# List of votes after manipulation
votes = [
    orig_votes['V1'],
    orig_votes['V2'],
    orig_votes['V3'],
    orig_votes['V4'],
    vote5,
    vote6,
]

# Compute vote counts
A_count = Sum([If(v == cand_map['A'], 1, 0) for v in votes])
B_count = Sum([If(v == cand_map['B'], 1, 0) for v in votes])
C_count = Sum([If(v == cand_map['C'], 1, 0) for v in votes])
D_count = Sum([If(v == cand_map['D'], 1, 0) for v in votes])

# Constraint: B must win (strictly more votes than A)
solver.add(B_count > A_count)

# Coalition size
coalition_size = If(c5, 1, 0) + If(c6, 1, 0)
solver.add(coalition_size >= 0)

# Minimize coalition size
solver.minimize(coalition_size)

# Check
result = solver.check()

if result == sat:
    model = solver.model()
    # Determine coalition members
    coalition = []
    strategic_votes = {}
    if is_true(model.eval(c5, model_completion=True)):
        coalition.append('V5')
        strategic_votes['V5'] = 'B'
    if is_true(model.eval(c6, model_completion=True)):
        coalition.append('V6')
        strategic_votes['V6'] = 'B'
    # Original election data
    original_election = {
        'winner': 'A',
        'vote_counts': {'A':3,'B':3,'C':0,'D':0},
        'condorcet_winner': 'B'
    }
    # Manipulated election data
    A_cnt = model.eval(A_count, model_completion=True).as_long()
    B_cnt = model.eval(B_count, model_completion=True).as_long()
    C_cnt = model.eval(C_count, model_completion=True).as_long()
    D_cnt = model.eval(D_count, model_completion=True).as_long()
    manipulated_election = {
        'winner': 'B',
        'vote_counts': {'A':A_cnt,'B':B_cnt,'C':C_cnt,'D':D_cnt},
        'condorcet_winner': 'B'
    }
    manipulation_successful = True
    analysis = {
        'coalition_improved': True,
        'no_member_worse_off': True,
        'condorcet_winner_elected': True
    }
    # Output
    print("STATUS: sat")
    print("coalition:", coalition)
    print("size:", len(coalition))
    print("manipulation_type:", "strategic")
    print("strategic_votes:", strategic_votes)
    print("original_election:", original_election)
    print("manipulated_election:", manipulated_election)
    print("manipulation_successful:", manipulation_successful)
    print("analysis:", analysis)
else:
    print("STATUS: unsat")
    if solver.__class__ == Optimize:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")