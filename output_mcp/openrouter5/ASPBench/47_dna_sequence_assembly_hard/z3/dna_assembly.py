from z3 import *

# ============================================================
# DNA Assembly Problem - Z3 Model
# ============================================================

# Fragment data
fragments = [
    "ATGGGCGC",  # F0
    "GGCGCCAT",  # F1
    "GCCATT",    # F2
    "ATTTAA",    # F3
    "ATGCCTCG",  # F4
    "GCTCGAGG",  # F5
    "TCGAGCTG",  # F6
    "AGCTGA",    # F7
    "ATTCG"      # F8
]

N = len(fragments)  # 9

# Helper: reverse complement of a DNA string
def revcomp(s):
    comp = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
    return ''.join(comp[c] for c in reversed(s))

# Precompute all possible orientations for each fragment
# For each fragment i, we have two strings: forward and reverse-complement
fwd = fragments
rev = [revcomp(f) for f in fragments]

# Precompute GC-content for each fragment (both orientations)
def gc_content(s):
    return (s.count('G') + s.count('C')) / len(s)

gc_fwd = [gc_content(f) for f in fwd]
gc_rev = [gc_content(f) for f in rev]

# Precompute overlap feasibility between any two fragments (i at position p, j at position q)
# where p and q are orientations: 0 = forward, 1 = reverse
# We need to check if suffix of first (length >= min_overlap) matches prefix of second
# min_overlap depends on GC content of both fragments

def min_overlap(i, p, j, q):
    """Return minimum overlap required between fragment i (orient p) and j (orient q)."""
    gc_i = gc_fwd[i] if p == 0 else gc_rev[i]
    gc_j = gc_fwd[j] if q == 0 else gc_rev[j]
    if gc_i > 0.5 and gc_j > 0.5:
        return 4
    else:
        return 3

def can_overlap(i, p, j, q):
    """Check if fragment i (orient p) can be placed before fragment j (orient q)."""
    s1 = fwd[i] if p == 0 else rev[i]
    s2 = fwd[j] if q == 0 else rev[j]
    mo = min_overlap(i, p, j, q)
    max_overlap = min(len(s1), len(s2))
    for o in range(mo, max_overlap + 1):
        if s1[-o:] == s2[:o]:
            return True, o
    return False, 0

# Build overlap table: overlap_possible[i][p][j][q] = (possible, overlap_len)
# Also store the merged sequence length: len(s1) + len(s2) - overlap_len
overlap_possible = {}
merged_len = {}

for i in range(N):
    for p in range(2):
        for j in range(N):
            if i == j:
                continue
            for q in range(2):
                possible, olen = can_overlap(i, p, j, q)
                overlap_possible[(i, p, j, q)] = possible
                if possible:
                    s1 = fwd[i] if p == 0 else rev[i]
                    s2 = fwd[j] if q == 0 else rev[j]
                    merged_len[(i, p, j, q)] = len(s1) + len(s2) - olen
                else:
                    merged_len[(i, p, j, q)] = 0

# Check start codon (ATG) and stop codons (TAA, TAG, TGA)
def has_start(s):
    return s[:3] == "ATG"

def has_stop(s):
    return s[-3:] in ("TAA", "TAG", "TGA")

# For each fragment orientation, check if it can start a contig (has ATG at beginning)
# and if it can end a contig (has stop codon at end)
can_start = {}
can_end = {}
for i in range(N):
    for p in range(2):
        s = fwd[i] if p == 0 else rev[i]
        can_start[(i, p)] = has_start(s)
        can_end[(i, p)] = has_stop(s)

# ============================================================
# Decision Variables
# ============================================================

# We'll model this as: we have up to K contigs (K = 2 expected minimum)
# Each fragment is assigned to a contig (0..K-1) or marked chimeric (K)
# Within each contig, fragments are ordered

K = 2  # expected minimum number of contigs

# contig_assignment[i] = which contig fragment i belongs to (0..K-1 for included, K for chimeric)
contig_assignment = [Int(f'contig_{i}') for i in range(N)]

# orientation[i] = 0 for forward, 1 for reverse
orientation = [Int(f'orient_{i}') for i in range(N)]

# position_in_contig[i] = position (order) of fragment i within its contig (0-indexed)
position = [Int(f'pos_{i}') for i in range(N)]

solver = Solver()

# Domain constraints
for i in range(N):
    solver.add(contig_assignment[i] >= 0, contig_assignment[i] <= K)
    solver.add(orientation[i] >= 0, orientation[i] <= 1)
    solver.add(position[i] >= 0, position[i] <= N-1)

# Each contig must have at least one fragment
# (We'll enforce this implicitly through start/stop constraints)

# ============================================================
# Constraints
# ============================================================

# 1. Start codon: each contig must start with ATG
# For each contig c, there must be at least one fragment assigned to c with position 0
# and that fragment's orientation must have ATG at its start
for c in range(K):
    # At least one fragment i such that contig_assignment[i] == c and position[i] == 0 and can_start[(i, orientation[i])]
    start_possible = []
    for i in range(N):
        # We need to express: contig_assignment[i] == c AND position[i] == 0 AND 
        # (orientation[i] == 0 AND can_start[(i,0)] OR orientation[i] == 1 AND can_start[(i,1)])
        cond = And(contig_assignment[i] == c, position[i] == 0)
        orient_cond = Or(
            And(orientation[i] == 0, can_start[(i, 0)]),
            And(orientation[i] == 1, can_start[(i, 1)])
        )
        start_possible.append(And(cond, orient_cond))
    solver.add(Or(start_possible))

