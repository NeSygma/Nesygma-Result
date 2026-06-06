from z3 import *

# Given fragments
fragments = {
    'F0': 'ATGGGCGC',
    'F1': 'GGCGCCAT',
    'F2': 'GCCATT',
    'F3': 'ATTTAA',
    'F4': 'ATGCCTCG',
    'F5': 'GCTCGAGG',
    'F6': 'TCGAGCTG',
    'F7': 'AGCTGA',
    'F8': 'ATTCG'
}

# Reverse complement function
def reverse_complement(seq):
    comp = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(comp[base] for base in reversed(seq))

# Precompute reverse complements
rev_comp = {fid: reverse_complement(seq) for fid, seq in fragments.items()}

# GC content function
def gc_content(seq):
    gc = sum(1 for base in seq if base in 'GC')
    return gc / len(seq)

# Precompute GC content for each fragment in both orientations
gc_forward = {fid: gc_content(seq) for fid, seq in fragments.items()}
gc_reverse = {fid: gc_content(rev_comp[fid]) for fid in fragments}

# Create solver
solver = Solver()

# Variables
n_fragments = 9
n_max_contigs = 9  # Upper bound

# For each fragment: which contig it belongs to (0 = not used, 1..n_max_contigs)
contig_assignment = [Int(f'contig_{i}') for i in range(n_fragments)]

# For each fragment: orientation (0 = forward, 1 = reverse)
orientation = [Bool(f'orient_{i}') for i in range(n_fragments)]

# For each contig: whether it exists
contig_exists = [Bool(f'contig_exists_{c}') for c in range(1, n_max_contigs + 1)]

# For each fragment: whether it's used (not chimeric)
is_used = [Bool(f'used_{i}') for i in range(n_fragments)]

# Constraints

# 1. Fragment usage: each fragment is either used in exactly one contig or chimeric
for i in range(n_fragments):
    # If used, contig_assignment must be between 1 and n_max_contigs
    solver.add(If(is_used[i], 
                  And(contig_assignment[i] >= 1, contig_assignment[i] <= n_max_contigs),
                  contig_assignment[i] == 0))
    
    # If not used (chimeric), contig_assignment is 0
    solver.add(Implies(Not(is_used[i]), contig_assignment[i] == 0))

# 2. Each contig that exists must have at least one fragment
for c in range(1, n_max_contigs + 1):
    solver.add(contig_exists[c-1] == Or([contig_assignment[i] == c for i in range(n_fragments)]))

# 3. Fragment orientation affects sequence
# We'll handle this when checking overlaps

# 4. Overlap constraints between adjacent fragments in same contig
# For each pair of fragments in same contig, check if they can be adjacent
# This is complex - we need to check all possible orderings

# Let's create a simpler approach: define possible adjacencies
# For each pair of fragments (i, j), check if they can be adjacent in either orientation

# Helper: check if seq1 overlaps with seq2 by at least k bases
def check_overlap(seq1, seq2, min_overlap):
    for k in range(min_overlap, min(len(seq1), len(seq2)) + 1):
        if seq1[-k:] == seq2[:k]:
            return True
    return False

# Precompute possible adjacencies
# adjacency[i][j][ori_i][ori_j] = True if fragment i (orientation ori_i) can be followed by fragment j (orientation ori_j)
adjacency = {}
for i in range(n_fragments):
    for j in range(n_fragments):
        if i == j:
            continue
        for ori_i in [0, 1]:  # 0 = forward, 1 = reverse
            for ori_j in [0, 1]:
                seq_i = fragments[f'F{i}'] if ori_i == 0 else rev_comp[f'F{i}']
                seq_j = fragments[f'F{j}'] if ori_j == 0 else rev_comp[f'F{j}']
                
                # Determine min overlap based on GC content
                gc_i = gc_forward[f'F{i}'] if ori_i == 0 else gc_reverse[f'F{i}']
                gc_j = gc_forward[f'F{j}'] if ori_j == 0 else gc_reverse[f'F{j}']
                min_overlap = 4 if (gc_i > 0.5 and gc_j > 0.5) else 3
                
                adjacency[(i, j, ori_i, ori_j)] = check_overlap(seq_i, seq_j, min_overlap)

# Create adjacency variables
adj_var = {}
for i in range(n_fragments):
    for j in range(n_fragments):
        if i == j:
            continue
        for ori_i in [0, 1]:
            for ori_j in [0, 1]:
                adj_var[(i, j, ori_i, ori_j)] = Bool(f'adj_{i}_{j}_{ori_i}_{ori_j}')

# Constraint: adjacency variable is true only if fragments are in same contig and adjacent
for i in range(n_fragments):
    for j in range(n_fragments):
        if i == j:
            continue
        for ori_i in [0, 1]:
            for ori_j in [0, 1]:
                # If adjacency is possible and fragments are in same contig
                solver.add(Implies(
                    And(adj_var[(i, j, ori_i, ori_j)],
                        contig_assignment[i] == contig_assignment[j],
                        contig_assignment[i] != 0,
                        orientation[i] == (ori_i == 1),
                        orientation[j] == (ori_j == 1)),
                    adjacency[(i, j, ori_i, ori_j)]
                ))

