from z3 import *

# Define fragments
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

# Function to compute reverse complement
def reverse_complement(seq):
    comp = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    return ''.join(comp[b] for b in reversed(seq))

# Precompute reverse complements
rev_comps = [reverse_complement(f) for f in fragments]

# Compute GC-content and high GC flag
def gc_content(seq):
    gc = sum(1 for b in seq if b in 'GC')
    return gc / len(seq)

gc_contents = [gc_content(f) for f in fragments]
high_gc = [gc > 0.5 for gc in gc_contents]

# Precompute start_ok and end_ok for each fragment and orientation
def starts_with_atg(seq):
    return seq[:3] == "ATG"

def ends_with_stop(seq):
    return seq[-3:] in ["TAA", "TAG", "TGA"]

start_ok = [[starts_with_atg(f), starts_with_atg(rev_comps[i])] for i, f in enumerate(fragments)]
end_ok = [[ends_with_stop(f), ends_with_stop(rev_comps[i])] for i, f in enumerate(fragments)]

# Precompute maximum overlap between fragments in given orientations
def max_overlap(s1, s2):
    """Find maximum k such that s1[-k:] == s2[:k]"""
    max_k = 0
    for k in range(1, min(len(s1), len(s2)) + 1):
        if s1[-k:] == s2[:k]:
            max_k = k
    return max_k

# Create overlap matrix: overlap[i][j][ori_i][ori_j]
overlap = [[[[0 for _ in range(2)] for _ in range(2)] for _ in range(9)] for _ in range(9)]
for i in range(9):
    for j in range(9):
        if i != j:
            # Forward-forward
            overlap[i][j][0][0] = max_overlap(fragments[i], fragments[j])
            # Forward-reverse
            overlap[i][j][0][1] = max_overlap(fragments[i], rev_comps[j])
            # Reverse-forward
            overlap[i][j][1][0] = max_overlap(rev_comps[i], fragments[j])
            # Reverse-reverse
            overlap[i][j][1][1] = max_overlap(rev_comps[i], rev_comps[j])

# Required minimum overlap based on GC-content
def required_min(i, j):
    if high_gc[i] and high_gc[j]:
        return 4
    else:
        return 3

# Create solver
solver = Optimize()

# Variables
used = [Bool(f'used_{i}') for i in range(9)]
chimeric = [Bool(f'chimeric_{i}') for i in range(9)]
orientation = [Bool(f'ori_{i}') for i in range(9)]  # False=forward, True=reverse
is_start = [Bool(f'start_{i}') for i in range(9)]
is_end = [Bool(f'end_{i}') for i in range(9)]
next_var = [[Bool(f'next_{i}_{j}') for j in range(9)] for i in range(9)]
order = [Int(f'order_{i}') for i in range(9)]

# Each fragment is either used or chimeric, not both
for i in range(9):
    solver.add(used[i] == Not(chimeric[i]))

# If used, orientation must be valid (forward or reverse)
for i in range(9):
    solver.add(Implies(used[i], Or(Not(orientation[i]), orientation[i])))

# Start and end constraints
for i in range(9):
    # If used and is_start, must start with ATG in chosen orientation
    solver.add(Implies(And(used[i], is_start[i]), 
                      If(orientation[i], start_ok[i][1], start_ok[i][0])))
    # If used and is_end, must end with stop codon in chosen orientation
    solver.add(Implies(And(used[i], is_end[i]), 
                      If(orientation[i], end_ok[i][1], end_ok[i][0])))

# Next constraints and overlap requirements
for i in range(9):
    for j in range(9):
        if i != j:
            # If next[i][j] is true, both must be used
            solver.add(Implies(next_var[i][j], And(used[i], used[j])))
            # Overlap requirement
            solver.add(Implies(next_var[i][j],
                              If(And(orientation[i], orientation[j]),
                                 overlap[i][j][1][1] >= required_min(i, j),
                              If(And(Not(orientation[i]), orientation[j]),
                                 overlap[i][j][0][1] >= required_min(i, j),
                              If(And(orientation[i], Not(orientation[j])),
                                 overlap[i][j][1][0] >= required_min(i, j),
                                 overlap[i][j][0][0] >= required_min(i, j))))))

# Each fragment has at most one predecessor and at most one successor
for i in range(9):
    solver.add(Sum([If(next_var[j][i], 1, 0) for j in range(9)]) <= 1)
    solver.add(Sum([If(next_var[i][j], 1, 0) for j in range(9)]) <= 1)