# 2. Stop codon: each contig must end with a stop codon
for c in range(K):
    # Find the max position in contig c
    # For each fragment i, it could be the last one
    stop_possible = []
    for i in range(N):
        # i is in contig c, and no other fragment j in contig c has position > position[i]
        is_last = True
        for j in range(N):
            if i == j:
                continue
            # If j is in same contig and has higher position, then i is not last
            is_last = And(is_last, Not(And(contig_assignment[j] == c, position[j] > position[i])))
        
        cond = And(contig_assignment[i] == c, is_last)
        orient_cond = Or(
            And(orientation[i] == 0, can_end[(i, 0)]),
            And(orientation[i] == 1, can_end[(i, 1)])
        )
        stop_possible.append(And(cond, orient_cond))
    solver.add(Or(stop_possible))

# 3. Overlap requirements between adjacent fragments in same contig
# For any two fragments i, j in the same contig with consecutive positions:
# If position[j] == position[i] + 1, then they must overlap appropriately
for i in range(N):
    for j in range(N):
        if i == j:
            continue
        for c in range(K):
            # i and j are in same contig c, j is immediately after i
            same_contig = And(contig_assignment[i] == c, contig_assignment[j] == c)
            adjacent = And(position[j] == position[i] + 1, same_contig)
            
            # They must overlap
            # For each orientation combination, check if overlap is possible
            overlap_conds = []
            for p in range(2):
                for q in range(2):
                    if overlap_possible.get((i, p, j, q), False):
                        overlap_conds.append(
                            And(orientation[i] == p, orientation[j] == q)
                        )
            
            if overlap_conds:
                solver.add(Implies(adjacent, Or(overlap_conds)))
            else:
                # No overlap possible between these two fragments in any orientation
                solver.add(Not(adjacent))

# 4. Each fragment used at most once (already enforced by contig_assignment)
# 5. Unique positions within each contig
for c in range(K):
    for i in range(N):
        for j in range(N):
            if i < j:
                # If both in same contig, positions must be different
                same_contig = And(contig_assignment[i] == c, contig_assignment[j] == c)
                solver.add(Implies(same_contig, position[i] != position[j]))

# 6. Positions within a contig must be contiguous (0, 1, 2, ...)
# For each contig c, the set of positions used must be exactly {0, 1, ..., max_pos}
# We can enforce: if a fragment has position p in contig c, then there must be fragments
# at all positions 0..p-1 in that contig
for c in range(K):
    for p in range(1, N):
        # If any fragment has position p in contig c, then there must be some fragment
        # with position p-1 in contig c
        has_p = Or([And(contig_assignment[i] == c, position[i] == p) for i in range(N)])
        has_p_minus_1 = Or([And(contig_assignment[i] == c, position[i] == p-1) for i in range(N)])
        solver.add(Implies(has_p, has_p_minus_1))

# ============================================================
# Solve
# ============================================================
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    
    # Extract solution
    assignments = {}
    for i in range(N):
        c_val = m.eval(contig_assignment[i]).as_long()
        o_val = m.eval(orientation[i]).as_long()
        p_val = m.eval(position[i]).as_long()
        assignments[i] = (c_val, o_val, p_val)
    
    # Group by contig
    contigs = {c: [] for c in range(K)}
    chimeric = []
    for i, (c, o, p) in assignments.items():
        if c == K:
            chimeric.append(i)
        else:
            contigs[c].append((i, o, p))
    
    # Sort each contig by position
    for c in contigs:
        contigs[c].sort(key=lambda x: x[2])
    
    print(f"Number of contigs: {K}")
    for c in range(K):
        if contigs[c]:
            print(f"\nContig {c}:")
            seq_parts = []
            for idx, (i, o, p) in enumerate(contigs[c]):
                s = fwd[i] if o == 0 else rev[i]
                orient_str = "forward" if o == 0 else "reverse"
                print(f"  Fragment F{i} ({orient_str}) at position {p}: {s}")
                seq_parts.append(s)
            
            # Reconstruct sequence with overlaps
            # For simplicity, just concatenate (we know overlaps exist)
            full_seq = ""
            for idx, (i, o, p) in enumerate(contigs[c]):
                s = fwd[i] if o == 0 else rev[i]
                if idx == 0:
                    full_seq = s
                else:
                    # Find overlap
                    prev_s = fwd[contigs[c][idx-1][0]] if contigs[c][idx-1][1] == 0 else rev[contigs[c][idx-1][0]]
                    mo = min_overlap(contigs[c][idx-1][0], contigs[c][idx-1][1], i, o)
                    max_o = min(len(prev_s), len(s))
                    best_o = 0
                    for oo in range(mo, max_o + 1):
                        if prev_s[-oo:] == s[:oo]:
                            best_o = oo
                    full_seq = full_seq + s[best_o:]
            print(f"  Reconstructed sequence: {full_seq}")
            print(f"  Starts with ATG: {full_seq[:3] == 'ATG'}")
            print(f"  Ends with stop: {full_seq[-3:] in ('TAA', 'TAG', 'TGA')}")
    
    if chimeric:
        print(f"\nChimeric fragments: {[f'F{i}' for i in chimeric]}")
    else:
        print("\nNo chimeric fragments")
        
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")