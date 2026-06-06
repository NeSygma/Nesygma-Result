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

# Precompute oriented sequences
forward_seq = fragments
rev_seq = [revcomp(s) for s in fragments]
# orientation: True = forward, False = reverse
orient_seq = {True: forward_seq, False: rev_seq}

# Start/stop codon checks per orientation
stop_codons = {"TAA","TAG","TGA"}
start_ATG = [[False, False] for _ in range(n)]  # [i][0]=forward, [i][1]=reverse
end_stop = [[False, False] for _ in range(n)]
for i in range(n):
    for idx, ori in enumerate([True, False]):
        seq = orient_seq[ori][i]
        start_ATG[i][idx] = seq.startswith("ATG")
        end_stop[i][idx] = any(seq.endswith(stop) for stop in stop_codons)

# GC high flag
GC_high = [gc_content(frag) for frag in fragments]

# Overlap feasibility for each ordered pair and orientation combination
overlap_ok = {}
for i in range(n):
    for j in range(n):
        if i == j:
            continue
        for oi in (True, False):
            for oj in (True, False):
                seq_i = orient_seq[oi][i]
                seq_j = orient_seq[oj][j]
                req = 4 if (GC_high[i] and GC_high[j]) else 3
                possible = False
                max_olap = min(len(seq_i), len(seq_j))
                for k in range(req, max_olap+1):
                    if seq_i[-k:] == seq_j[:k]:
                        possible = True
                        break
                overlap_ok[(i,j,oi,oj)] = possible

# Z3 model
solver = Optimize()

# Variables
orient = [Bool(f"orient_{i}") for i in range(n)]   # True = forward, False = reverse
excluded = [Bool(f"excl_{i}") for i in range(n)]
next_f = [Int(f"next_{i}") for i in range(n)]   # -1 means no successor
prev_f = [Int(f"prev_{i}") for i in range(n)]   # -1 means no predecessor
pos = [Int(f"pos_{i}") for i in range(n)]       # ordering index, -1 if excluded

# Domain constraints for next/prev/pos
for i in range(n):
    solver.add(Or(next_f[i] == -1, And(next_f[i] >= 0, next_f[i] < n)))
    solver.add(Or(prev_f[i] == -1, And(prev_f[i] >= 0, prev_f[i] < n)))
    solver.add(Or(pos[i] == -1, And(pos[i] >= 0, pos[i] < n)))

# Exclusion forces no links
for i in range(n):
    solver.add(Implies(excluded[i], And(next_f[i] == -1, prev_f[i] == -1, pos[i] == -1)))

# Consistency of next/prev and overlap condition when linked
for i in range(n):
    for j in range(n):
        if i == j:
            continue
        # linking constraints
        solver.add(Implies(next_f[i] == j, prev_f[j] == i))
        solver.add(Implies(prev_f[i] == j, next_f[j] == i))
        # Overlap condition based on orientations
        overlap_cond = Or(
            And(orient[i], orient[j], BoolVal(overlap_ok[(i,j,True,True)])),
            And(orient[i], Not(orient[j]), BoolVal(overlap_ok[(i,j,True,False)])),
            And(Not(orient[i]), orient[j], BoolVal(overlap_ok[(i,j,False,True)])),
            And(Not(orient[i]), Not(orient[j]), BoolVal(overlap_ok[(i,j,False,False)]))
        )
        solver.add(Implies(next_f[i] == j, overlap_cond))

# Position ordering for linked fragments
for i in range(n):
    for j in range(n):
        if i == j:
            continue
        solver.add(Implies(next_f[i] == j, pos[j] == pos[i] + 1))
        solver.add(Implies(prev_f[i] == j, pos[i] == pos[j] + 1))

# At most one predecessor and one successor per fragment
for i in range(n):
    preds = [If(next_f[k] == i, 1, 0) for k in range(n) if k != i]
    solver.add(Sum(preds) <= 1)
    succs = [If(prev_f[k] == i, 1, 0) for k in range(n) if k != i]
    solver.add(Sum(succs) <= 1)

# Start codon constraint for contig starts (prev == -1 and not excluded)
for i in range(n):
    is_start = And(prev_f[i] == -1, Not(excluded[i]))
    start_cond = If(orient[i], BoolVal(start_ATG[i][0]), BoolVal(start_ATG[i][1]))
    solver.add(Implies(is_start, start_cond))
    # End codon constraint for contig ends (next == -1 and not excluded)
    is_end = And(next_f[i] == -1, Not(excluded[i]))
    end_cond = If(orient[i], BoolVal(end_stop[i][0]), BoolVal(end_stop[i][1]))
    solver.add(Implies(is_end, end_cond))

# Minimize number of contigs (starts)
num_contigs = Sum([If(And(prev_f[i] == -1, Not(excluded[i])), 1, 0) for i in range(n)])
solver.minimize(num_contigs)

# Solve
if solver.check() == sat:
    m = solver.model()
    contig_map = {}
    visited = set()
    for i in range(n):
        if is_true(m.eval(excluded[i])):
            continue
        if m.eval(prev_f[i]).as_long() == -1 and i not in visited:
            # start a new contig
            cur = i
            frags = []
            orients = []
            seq_parts = []
            while cur != -1 and cur not in visited:
                visited.add(cur)
                frags.append(cur)
                ori = is_true(m.eval(orient[cur]))
                orients.append('forward' if ori else 'reverse')
                seq_parts.append(forward_seq[cur] if ori else rev_seq[cur])
                nxt = m.eval(next_f[cur]).as_long()
                cur = nxt
            # Build full sequence by merging overlaps
            full_seq = seq_parts[0]
            for k in range(1, len(seq_parts)):
                prev_seq = seq_parts[k-1]
                cur_seq = seq_parts[k]
                req = 4 if (GC_high[frags[k-1]] and GC_high[frags[k]]) else 3
                overlap_len = 0
                for ol in range(req, min(len(prev_seq), len(cur_seq)) + 1):
                    if prev_seq[-ol:] == cur_seq[:ol]:
                        overlap_len = ol
                full_seq = full_seq + cur_seq[overlap_len:]
            cid = len(contig_map) + 1
            contig_map[cid] = {
                'fragments': frags,
                'orientations': orients,
                'sequence': full_seq
            }
    chimeric = [i for i in range(n) if is_true(m.eval(excluded[i]))]
    print("STATUS: sat")
    print("contigs = {")
    for cid, info in contig_map.items():
        print(f"  {cid}: {{'fragments': {info['fragments']}, 'orientations': {info['orientations']}, 'sequence': '{info['sequence']}'}}")
    print("}")
    print("excluded = {'chimeric':", chimeric, "}")
else:
    print("STATUS: unsat")