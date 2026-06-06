from z3 import *

# Problem data
fragments = [
    "ATCGATCG",  # 0
    "CGATCGTA",  # 1
    "ATCGTAAC",  # 2
    "CGTAACGG",  # 3
    "TAACGGCT",  # 4
    "ACGGCTGA",  # 5
    "GGCTGAAA",  # 6
    "CTGAAATC"   # 7
]
N = len(fragments)

# Precompute overlap lengths (suffix of a matches prefix of b)

def overlap_len(a, b):
    max_k = min(len(a), len(b))
    best = 0
    for k in range(1, max_k+1):
        if a[-k:] == b[:k]:
            best = k
    return best

overlap = [[0]*N for _ in range(N)]
for i in range(N):
    for j in range(N):
        if i != j:
            overlap[i][j] = overlap_len(fragments[i], fragments[j])

# Solver
opt = Optimize()
# Position variables: pos[i] is the position (0..N-1) of fragment i in the assembly
pos = [Int(f"pos_{i}") for i in range(N)]
for i in range(N):
    opt.add(pos[i] >= 0, pos[i] < N)
opt.add(Distinct(pos))

# Adjacency constraints: if pos[i]+1 == pos[j] then overlap[i][j] >= 3
for i in range(N):
    for j in range(N):
        if i != j:
            opt.add(Implies(pos[i] + 1 == pos[j], overlap[i][j] >= 3))

# Objective: maximize total overlap of adjacent pairs
obj = Sum([If(pos[i] + 1 == pos[j], overlap[i][j], 0) for i in range(N) for j in range(N)])
opt.maximize(obj)

# Check
result = opt.check()
if result == sat:
    m = opt.model()
    # Build ordering by position
    ordering = [None]*N
    for i in range(N):
        ordering[m[pos[i]].as_long()] = i
    # Compute consensus sequence
    consensus = fragments[ordering[0]]
    total_overlap = 0
    overlap_details = []
    for idx in range(N-1):
        a = ordering[idx]
        b = ordering[idx+1]
        ol = overlap[a][b]
        total_overlap += ol
        # start positions
        pos1 = len(fragments[a]) - ol
        pos2 = 0
        overlap_details.append({
            'fragment1': a,
            'fragment2': b,
            'overlap_length': ol,
            'position1': pos1,
            'position2': pos2
        })
        # Append non-overlapping part of b
        consensus += fragments[b][ol:]
    # Output
    print("STATUS: sat")
    print("consensus_sequence:", consensus)
    print("assembly_path:", ordering)
    print("overlap_details:")
    for d in overlap_details:
        print(d)
    print("total_overlap:", total_overlap)
elif result == unsat:
    print("STATUS: unsat")
    if True:  # BENCHMARK_MODE is ON
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")