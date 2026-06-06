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

# Reverse-complement function
def reverse_complement(seq):
    comp = {"A": "T", "T": "A", "C": "G", "G": "C"}
    return "".join(comp[base] for base in reversed(seq))

# Solver setup
solver = Solver()

# Decision variables
# contig_id[fid] = cid if fragment fid is in contig cid, else -1
contig_id = [Int(f"contig_id_{fid}") for fid in range(9)]

# orientation[fid] = True for forward, False for reverse-complement
orientation = [Bool(f"orientation_{fid}") for fid in range(9)]

# chimeric[fid] = True if fragment fid is chimeric
chimeric = [Bool(f"chimeric_{fid}") for fid in range(9)]

# Each fragment is either in a contig or chimeric
for fid in range(9):
    solver.add(Or(contig_id[fid] >= 0, chimeric[fid]))
    solver.add(Implies(chimeric[fid], contig_id[fid] == -1))
    solver.add(Implies(Not(chimeric[fid]), contig_id[fid] >= 0))

# Assume a maximum of 3 contigs (as the expected minimum is 2)
max_contigs = 3

# For each contig, we will track the fragments and their order
# We will use a list of fragment IDs for each contig
contig_fragments = [[Int(f"contig_{cid}_fragment_{i}") for i in range(9)] for cid in range(max_contigs)]

# For each contig, we will track the orientations of the fragments
contig_orientations = [[Bool(f"contig_{cid}_fragment_{i}_orientation") for i in range(9)] for cid in range(max_contigs)]

# For each contig, we will track the number of fragments in the contig
contig_length = [Int(f"contig_{cid}_length") for cid in range(max_contigs)]

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

# Check for satisfiability
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Solution found!")
    
    # Extract the contigs
    contigs = []
    for cid in range(max_contigs):
        fragments_in_contig = []
        orientations_in_contig = []
        for i in range(9):
            fid = model.eval(contig_fragments[cid][i])
            if fid is not None and fid.as_long() >= 0:
                fragments_in_contig.append(fid.as_long())
                orientations_in_contig.append("forward" if model.eval(orientation[fid]) else "reverse")
        if fragments_in_contig:
            contigs.append({
                "contig_id": cid,
                "fragments": fragments_in_contig,
                "orientations": orientations_in_contig,
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