% DNA Fragment Assembly Problem

% Fragment definitions
fragment(0..8).

% Fragment sequences as facts (each character as separate fact)
% F0: ATGGGCGC
seq(0, 0, "A"). seq(0, 1, "T"). seq(0, 2, "G"). seq(0, 3, "G").
seq(0, 4, "G"). seq(0, 5, "C"). seq(0, 6, "G"). seq(0, 7, "C").

% F1: GGCGCCAT
seq(1, 0, "G"). seq(1, 1, "G"). seq(1, 2, "C"). seq(1, 3, "G").
seq(1, 4, "C"). seq(1, 5, "C"). seq(1, 6, "A"). seq(1, 7, "T").

% F2: GCCATT
seq(2, 0, "G"). seq(2, 1, "C"). seq(2, 2, "C"). seq(2, 3, "A").
seq(2, 4, "T"). seq(2, 5, "T").

% F3: ATTTAA
seq(3, 0, "A"). seq(3, 1, "T"). seq(3, 2, "T"). seq(3, 3, "T").
seq(3, 4, "A"). seq(3, 5, "A").

% F4: ATGCCTCG
seq(4, 0, "A"). seq(4, 1, "T"). seq(4, 2, "G"). seq(4, 3, "C").
seq(4, 4, "C"). seq(4, 5, "T"). seq(4, 6, "C"). seq(4, 7, "G").

% F5: GCTCGAGG
seq(5, 0, "G"). seq(5, 1, "C"). seq(5, 2, "T"). seq(5, 3, "C").
seq(5, 4, "G"). seq(5, 5, "A"). seq(5, 6, "G"). seq(5, 7, "G").

% F6: TCGAGCTG
seq(6, 0, "T"). seq(6, 1, "C"). seq(6, 2, "G"). seq(6, 3, "A").
seq(6, 4, "G"). seq(6, 5, "C"). seq(6, 6, "T"). seq(6, 7, "G").

% F7: AGCTGA
seq(7, 0, "A"). seq(7, 1, "G"). seq(7, 2, "C"). seq(7, 3, "T").
seq(7, 4, "G"). seq(7, 5, "A").

% F8: ATTCG
seq(8, 0, "A"). seq(8, 1, "T"). seq(8, 2, "T"). seq(8, 3, "C").
seq(8, 4, "G").

% Fragment length
length(F, L) :- fragment(F), L = #count{P : seq(F, P, _)}.

% Orientation choice: 0 = forward, 1 = reverse
{ orientation(F, 0), orientation(F, 1) } :- fragment(F).

% Complement base
complement("A", "T").
complement("T", "A").
complement("C", "G").
complement("G", "C").

% Get base at position P in fragment F with orientation O
% O=0: forward (original), O=1: reverse complement
base(F, P, O, B) :-
    fragment(F), orientation(F, O),
    length(F, L), P >= 0, P < L,
    O = 0, seq(F, P, B).
base(F, P, O, B) :-
    fragment(F), orientation(F, O),
    length(F, L), P >= 0, P < L,
    O = 1, seq(F, L-1-P, B0), complement(B0, B).

% GC content calculation
gc_content(F, Content) :-
    fragment(F),
    G_count = #count{P : base(F, P, 0, "G")},
    C_count = #count{P : base(F, P, 0, "C")},
    L = #count{P : seq(F, P, _)},
    Content = (G_count + C_count) * 100 / L.

% Overlap calculation between two fragments
% For each pair of fragments and orientations, compute maximum valid overlap
overlap(F1, F2, O1, O2, Overlap) :-
    fragment(F1), fragment(F2), F1 != F2,
    orientation(F1, O1), orientation(F2, O2),
    length(F1, L1), length(F2, L2),
    MaxOverlap = min(L1, L2),
    Overlap = 1..MaxOverlap,
    % Check if suffix of F1 matches prefix of F2
    suffix_match(F1, O1, F2, O2, Overlap).

% Check if suffix of F1 matches prefix of F2 for given overlap length
suffix_match(F1, O1, F2, O2, K) :-
    fragment(F1), fragment(F2),
    orientation(F1, O1), orientation(F2, O2),
    K > 0,
    base(F1, L1-1-P, O1, B1) = base(F2, P, O2, B2) : P = 0..K-1,
    length(F1, L1), length(F2, L2), K <= L1, K <= L2.

% Contig assignment
% Each fragment is either in exactly one contig or chimeric
contig(1..9). % Maximum possible contigs
{ in_contig(F, C) : contig(C) } 1 :- fragment(F), not chimeric(F).
chimeric(F) :- fragment(F), not in_contig(F, _).

% Position assignment within contig
% Each fragment in contig has exactly one position
{ position(F, C, P) : P = 0..8 } 1 :- in_contig(F, C).

% Ensure positions are unique within contig
:- in_contig(F1, C), in_contig(F2, C), F1 != F2,
   position(F1, C, P), position(F2, C, P).

% Overlap requirements for adjacent fragments
:- in_contig(F1, C), in_contig(F2, C), F1 != F2,
   position(F1, C, P1), position(F2, C, P2), P2 = P1 + 1,
   orientation(F1, O1), orientation(F2, O2),
   not overlap(F1, F2, O1, O2, Overlap),
   gc_content(F1, GC1), gc_content(F2, GC2),
   (GC1 > 50, GC2 > 50, Overlap < 4; 
    (GC1 <= 50; GC2 <= 50), Overlap < 3).

% Contig start must be ATG
% Check first fragment in contig
start_codon(C) :-
    contig(C),
    in_contig(F, C),
    position(F, C, 0),
    orientation(F, O),
    base(F, 0, O, "A"),
    base(F, 1, O, "T"),
    base(F, 2, O, "G").

% Contig end must be stop codon
stop_codon(C) :-
    contig(C),
    in_contig(F, C),
    position(F, C, P),
    length(F, L),
    orientation(F, O),
    base(F, L-3, O, "T"),
    base(F, L-2, O, "A"),
    base(F, L-1, O, "A").
stop_codon(C) :-
    contig(C),
    in_contig(F, C),
    position(F, C, P),
    length(F, L),
    orientation(F, O),
    base(F, L-3, O, "T"),
    base(F, L-2, O, "A"),
    base(F, L-1, O, "G").
stop_codon(C) :-
    contig(C),
    in_contig(F, C),
    position(F, C, P),
    length(F, L),
    orientation(F, O),
    base(F, L-3, O, "T"),
    base(F, L-2, O, "G"),
    base(F, L-1, O, "A").

% Each contig must have start and stop codons
:- contig(C), in_contig(F, C), not start_codon(C).
:- contig(C), in_contig(F, C), not stop_codon(C).

% Minimize number of contigs
#minimize { 1, C : contig(C), in_contig(_, C) }.

% Show results
#show fragment/1.
#show orientation/2.
#show in_contig/2.
#show position/3.
#show chimeric/1.
#show contig/1.
#show start_codon/1.
#show stop_codon/1.