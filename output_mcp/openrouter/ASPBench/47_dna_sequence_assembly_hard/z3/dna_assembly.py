from z3 import *

# Data
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

n = len(fragments)

# Helper functions

def revcomp(seq):
    comp = {'A':'T','T':'A','C':'G','G':'C'}
    return ''.join(comp[b] for b in reversed(seq))

def gc_content(seq):
    gc = sum(1 for b in seq if b in ('G','C'))
    return gc*2 > len(seq)  # >50%

# Precompute oriented sequences and properties
forward_seq = fragments
rev_seq = [revcomp(s) for s in fragments]
# orientation: True = forward, False = reverse
orient_seq = {True: forward_seq, False: rev_seq}

# start codon requirement per fragment orientation
start_ATG = [[False, False] for _ in range(n)]  # [i][ori]
stop_codons = {"TAA","TAG","TGA"}
end_stop = [[False, False] for _ in range(n)]
for i in range(n):
    for ori in (True, False):
        seq = orient_seq[ori][i]
        start_ATG[i][ori] = seq.startswith("ATG")
        end_stop[i][ori] = any(seq.endswith(stop) for stop in stop_codons)

# Overlap possibilities
# overlap length requirement depends on GC content of both fragments (orientation independent)
GC_high = [gc_content(frag) for frag in fragments]
# compute allowed adjacency matrix for each orientation pair
overlap_ok = {}
for i in range(n):
    for j in range(n):
        if i==j: continue
        for oi in (True, False):
            for oj in (True, False):
                seq_i = orient_seq[oi][i]
                seq_j = orient_seq[oj][j]
                # required overlap length
                req = 4 if (GC_high[i] and GC_high[j]) else 3
                max_olap = min(len(seq_i), len(seq_j))
                possible = False
                for k in range(req, max_olap+1):
                    if seq_i[-k:] == seq_j[:k]:
                        possible = True
                        break
                overlap_ok[(i,j,oi,oj)] = possible

# Z3 model
solver = Optimize()

# Variables
orient = [Bool(f"orient_{i}") for i in range(n)]  # True = forward, False = reverse
excluded = [Bool(f"excl_{i}") for i in range(n)]
next_f = [Int(f"next_{i}") for i in range(n)]
prev_f = [Int(f"prev_{i}") for i in range(n)]
pos = [Int(f"pos_{i}") for i in range(n)]

# Domains
for i in range(n):
    solver.add(Or(next_f[i] == -1, And(next_f[i] >= 0, next_f[i] < n)))
    solver.add(Or(prev_f[i] == -1, And(prev_f[i] >= 0, prev_f[i] < n)))
    solver.add(Or(pos[i] == -1, And(pos[i] >= 0, pos[i] < n)))

# Exclusion constraints
for i in range(n):
    solver.add(Implies(excluded[i], And(next_f[i] == -1, prev_f[i] == -1, pos[i] == -1)))
    # If not excluded, then excluded[i] is false (implicitly by other constraints)

# Link next and prev consistency
for i in range(n):
    for j in range(n):
        if i==j: continue
        # if i's next is j then j's prev is i
        solver.add(Implies(next_f[i] == j, prev_f[j] == i))
        solver.add(Implies(prev_f[i] == j, next_f[j] == i))
        # also enforce orientation overlap condition when linked
        # encode as: (next_f[i]==j) => overlap_ok[(i,j,orient_i,orient_j)]
        # need to translate Bool orient to True/False values
        # Use ite to map Bool to Python bool index 0/1
        # We'll create a Bool expression for each case
        # Overlap condition must hold for the chosen orientations
        # Create a Bool constant for the condition
        cond = BoolVal(overlap_ok[(i,j,True,True)])
        # We'll build a big implication covering all orientation combos
        # (next_f[i]==j) => ( (orient[i] && orient[j] && cond) or ... )
        # Simpler: use If to select appropriate BoolVal
        overlap_expr = If(And(orient[i], orient[j]), BoolVal(overlap_ok[(i,j,True,True)],),
                           If(And(orient[i], Not(orient[j])), BoolVal(overlap_ok[(i,j,True,False)],),
                              If(And(Not(orient[i]), orient[j]), BoolVal(overlap_ok[(i,j,False,True)],),
                                 BoolVal(overlap_ok[(i,j,False,False)]))))
        solver.add(Implies(next_f[i] == j, overlap_expr))

