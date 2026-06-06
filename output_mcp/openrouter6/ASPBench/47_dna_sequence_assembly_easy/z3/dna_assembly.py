from z3 import *

# Fragments
fragments = [
    "ATCGATCG",
    "CGATCGTA",
    "ATCGTAAC",
    "CGTAACGG",
    "TAACGGCT",
    "ACGGCTGA",
    "GGCTGAAA",
    "CTGAAATC"
]

# Precompute overlap matrix O[i][j] = max overlap length between fragment i and j (>=3)
# Based on manual calculation
O = [[0]*8 for _ in range(8)]
# Fill with known overlaps
O[0][1] = 6
O[0][2] = 4
O[1][2] = 6
O[1][3] = 4
O[2][3] = 6
O[2][4] = 4
O[3][4] = 6
O[3][5] = 4
O[4][5] = 6
O[4][6] = 4
O[5][6] = 6
O[5][7] = 4
O[6][7] = 6

# Also check reverse overlaps? For assembly, direction matters: we only consider
# overlap where fragment i's suffix matches fragment j's prefix.
# So O[i][j] is defined only for that direction. Reverse direction may have different overlap.
# We need to compute reverse overlaps as well.
# Let's compute reverse overlaps (j,i) where j's suffix matches i's prefix.
# We'll compute manually.

# Fragment 1 suffix vs fragment 0 prefix: CGATCGTA vs ATCGATCG
# Check overlap: suffix of 1 vs prefix of 0.
# Length 3: "GTA" vs "ATC"? No.
# Length 4: "CGTA" vs "ATCG"? No.
# Length 5: "TCGTA" vs "ATCGA"? No.
# Length 6: "ATCGTA" vs "ATCGAT"? No.
# So no overlap >=3.

# Similarly, we need to compute all reverse overlaps.
# Let's write a small function to compute overlap between two strings.
def max_overlap(s1, s2):
    """Return max overlap length where suffix of s1 matches prefix of s2, at least 3."""
    max_len = 0
    for l in range(3, min(len(s1), len(s2)) + 1):
        if s1[-l:] == s2[:l]:
            max_len = l
    return max_len

# Compute full overlap matrix
O_full = [[0]*8 for _ in range(8)]
for i in range(8):
    for j in range(8):
        if i != j:
            O_full[i][j] = max_overlap(fragments[i], fragments[j])

# Print matrix for verification
print("Overlap matrix (i->j):")
for i in range(8):
    for j in range(8):
        print(f"{O_full[i][j]:2d}", end=" ")
    print()

# Now use O_full in the model.

# Create solver
solver = Optimize()

# Variables: order[k] = fragment index at position k (0..7)
order = [Int(f'order_{k}') for k in range(8)]

# All order[k] in 0..7
for k in range(8):
    solver.add(order[k] >= 0, order[k] <= 7)

# All distinct
solver.add(Distinct(order))

# For each consecutive pair, ensure overlap >= 3
for k in range(7):
    i = order[k]
    j = order[k+1]
    # We need to enforce that O_full[i][j] >= 3.
    # Since O_full is a constant matrix, we can use a big constraint:
    # For each possible pair (a,b), if i==a and j==b then O_full[a][b] >= 3.
    # We'll use an Or-loop over all pairs.
    constraints = []
    for a in range(8):
        for b in range(8):
            if O_full[a][b] >= 3:
                constraints.append(And(i == a, j == b))
    solver.add(Or(constraints))

# Maximize total overlap
total_overlap = Int('total_overlap')
solver.add(total_overlap == Sum([O_full[order[k]][order[k+1]] for k in range(7)]))
solver.maximize(total_overlap)

# Check
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Optimal total overlap:", m[total_overlap])
    # Extract order
    assembly_path = [m[order[k]] for k in range(8)]
    print("Assembly path (fragment indices):", assembly_path)
    # Compute consensus sequence
    # Start with first fragment
    consensus = fragments[assembly_path[0]]
    for k in range(1, 8):
        prev = fragments[assembly_path[k-1]]
        curr = fragments[assembly_path[k]]
        # Find overlap length
        ov = O_full[assembly_path[k-1]][assembly_path[k]]
        # Append curr without overlapping part
        consensus += curr[ov:]
    print("Consensus sequence:", consensus)
    # Print overlap details
    print("Overlap details:")
    for k in range(7):
        i = assembly_path[k]
        j = assembly_path[k+1]
        ov = O_full[i][j]
        # Position1: start of overlap in fragment i (length of i minus ov)
        pos1 = len(fragments[i]) - ov
        # Position2: start of overlap in fragment j (0)
        pos2 = 0
        print(f"  Pair {k}: fragment {i} -> fragment {j}, overlap {ov}, pos1={pos1}, pos2={pos2}")
elif result == unsat:
    print("STATUS: unsat")
    print("No valid assembly found")
else:
    print("STATUS: unknown")