# 5. Start codon constraint: each contig must start with ATG
# For each contig, find the first fragment and check if it starts with ATG (in its orientation)
for c in range(1, n_max_contigs + 1):
    # For each fragment in this contig, check if it could be the first
    for i in range(n_fragments):
        # If fragment i is in contig c and is the first fragment
        # We need to ensure that if it's first, its sequence starts with ATG
        first_frag = Bool(f'first_{c}_{i}')
        
        # Fragment i is first in contig c if:
        # 1. It's in contig c
        # 2. No other fragment in contig c comes before it
        # This is complex - we'll use a simpler approach
        
        # For now, just check that if a fragment is used and its contig exists,
        # then either it starts with ATG or some other fragment in the contig does
        pass

# Simplified start codon: For each contig, at least one fragment must start with ATG
# when placed at the beginning of the contig
for c in range(1, n_max_contigs + 1):
    start_options = []
    for i in range(n_fragments):
        # Check if fragment i can start a contig (starts with ATG in its orientation)
        seq_forward = fragments[f'F{i}']
        seq_reverse = rev_comp[f'F{i}']
        
        can_start_forward = seq_forward.startswith('ATG')
        can_start_reverse = seq_reverse.startswith('ATG')
        
        # Variable: fragment i is the first fragment in contig c
        is_first = Bool(f'first_{c}_{i}')
        
        # Constraint: if is_first, then orientation must allow ATG start
        solver.add(Implies(is_first, 
                          If(orientation[i], 
                             can_start_reverse, 
                             can_start_forward)))
        
        # Fragment i can be first only if it's in contig c
        solver.add(Implies(is_first, contig_assignment[i] == c))
        
        start_options.append(is_first)
    
    # At least one fragment must be first in each existing contig
    if start_options:
        solver.add(Implies(contig_exists[c-1], Or(start_options)))

# 6. Stop codon constraint: each contig must end with a stop codon
for c in range(1, n_max_contigs + 1):
    end_options = []
    for i in range(n_fragments):
        # Check if fragment i can end a contig (ends with stop codon in its orientation)
        seq_forward = fragments[f'F{i}']
        seq_reverse = rev_comp[f'F{i}']
        
        can_end_forward = any(seq_forward.endswith(codon) for codon in ['TAA', 'TAG', 'TGA'])
        can_end_reverse = any(seq_reverse.endswith(codon) for codon in ['TAA', 'TAG', 'TGA'])
        
        # Variable: fragment i is the last fragment in contig c
        is_last = Bool(f'last_{c}_{i}')
        
        # Constraint: if is_last, then orientation must allow stop codon end
        solver.add(Implies(is_last,
                          If(orientation[i],
                             can_end_reverse,
                             can_end_forward)))
        
        # Fragment i can be last only if it's in contig c
        solver.add(Implies(is_last, contig_assignment[i] == c))
        
        end_options.append(is_last)
    
    # At least one fragment must be last in each existing contig
    if end_options:
        solver.add(Implies(contig_exists[c-1], Or(end_options)))

# 7. Minimize number of contigs
# Count number of contigs that exist
num_contigs = Sum([If(contig_exists[c-1], 1, 0) for c in range(1, n_max_contigs + 1)])

# Use optimization to minimize contigs
opt = Solver()
for c in solver.assertions():
    opt.add(c)

# Add objective: minimize number of contigs
opt.minimize(num_contigs)

# Check
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract solution
    contigs = {}
    excluded = {'chimeric': []}
    
    # Group fragments by contig
    for i in range(n_fragments):
        contig_id = model.eval(contig_assignment[i])
        if contig_id == 0:
            excluded['chimeric'].append(f'F{i}')
        else:
            if contig_id not in contigs:
                contigs[contig_id] = {'fragments': [], 'orientations': []}
            contigs[contig_id]['fragments'].append(f'F{i}')
            orient = 'reverse' if model.eval(orientation[i]) else 'forward'
            contigs[contig_id]['orientations'].append(orient)
    
    # Print results
    print(f"Number of contigs: {len(contigs)}")
    print(f"Chimeric fragments: {excluded['chimeric']}")
    
    # For each contig, print details
    for contig_id in sorted(contigs.keys()):
        print(f"\nContig {contig_id}:")
        print(f"  Fragments: {contigs[contig_id]['fragments']}")
        print(f"  Orientations: {contigs[contig_id]['orientations']}")
        
        # Reconstruct sequence
        seq = ""
        for fid, orient in zip(contigs[contig_id]['fragments'], contigs[contig_id]['orientations']):
            fid_num = int(fid[1:])
            if orient == 'forward':
                seq += fragments[f'F{fid_num}']
            else:
                seq += rev_comp[f'F{fid_num}']
        print(f"  Sequence: {seq}")
    
    # Check if we have 2 contigs as expected
    if len(contigs) == 2:
        print("\n✓ Found expected minimum of 2 contigs")
    else:
        print(f"\n⚠ Found {len(contigs)} contigs, expected 2")
        
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")