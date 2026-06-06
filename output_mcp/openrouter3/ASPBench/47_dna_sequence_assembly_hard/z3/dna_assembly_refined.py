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

# Create optimizer
opt = Optimize()

# Variables
n_fragments = 9
n_max_contigs = 9

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
    opt.add(If(is_used[i], 
               And(contig_assignment[i] >= 1, contig_assignment[i] <= n_max_contigs),
               contig_assignment[i] == 0))
    
    # If not used (chimeric), contig_assignment is 0
    opt.add(Implies(Not(is_used[i]), contig_assignment[i] == 0))

# 2. Each contig that exists must have at least one fragment
for c in range(1, n_max_contigs + 1):
    opt.add(contig_exists[c-1] == Or([contig_assignment[i] == c for i in range(n_fragments)]))

# 3. Start codon constraint: each contig must start with ATG
# For each contig, find the first fragment and check if it starts with ATG
for c in range(1, n_max_contigs + 1):
    for i in range(n_fragments):
        # Check if fragment i can start a contig (starts with ATG in its orientation)
        seq_forward = fragments[f'F{i}']
        seq_reverse = rev_comp[f'F{i}']
        
        can_start_forward = seq_forward.startswith('ATG')
        can_start_reverse = seq_reverse.startswith('ATG')
        
        # If fragment i is in contig c and is the first fragment, it must start with ATG
        # We'll handle "first fragment" logic later
        
        # For now, just ensure that if a fragment is in a contig, it can potentially be placed
        # We'll add a constraint that at least one fragment in each contig can start with ATG
        # This is handled by the "first fragment" logic below

# 4. Stop codon constraint: each contig must end with a stop codon
# Similar to start codon, handled by "last fragment" logic

# 5. Overlap constraints between adjacent fragments in same contig
# This is complex - let's simplify by requiring that adjacent fragments in same contig
# must have at least the required overlap

# Helper: check if seq1 overlaps with seq2 by at least k bases
def check_overlap(seq1, seq2, min_overlap):
    for k in range(min_overlap, min(len(seq1), len(seq2)) + 1):
        if seq1[-k:] == seq2[:k]:
            return True
    return False

# For each pair of fragments in same contig, we need to ensure they can be adjacent
# But we don't know the order - this is the hardest part

# Let's try a different approach: define possible orderings within each contig
# We'll create variables for the position of each fragment in its contig

# Position of fragment i in its contig (1-based, 0 if not used)
position = [Int(f'pos_{i}') for i in range(n_fragments)]

# For each fragment, position must be >= 1 if used, 0 if not used
for i in range(n_fragments):
    opt.add(If(is_used[i], position[i] >= 1, position[i] == 0))

# For each contig, positions must be unique and consecutive starting from 1
for c in range(1, n_max_contigs + 1):
    # Get fragments in this contig
    frags_in_contig = [i for i in range(n_fragments)]
    
    # For each fragment in this contig, its position must be unique
    # We'll use a simpler approach: ensure that if two fragments are in same contig,
    # they have different positions
    for i in frags_in_contig:
        for j in frags_in_contig:
            if i < j:
                opt.add(Implies(
                    And(contig_assignment[i] == c, contig_assignment[j] == c),
                    position[i] != position[j]
                ))

# Now, for each pair of fragments in same contig with consecutive positions,
# check overlap constraints
for c in range(1, n_max_contigs + 1):
    for i in range(n_fragments):
        for j in range(n_fragments):
            if i == j:
                continue
            
            # Check if i and j are in same contig and j is immediately after i
            # This requires position[j] == position[i] + 1
            
            # For each possible orientation combination
            for ori_i in [0, 1]:
                for ori_j in [0, 1]:
                    seq_i = fragments[f'F{i}'] if ori_i == 0 else rev_comp[f'F{i}']
                    seq_j = fragments[f'F{j}'] if ori_j == 0 else rev_comp[f'F{j}']
                    
                    # Determine min overlap based on GC content
                    gc_i = gc_forward[f'F{i}'] if ori_i == 0 else gc_reverse[f'F{i}']
                    gc_j = gc_forward[f'F{j}'] if ori_j == 0 else gc_reverse[f'F{j}']
                    min_overlap = 4 if (gc_i > 0.5 and gc_j > 0.5) else 3
                    
                    can_overlap = check_overlap(seq_i, seq_j, min_overlap)
                    
                    # If i and j are in same contig and j is immediately after i,
                    # and they have these orientations, then they must be able to overlap
                    opt.add(Implies(
                        And(
                            contig_assignment[i] == c,
                            contig_assignment[j] == c,
                            position[j] == position[i] + 1,
                            orientation[i] == (ori_i == 1),
                            orientation[j] == (ori_j == 1)
                        ),
                        can_overlap
                    ))

