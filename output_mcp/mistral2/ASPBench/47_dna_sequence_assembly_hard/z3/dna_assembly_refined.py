from z3 import *

# Fragment sequences
fragments = {
    0: "ATGGGCGC",
    1: "GGCGCCAT",
    2: "GCCATT",
    3: "ATTTAA",
    4: "ATGCCTCG",
    5: "GCTCGAGG",
    6: "TCGAGCTG",
    7: "AGCTGA",
    8: "ATTCG"
}

# Precompute GC-content for each fragment
def gc_content(seq):
    gc = sum(1 for base in seq if base in "GC")
    return gc / len(seq)

gc = {fid: gc_content(seq) for fid, seq in fragments.items()}

# Reverse-complement function
def reverse_complement(seq):
    comp = {"A": "T", "T": "A", "C": "G", "G": "C"}
    return "".join(comp[base] for base in reversed(seq))

# Solver setup
solver = Optimize()

# Decision variables
# contig_id[fid] = cid if fragment fid is in contig cid, else -1
contig_id = [Int(f"contig_id_{fid}") for fid in range(9)]

# orientation[fid] = True for forward, False for reverse-complement
orientation = [Bool(f"orientation_{fid}") for fid in range(9)]

# chimeric[fid] = True if fragment fid is chimeric
chimeric = [Bool(f"chimeric_{fid}") for fid in range(9)]

# Number of contigs (to minimize)
num_contigs = Int("num_contigs")

# Each fragment is either in a contig or chimeric
for fid in range(9):
    solver.add(Or(contig_id[fid] >= 0, chimeric[fid]))
    solver.add(Implies(chimeric[fid], contig_id[fid] == -1))
    solver.add(Implies(Not(chimeric[fid]), contig_id[fid] >= 0))

# Maximum possible contigs (worst case: each fragment is its own contig)
max_contigs = 9

# For each contig, we will track the fragments and their order
# We will use a symbolic array to represent the fragments in each contig
# Since Z3 does not support symbolic lists, we will use a fixed-size array for each contig
# and assert constraints for the fragments in the contig

# We will also track the sequence of each contig
contig_sequence = [String(f"contig_sequence_{cid}") for cid in range(max_contigs)]

# For each contig, we will track the fragments and their order
# We will use a list of fragment IDs for each contig
# We will use a list of orientations for each contig

# We will use a symbolic representation for the fragments in each contig
# We will use a list of fragment IDs for each contig
# We will use a list of orientations for each contig

# For simplicity, we will assume a maximum of 3 contigs (as the expected minimum is 2)
# and assert constraints for each contig
max_contigs = 3

# For each contig, we will track the fragments and their order
# We will use a list of fragment IDs for each contig
# We will use a list of orientations for each contig

# We will use a symbolic representation for the fragments in each contig
# We will use a list of fragment IDs for each contig
# We will use a list of orientations for each contig

# For each contig, we will track the fragments and their order
contig_fragments = [[Int(f"contig_{cid}_fragment_{i}") for i in range(9)] for cid in range(max_contigs)]
contig_orientations = [[Bool(f"contig_{cid}_fragment_{i}_orientation") for i in range(9)] for cid in range(max_contigs)]

# For each contig, we will track the number of fragments in the contig
contig_length = [Int(f"contig_{cid}_length") for cid in range(max_contigs)]

# For each contig, we will track whether it is used
contig_used = [Bool(f"contig_{cid}_used") for cid in range(max_contigs)]

# For each contig, the fragments must be unique and ordered
for cid in range(max_contigs):
    # Fragments in a contig must be unique
    for i in range(9):
        for j in range(i + 1, 9):
            solver.add(contig_fragments[cid][i] != contig_fragments[cid][j])
    
    # Contig length is the number of fragments in the contig
    solver.add(contig_length[cid] >= 0)
    solver.add(contig_length[cid] <= 9)
    
    # The first 'contig_length[cid]' fragments are used, the rest are -1
    for i in range(9):
        solver.add(If(i < contig_length[cid], 
                      And(contig_fragments[cid][i] >= 0, contig_fragments[cid][i] < 9), 
                      contig_fragments[cid][i] == -1))

# Each fragment is in at most one contig
for fid in range(9):
    solver.add(Sum([If(contig_fragments[cid][i] == fid, 1, 0) for cid in range(max_contigs) for i in range(9)]) <= 1)