# Position ordering for linked fragments
for i in range(n):
    for j in range(n):
        if i==j: continue
        solver.add(Implies(next_f[i] == j, pos[j] == pos[i] + 1))
        solver.add(Implies(prev_f[i] == j, pos[i] == pos[j] + 1))

# Ensure each fragment has at most one predecessor and one successor (already by function of variables)
# But need to prevent two different fragments pointing to same next
for i in range(n):
    # at most one predecessor: sum of indicators where next == i <=1
    preds = [If(next_f[k] == i, 1, 0) for k in range(n) if k!=i]
    solver.add(Sum(preds) <= 1)
    # at most one successor: sum of indicators where prev == i <=1
    succs = [If(prev_f[k] == i, 1, 0) for k in range(n) if k!=i]
    solver.add(Sum(succs) <= 1)

# Start and end codon constraints for contig ends (non-excluded)
for i in range(n):
    # start node: prev == -1 and not excluded
    is_start = And(prev_f[i] == -1, Not(excluded[i]))
    # enforce start codon
    start_cond = If(orient[i], BoolVal(start_ATG[i][True]), BoolVal(start_ATG[i][False]))
    solver.add(Implies(is_start, start_cond))
    # end node: next == -1 and not excluded
    is_end = And(next_f[i] == -1, Not(excluded[i]))
    end_cond = If(orient[i], BoolVal(end_stop[i][True]), BoolVal(end_stop[i][False]))
    solver.add(Implies(is_end, end_cond))

# Ensure that if a fragment is not excluded, it participates in a chain (either has prev or next or both)
for i in range(n):
    solver.add(Implies(Not(excluded[i]), Or(prev_f[i] != -1, next_f[i] != -1)))

# Minimize number of contigs = number of start nodes (prev==-1 and not excluded)
num_contigs = Sum([If(And(prev_f[i] == -1, Not(excluded[i]), 1, 0) for i in range(n)])
solver.minimize(num_contigs)

# Solve
if solver.check() == sat:
    m = solver.model()
    # Build contigs
    contig_map = {}
    for i in range(n):
        if is_true(m.eval(excluded[i])):
            continue
        if m.eval(prev_f[i]).as_long() == -1:
            # start of a contig
            cur = i
            seq_parts = []
            frags = []
            orients = []
            while cur != -1:
                frags.append(cur)
                ori = is_true(m.eval(orient[cur]))
                orients.append('forward' if ori else 'reverse')
                seq = forward_seq[cur] if ori else rev_seq[cur]
                seq_parts.append(seq)
                nxt = m.eval(next_f[cur]).as_long()
                cur = nxt
            # Build full sequence by overlapping merges
            # Simple concatenation using maximal overlap (precomputed)
            full_seq = seq_parts[0]
            for k in range(1, len(seq_parts)):
                prev_seq = seq_parts[k-1]
                cur_seq = seq_parts[k]
                # find max overlap >= required
                req = 4 if (GC_high[frags[k-1]] and GC_high[frags[k]]) else 3
                max_ol = 0
                for ol in range(req, min(len(prev_seq), len(cur_seq))+1:
                    if prev_seq[-ol:] == cur_seq[:ol]:
                        max_ol = ol
                full_seq = full_seq + cur_seq[max_ol:]
            contig_id = len(contig_map)+1
            contig_map[contig_id] = {
                'fragments': frags,
                'orientations': orients,
                'sequence': full_seq
            }
    # excluded list
    chimeric = [i for i in range(n) if is_true(m.eval(excluded[i]))]
    print("STATUS: sat")
    print("contigs = {")
    for cid, info in contig_map.items():
        print(f"  {cid}: {{'fragments': {info['fragments']}, 'orientations': {info['orientations']}, 'sequence': '{info['sequence']}'}}")
    print("}")
    print("excluded = {'chimeric':", chimeric, "}")
else:
    print("STATUS: unsat")