# 6. Start codon: for each contig, the fragment with position 1 must start with ATG
for c in range(1, n_max_contigs + 1):
    for i in range(n_fragments):
        seq_forward = fragments[f'F{i}']
        seq_reverse = rev_comp[f'F{i}']
        
        can_start_forward = seq_forward.startswith('ATG')
        can_start_reverse = seq_reverse.startswith('ATG')
        
        opt.add(Implies(
            And(contig_assignment[i] == c, position[i] == 1),
            If(orientation[i], can_start_reverse, can_start_forward)
        ))

# 7. Stop codon: for each contig, the fragment with the highest position must end with stop codon
# We need to find the maximum position in each contig
for c in range(1, n_max_contigs + 1):
    # For each fragment, check if it's the last one
    for i in range(n_fragments):
        seq_forward = fragments[f'F{i}']
        seq_reverse = rev_comp[f'F{i}']
        
        can_end_forward = any(seq_forward.endswith(codon) for codon in ['TAA', 'TAG', 'TGA'])
        can_end_reverse = any(seq_reverse.endswith(codon) for codon in ['TAA', 'TAG', 'TGA'])
        
        # Fragment i is last in contig c if:
        # 1. It's in contig c
        # 2. No other fragment in contig c has a higher position
        is_last = Bool(f'last_{c}_{i}')
        
        # Check if any other fragment has higher position
        higher_exists = Or([And(contig_assignment[j] == c, position[j] > position[i]) 
                           for j in range(n_fragments) if j != i])
        
        opt.add(is_last == And(contig_assignment[i] == c, Not(higher_exists)))
        
        # If it's the last fragment, it must end with stop codon
        opt.add(Implies(is_last,
                       If(orientation[i], can_end_reverse, can_end_forward)))

# 8. Minimize number of contigs
num_contigs = Sum([If(contig_exists[c-1], 1, 0) for c in range(1, n_max_contigs + 1)])
opt.minimize(num_contigs)

# Also minimize number of chimeric fragments (use as secondary objective)
num_chimeric = Sum([If(Not(is_used[i]), 1, 0) for i in range(n_fragments)])
opt.minimize(num_chimeric)

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
                contigs[contig_id] = {'fragments': [], 'orientations': [], 'positions': []}
            contigs[contig_id]['fragments'].append(f'F{i}')
            orient = 'reverse' if model.eval(orientation[i]) else 'forward'
            contigs[contig_id]['orientations'].append(orient)
            pos = model.eval(position[i])
            contigs[contig_id]['positions'].append(pos)
    
    # Sort fragments by position within each contig
    for contig_id in contigs:
        frags = list(zip(contigs[contig_id]['fragments'], 
                        contigs[contig_id]['orientations'], 
                        contigs[contig_id]['positions']))
        frags.sort(key=lambda x: x[2])  # Sort by position
        contigs[contig_id]['fragments'] = [f[0] for f in frags]
        contigs[contig_id]['orientations'] = [f[1] for f in frags]
    
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
        
        # Verify start codon
        if seq.startswith('ATG'):
            print(f"  ✓ Starts with ATG")
        else:
            print(f"  ✗ Does NOT start with ATG")
        
        # Verify stop codon
        has_stop = any(seq.endswith(codon) for codon in ['TAA', 'TAG', 'TGA'])
        if has_stop:
            print(f"  ✓ Ends with stop codon")
        else:
            print(f"  ✗ Does NOT end with stop codon")
    
    # Check if we have 2 contigs as expected
    if len(contigs) == 2:
        print("\nFound expected minimum of 2 contigs")
    else:
        print(f"\nFound {len(contigs)} contigs, expected 2")
        
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")