# For each contig, the fragments must satisfy the start codon, stop codon, and overlap constraints
for cid in range(max_contigs):
    # If the contig is used, it must have at least one fragment
    solver.add(Implies(contig_used[cid], contig_length[cid] >= 1))
    
    # For each fragment in the contig, set its orientation
    for i in range(9):
        for fid in range(9):
            solver.add(Implies(contig_fragments[cid][i] == fid, 
                              contig_orientations[cid][i] == orientation[fid]))
    
    # Start codon: first fragment must start with "ATG"
    for i in range(9):
        for fid in range(9):
            solver.add(Implies(And(contig_fragments[cid][i] == fid, i == 0), 
                              Or(
                                  And(orientation[fid], 
                                      fragments[fid][:3] == "ATG"),
                                  And(Not(orientation[fid]),
                                      reverse_complement(fragments[fid])[:3] == "ATG")
                              )))
    
    # Stop codon: last fragment must end with "TAA", "TAG", or "TGA"
    for i in range(9):
        for fid in range(9):
            solver.add(Implies(And(contig_fragments[cid][i] == fid, 
                                  contig_length[cid] > 0, 
                                  i == contig_length[cid] - 1), 
                              Or(
                                  And(orientation[fid],
                                      fragments[fid][-3:] == "TAA" or
                                      fragments[fid][-3:] == "TAG" or
                                      fragments[fid][-3:] == "TGA"),
                                  And(Not(orientation[fid]),
                                      reverse_complement(fragments[fid])[-3:] == "TAA" or
                                      reverse_complement(fragments[fid])[-3:] == "TAG" or
                                      reverse_complement(fragments[fid])[-3:] == "TGA")
                              )))
    
    # Overlap constraints between adjacent fragments
    for i in range(8):
        for fid1 in range(9):
            for fid2 in range(9):
                # Get the sequences of the two fragments in their chosen orientations
                seq1_forward = fragments[fid1]
                seq1_reverse = reverse_complement(fragments[fid1])
                seq2_forward = fragments[fid2]
                seq2_reverse = reverse_complement(fragments[fid2])
                
                # Overlap constraint: last 3 bases of seq1 must match first 3 bases of seq2
                # For forward orientation of both
                solver.add(Implies(And(contig_fragments[cid][i] == fid1, contig_fragments[cid][i+1] == fid2, 
                                      orientation[fid1], orientation[fid2]),
                                  seq1_forward[-3:] == seq2_forward[:3]))
                
                # For forward seq1 and reverse seq2
                solver.add(Implies(And(contig_fragments[cid][i] == fid1, contig_fragments[cid][i+1] == fid2, 
                                      orientation[fid1], Not(orientation[fid2])),
                                  seq1_forward[-3:] == seq2_reverse[:3]))
                
                # For reverse seq1 and forward seq2
                solver.add(Implies(And(contig_fragments[cid][i] == fid1, contig_fragments[cid][i+1] == fid2, 
                                      Not(orientation[fid1]), orientation[fid2]),
                                  seq1_reverse[-3:] == seq2_forward[:3]))
                
                # For reverse seq1 and reverse seq2
                solver.add(Implies(And(contig_fragments[cid][i] == fid1, contig_fragments[cid][i+1] == fid2, 
                                      Not(orientation[fid1]), Not(orientation[fid2])),
                                  seq1_reverse[-3:] == seq2_reverse[:3]))

# Minimize the number of contigs
solver.add(num_contigs == Sum([If(contig_used[cid], 1, 0) for cid in range(max_contigs)]))
solver.minimize(num_contigs)

# Check for satisfiability
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Solution found!")
    
    # Extract the number of contigs
    num_contigs_val = model.eval(num_contigs)
    print(f"Number of contigs: {num_contigs_val}")
    
    # Extract the contigs
    contigs = []
    for cid in range(max_contigs):
        if model.eval(contig_used[cid]) == True:
            fragments_in_contig = []
            orientations_in_contig = []
            for i in range(9):
                fid = model.eval(contig_fragments[cid][i])
                if fid is not None and fid.as_long() >= 0:
                    fragments_in_contig.append(fid.as_long())
                    orientations_in_contig.append("forward" if model.eval(orientation[fid]) else "reverse")
            contigs.append({
                "contig_id": cid,
                "fragments": fragments_in_contig,
                "orientations": orientations_in_contig,
                "sequence": "TBD"  # Placeholder; actual sequence construction is complex in Z3
            })
    
    print("Contigs:")
    for contig in contigs:
        print(f"  Contig {contig['contig_id']}: fragments {contig['fragments']}, orientations {contig['orientations']}")
    
    # Extract chimeric fragments
    chimeric_fragments = []
    for fid in range(9):
        if model.eval(chimeric[fid]) == True:
            chimeric_fragments.append(fid)
    
    print("Chimeric fragments:", chimeric_fragments)
    
elif result == unsat:
    print("STATUS: unsat")
    print("No solution found.")
else:
    print("STATUS: unknown")
    print("Unknown result.")