# Start fragments have no predecessor, end fragments have no successor
for i in range(9):
    solver.add(Implies(is_start[i], Sum([If(next_var[j][i], 1, 0) for j in range(9)]) == 0))
    solver.add(Implies(is_end[i], Sum([If(next_var[i][j], 1, 0) for j in range(9)]) == 0))

# Internal fragments (not start/end) must have exactly one predecessor and one successor
for i in range(9):
    solver.add(Implies(And(used[i], Not(is_start[i]), Not(is_end[i])),
                      And(Sum([If(next_var[j][i], 1, 0) for j in range(9)]) == 1,
                          Sum([If(next_var[i][j], 1, 0) for j in range(9)]) == 1)))

# Acyclicity: if next[i][j] then order[i] < order[j]
for i in range(9):
    for j in range(9):
        if i != j:
            solver.add(Implies(next_var[i][j], order[i] < order[j]))

# Order must be between 0 and 8
for i in range(9):
    solver.add(order[i] >= 0)
    solver.add(order[i] <= 8)

# Minimize number of contigs (number of starts)
num_contigs = Sum([If(is_start[i], 1, 0) for i in range(9)])
solver.minimize(num_contigs)

# Ensure all used fragments are connected in paths
for i in range(9):
    solver.add(Implies(used[i],
                      Or(is_start[i], is_end[i],
                         And(Sum([If(next_var[j][i], 1, 0) for j in range(9)]) == 1,
                             Sum([If(next_var[i][j], 1, 0) for j in range(9)]) == 1))))

# Check and print results
result = solver.check()
if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Extract solution
    used_fragments = []
    chimeric_fragments = []
    contigs = []
    
    # Find which fragments are used and which are chimeric
    for i in range(9):
        if is_true(model[used[i]]):
            used_fragments.append(i)
        if is_true(model[chimeric[i]]):
            chimeric_fragments.append(i)
    
    # Build contigs from next relations
    visited = set()
    for i in range(9):
        if is_true(model[is_start[i]]) and i not in visited:
            # Start of a new contig
            contig = []
            current = i
            while current is not None:
                contig.append(current)
                visited.add(current)
                # Find next fragment
                next_found = False
                for j in range(9):
                    if is_true(model[next_var[current][j]]):
                        current = j
                        next_found = True
                        break
                if not next_found:
                    current = None
            contigs.append(contig)
    
    # Print contigs
    print(f"Number of contigs: {len(contigs)}")
    for idx, contig in enumerate(contigs):
        print(f"Contig {idx}:")
        print(f"  Fragments: {contig}")
        orientations = []
        for frag in contig:
            ori = "reverse" if is_true(model[orientation[frag]]) else "forward"
            orientations.append(ori)
        print(f"  Orientations: {orientations}")
        # Build sequence
        seq = ""
        for k, frag in enumerate(contig):
            ori = is_true(model[orientation[frag]])
            frag_seq = rev_comps[frag] if ori else fragments[frag]
            if k == 0:
                seq = frag_seq
            else:
                # Find overlap with previous fragment
                prev_frag = contig[k-1]
                prev_ori = is_true(model[orientation[prev_frag]])
                prev_seq = rev_comps[prev_frag] if prev_ori else fragments[prev_frag]
                # Find actual overlap length
                overlap_len = 0
                for l in range(min(len(prev_seq), len(frag_seq)), 0, -1):
                    if prev_seq[-l:] == frag_seq[:l]:
                        overlap_len = l
                        break
                seq += frag_seq[overlap_len:]
        print(f"  Sequence: {seq}")
        # Verify start and end
        print(f"  Starts with ATG: {seq[:3] == 'ATG'}")
        print(f"  Ends with stop: {seq[-3:] in ['TAA', 'TAG', 'TGA']}")
    
    # Print chimeric fragments
    print(f"Chimeric fragments: {chimeric_fragments}")
    for i in chimeric_fragments:
        print(f"  F{i}: {fragments[i]}")
    
    # Verify solution meets constraints
    print("\nVerification:")
    print(f"All fragments accounted for: {len(used_fragments) + len(chimeric_fragments) == 9}")
    print(f"Number of contigs minimized: {len(contigs)}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No solution found - problem may be unsatisfiable")
else:
    print("STATUS: unknown")
    print("Solver returned unknown")