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

# Create solver
solver = Optimize()

# Variables: order[k] = fragment index at position k (0..7)
order = [Int(f'order_{k}') for k in range(8)]

# All order[k] in 0..7
for k in range(8):
    solver.add(order[k] >= 0, order[k] <= 7)

# All distinct
solver.add(Distinct(order))

# For each consecutive pair, define overlap variable ov_k
ov = [Int(f'ov_{k}') for k in range(7)]

# Constraint: ov_k must equal O_full[i][j] where i = order[k], j = order[k+1]
for k in range(7):
    i = order[k]
    j = order[k+1]
    # Build constraints for each possible (a,b)
    constraints = []
    for a in range(8):
        for b in range(8):
            if O_full[a][b] >= 3:
                constraints.append(And(i == a, j == b, ov[k] == O_full[a][b]))
    # At least one of these must hold (since i and j are some a,b)
    solver.add(Or(constraints))
    # Also ensure overlap >= 3 (should be satisfied by above)
    solver.add(ov[k] >= 3)

# Maximize total overlap
total_overlap = Sum(ov)
solver.maximize(total_overlap)

# Check
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    optimal_total = m.evaluate(total_overlap)
    print("Optimal total overlap:", optimal_total)
    # Extract order as Python integers
    assembly_path = [int(m[order[k]].as_long()) for k in range(8)]
    print("Assembly path (fragment indices):", assembly_path)
    # Compute consensus sequence
    consensus = fragments[assembly_path[0]]
    for k in range(1, 8):
        prev = fragments[assembly_path[k-1]]
        curr = fragments[assembly_path[k]]
        ov_len = int(m[ov[k-1]].as_long())
        consensus += curr[ov_len:]
    print("Consensus sequence:", consensus)
    # Print overlap details
    print("Overlap details:")
    overlap_details = []
    for k in range(7):
        i = assembly_path[k]
        j = assembly_path[k+1]
        ov_len = int(m[ov[k]].as_long())
        pos1 = len(fragments[i]) - ov_len
        pos2 = 0
        overlap_details.append({
            "fragment1": i,
            "fragment2": j,
            "overlap_length": ov_len,
            "position1": pos1,
            "position2": pos2
        })
        print(f"  Pair {k}: fragment {i} -> fragment {j}, overlap {ov_len}, pos1={pos1}, pos2={pos2}")
    # Print required fields
    print("\nRequired output fields:")
    print("fragments:", fragments)
    print("consensus_sequence:", consensus)
    print("assembly_path:", assembly_path)
    print("overlap_details:", overlap_details)
elif result == unsat:
    print("STATUS: unsat")
    print("No valid assembly found")
else:
    print("STATUS: unknown")