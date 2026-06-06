% DNA Fragment Assembly Problem

% Fragments and their lengths
len(f0, 8). len(f1, 8). len(f2, 6). len(f3, 6). len(f4, 8). len(f5, 8). len(f6, 8). len(f7, 6). len(f8, 5).

% Forward sequences
seq(f0, f, 1, a). seq(f0, f, 2, t). seq(f0, f, 3, g). seq(f0, f, 4, g). seq(f0, f, 5, g). seq(f0, f, 6, c). seq(f0, f, 7, g). seq(f0, f, 8, c).
seq(f1, f, 1, g). seq(f1, f, 2, g). seq(f1, f, 3, c). seq(f1, f, 4, g). seq(f1, f, 5, c). seq(f1, f, 6, c). seq(f1, f, 7, a). seq(f1, f, 8, t).
seq(f2, f, 1, g). seq(f2, f, 2, c). seq(f2, f, 3, c). seq(f2, f, 4, a). seq(f2, f, 5, t). seq(f2, f, 6, t).
seq(f3, f, 1, a). seq(f3, f, 2, t). seq(f3, f, 3, t). seq(f3, f, 4, t). seq(f3, f, 5, a). seq(f3, f, 6, a).
seq(f4, f, 1, a). seq(f4, f, 2, t). seq(f4, f, 3, g). seq(f4, f, 4, c). seq(f4, f, 5, c). seq(f4, f, 6, t). seq(f4, f, 7, c). seq(f4, f, 8, g).
seq(f5, f, 1, g). seq(f5, f, 2, c). seq(f5, f, 3, t). seq(f5, f, 4, c). seq(f5, f, 5, g). seq(f5, f, 6, a). seq(f5, f, 7, g). seq(f5, f, 8, g).
seq(f6, f, 1, t). seq(f6, f, 2, c). seq(f6, f, 3, g). seq(f6, f, 4, a). seq(f6, f, 5, g). seq(f6, f, 6, c). seq(f6, f, 7, t). seq(f6, f, 8, g).
seq(f7, f, 1, a). seq(f7, f, 2, g). seq(f7, f, 3, c). seq(f7, f, 4, t). seq(f7, f, 5, g). seq(f7, f, 6, a).
seq(f8, f, 1, a). seq(f8, f, 2, t). seq(f8, f, 3, t). seq(f8, f, 4, c). seq(f8, f, 5, g).

% Reverse complement sequences
seq(f0, r, 1, g). seq(f0, r, 2, c). seq(f0, r, 3, g). seq(f0, r, 4, c). seq(f0, r, 5, c). seq(f0, r, 6, c). seq(f0, r, 7, a). seq(f0, r, 8, t).
seq(f1, r, 1, a). seq(f1, r, 2, t). seq(f1, r, 3, g). seq(f1, r, 4, g). seq(f1, r, 5, c). seq(f1, r, 6, g). seq(f1, r, 7, c). seq(f1, r, 8, c).
seq(f2, r, 1, a). seq(f2, r, 2, a). seq(f2, r, 3, t). seq(f2, r, 4, g). seq(f2, r, 5, g). seq(f2, r, 6, c).
seq(f3, r, 1, t). seq(f3, r, 2, t). seq(f3, r, 3, a). seq(f3, r, 4, a). seq(f3, r, 5, a). seq(f3, r, 6, t).
seq(f4, r, 1, c). seq(f4, r, 2, g). seq(f4, r, 3, a). seq(f4, r, 4, g). seq(f4, r, 5, g). seq(f4, r, 6, c). seq(f4, r, 7, a). seq(f4, r, 8, t).
seq(f5, r, 1, c). seq(f5, r, 2, c). seq(f5, r, 3, t). seq(f5, r, 4, c). seq(f5, r, 5, g). seq(f5, r, 6, a). seq(f5, r, 7, g). seq(f5, r, 8, c).
seq(f6, r, 1, c). seq(f6, r, 2, a). seq(f6, r, 3, g). seq(f6, r, 4, c). seq(f6, r, 5, t). seq(f6, r, 6, c). seq(f6, r, 7, g). seq(f6, r, 8, a).
seq(f7, r, 1, t). seq(f7, r, 2, c). seq(f7, r, 3, a). seq(f7, r, 4, g). seq(f7, r, 5, c). seq(f7, r, 6, t).
seq(f8, r, 1, c). seq(f8, r, 2, g). seq(f8, r, 3, a). seq(f8, r, 4, a). seq(f8, r, 5, t).

% Orientations
orientation(f). orientation(r).

% Fragment domain
fragment(F) :- len(F, _).

% GC content: mark GC bases
gc_base(B) :- B = g ; B = c.

% Count GC bases in forward orientation (GC content is independent of orientation)
gc_count(F, Count) :-
    len(F, Len),
    Count = #count { P : seq(F, f, P, B), gc_base(B) }.

% GC > 50%
gc_gt_50(F) :-
    gc_count(F, Count),
    len(F, Len),
    Count * 100 > Len * 50.

% Choose orientation for each fragment (or exclude)
{ used(F, O) : orientation(O) } 1 :- fragment(F).

% Excluded fragments
excluded(F) :- fragment(F), not used(F, f), not used(F, r).

% Overlap possible: suffix of F1 matches prefix of F2 for length L
overlap_possible(F1, O1, F2, O2, L) :-
    len(F1, Len1), len(F2, Len2),
    L <= Len1, L <= Len2,
    1 <= L,
    1 { seq(F1, O1, Len1 - L + P, B) = seq(F2, O2, P, B) : P = 1..L } L.

% Maximum overlap
max_overlap(F1, O1, F2, O2, Lmax) :-
    used(F1, O1), used(F2, O2),
    Lmax = #max { L : overlap_possible(F1, O1, F2, O2, L) }.

% Minimum overlap based on GC content
min_overlap(F1, O1, F2, O2, Lmin) :-
    used(F1, O1), used(F2, O2),
    gc_gt_50(F1), gc_gt_50(F2),
    Lmin = 4.

min_overlap(F1, O1, F2, O2, Lmin) :-
    used(F1, O1), used(F2, O2),
    (not gc_gt_50(F1) ; not gc_gt_50(F2)),
    Lmin = 3.

% Choose which fragments are adjacent (next) and choose overlap length
{ next(F1, F2) : used(F1, _), used(F2, _), F1 != F2 } :- fragment(F1), fragment(F2).

% Each fragment can have at most one successor and one predecessor
{ next(F, _) } 1 :- used(F, _).
{ next(_, F) } 1 :- used(F, _).

% For each next pair, choose an overlap length that satisfies constraints
{ chosen_overlap(F1, O1, F2, O2, L) : L = Lmin..Lmax } 1 :-
    next(F1, F2),
    used(F1, O1), used(F2, O2),
    max_overlap(F1, O1, F2, O2, Lmax),
    min_overlap(F1, O1, F2, O2, Lmin).

% Overlap used is the chosen overlap
overlap_used(F1, F2, L) :-
    chosen_overlap(F1, O1, F2, O2, L),
    used(F1, O1), used(F2, O2).

% Contig starts and ends
contig_start(F) :- used(F, _), not next(_, F).
contig_end(F) :- used(F, _), not next(F, _).

% Start codon check (ATG)
start_codon_ok(F) :-
    contig_start(F),
    used(F, O),
    seq(F, O, 1, a),
    seq(F, O, 2, t),
    seq(F, O, 3, g).

% Stop codon check (TAA, TAG, TGA)
stop_codon_ok(F) :-
    contig_end(F),
    used(F, O),
    len(F, Len),
    seq(F, O, Len-2, B1), seq(F, O, Len-1, B2), seq(F, O, Len, B3),
    (B1 = t, B2 = a, B3 = a ; B1 = t, B2 = a, B3 = g ; B1 = t, B2 = g, B3 = a).

% Enforce start and stop codons
:- contig_start(F), not start_codon_ok(F).
:- contig_end(F), not stop_codon_ok(F).

% Forbid cycles in contigs
reachable(F1, F2) :- next(F1, F2).
reachable(F1, F3) :- reachable(F1, F2), next(F2, F3).
:- reachable(F, F).

% Assign contig IDs to starts (using fragment order)
frag_index(f0, 0). frag_index(f1, 1). frag_index(f2, 2). frag_index(f3, 3). frag_index(f4, 4).
frag_index(f5, 5). frag_index(f6, 6). frag_index(f7, 7). frag_index(f8, 8).

% Compute the number of contig starts before F
contig_start_count(F, C) :-
    contig_start(F),
    C = #count { G : contig_start(G), frag_index(G, IG), frag_index(F, IF), IG < IF }.

% Contig ID: assign sequential IDs to contig starts
contig_id(F, ID) :-
    contig_start(F),
    contig_start_count(F, C),
    ID = C + 1.

% Propagate contig ID along the chain
contig_id(F2, ID) :- next(F1, F2), contig_id(F1, ID).

% Position of fragment within contig
contig_position(F, 1) :- contig_start(F).
contig_position(F2, P2) :- next(F1, F2), contig_position(F1, P1), P2 = P1 + 1.

% Output contig fragments
contig(contig_id, fragment, position, orientation) :-
    contig_id(F, ID), contig_position(F, Pos), used(F, O).

% Compute start position of each fragment in the contig sequence
contig_start_pos(F, S) :- contig_start(F), S = 1.
contig_start_pos(F2, S2) :- next(F1, F2), contig_start_pos(F1, S1), len(F1, Len1), overlap_used(F1, F2, L), S2 = S1 + Len1 - L.

% Contig base at each position
contig_base(ID, Pos, Base) :-
    contig_id(F, ID),
    contig_start_pos(F, S),
    used(F, O),
    len(F, Len),
    1 <= P <= Len,
    Pos = S + P - 1,
    seq(F, O, P, Base).

% Minimize number of contigs
#minimize { 1, F : contig_start(F) }.

% Show relevant predicates
#show contig/4.
#show contig_base/3.
#show excluded/1.