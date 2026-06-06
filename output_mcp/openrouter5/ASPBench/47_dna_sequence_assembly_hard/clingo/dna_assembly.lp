%% DNA Fragment Assembly Problem
%% ================================

%% Fragment data: fragment(ID, Sequence as list of chars)
frag_chars(0, a,t,g,g,g,c,g,c).
frag_chars(1, g,g,c,g,c,c,a,t).
frag_chars(2, g,c,c,a,t,t).
frag_chars(3, a,t,t,t,a,a).
frag_chars(4, a,t,g,c,c,t,c,g).
frag_chars(5, g,c,t,c,g,a,g,g).
frag_chars(6, t,c,g,a,g,c,t,g).
frag_chars(7, a,g,c,t,g,a).
frag_chars(8, a,t,t,c,g).

%% Length of each fragment
frag_len(0,8).
frag_len(1,8).
frag_len(2,6).
frag_len(3,6).
frag_len(4,8).
frag_len(5,8).
frag_len(6,8).
frag_len(7,6).
frag_len(8,5).

%% All fragment IDs
frag_id(0..8).

%% Character at position (0-indexed) in a fragment
char_at(F,0,C0) :- frag_chars(F, C0,_,_,_,_,_,_,_).
char_at(F,1,C1) :- frag_chars(F, _,C1,_,_,_,_,_,_).
char_at(F,2,C2) :- frag_chars(F, _,_,C2,_,_,_,_,_).
char_at(F,3,C3) :- frag_chars(F, _,_,_,C3,_,_,_,_).
char_at(F,4,C4) :- frag_chars(F, _,_,_,_,C4,_,_,_).
char_at(F,5,C5) :- frag_chars(F, _,_,_,_,_,C5,_,_).
char_at(F,6,C6) :- frag_chars(F, _,_,_,_,_,_,C6,_).
char_at(F,7,C7) :- frag_chars(F, _,_,_,_,_,_,_,C7).

%% Complement mapping
complement(a,t).
complement(t,a).
complement(c,g).
complement(g,c).

%% Reverse-complement: char_at_rc(F, P, C) means at position P (from start of original),
%% the reverse-complement has base C.
char_at_rc(F, P, C) :- frag_id(F), frag_len(F, L), P < L, 
                        RP = L - 1 - P,
                        char_at(F, RP, B),
                        complement(B, C).

%% ================================
%% Domain: contigs
%% ================================

%% Maximum number of contigs to consider
max_contigs(5).
contig_id(1..M) :- max_contigs(M).

%% ================================
%% Choice: fragment usage and orientation
%% ================================

%% Each fragment is either used in a contig (at some position) or chimeric
{ used(F, C, Pos) : contig_id(C), Pos = 0..8 } 1 :- frag_id(F).

%% Each fragment can be used at most once
:- used(F, C1, P1), used(F, C2, P2), (C1, P1) != (C2, P2).

%% Orientation: forward (0) or reverse (1)
{ orientation(F, 0) } :- used(F, _, _).
{ orientation(F, 1) } :- used(F, _, _).
:- used(F, _, _), not orientation(F, 0), not orientation(F, 1).
:- orientation(F, 0), orientation(F, 1).

%% Chimeric fragments
chimeric(F) :- frag_id(F), not used(F, _, _).

%% ================================
%% Contig ordering constraints
%% ================================

%% At most one fragment per position per contig
:- used(F1, C, Pos), used(F2, C, Pos), F1 != F2.

%% Positions must be consecutive (no gaps)
:- contig_id(C), used(F1, C, P1), used(F2, C, P2), P1 < P2, 
   P2 - P1 > 1, not used(_, C, P1+1).

%% ================================
%% GC-content computation
%% ================================

%% Count G and C bases in a fragment
gc_count(F, N) :- frag_id(F), frag_len(F, L), 
                   N = #count{P : char_at(F, P, c); P : char_at(F, P, g)}.

high_gc(F) :- frag_id(F), frag_len(F, L), gc_count(F, N), L > 0, N * 2 > L.

%% Minimum overlap required between adjacent fragments in a contig
min_overlap(F1, F2, 4) :- frag_id(F1), frag_id(F2), high_gc(F1), high_gc(F2).
min_overlap(F1, F2, 3) :- frag_id(F1), frag_id(F2), not high_gc(F1), not high_gc(F2).

%% ================================
%% Base at position in chosen orientation
%% ================================

base_at(F, P, B) :- orientation(F, 0), char_at(F, P, B).
base_at(F, P, B) :- orientation(F, 1), char_at_rc(F, P, B).

frag_len_used(F, L) :- orientation(F, 0), frag_len(F, L).
frag_len_used(F, L) :- orientation(F, 1), frag_len(F, L).

%% ================================
%% Overlap validation
%% ================================

%% Check if overlap of length K works between F1 (first) and F2 (second)
overlap_match(F1, F2, K) :- frag_id(F1), frag_id(F2),
                             frag_len_used(F1, L1), frag_len_used(F2, L2),
                             K = 1..L1, K = 1..L2,
                             #count{I : I = 0..K-1, 
                                    base_at(F1, L1-K+I, B1), 
                                    base_at(F2, I, B2), 
                                    B1 = B2} = K.

valid_overlap(F1, F2, K) :- used(F1, C, P), used(F2, C, P+1),
                             frag_len_used(F1, L1), frag_len_used(F2, L2),
                             K = 1..L1, K = 1..L2,
                             min_overlap(F1, F2, MinK), K >= MinK,
                             overlap_match(F1, F2, K).

%% At least one valid overlap must exist between adjacent fragments
:- used(F1, C, P), used(F2, C, P+1), not valid_overlap(F1, F2, _).

%% ================================
%% Start codon: each contig must start with ATG
%% ================================

%% Forward: first 3 bases are a,t,g
starts_with_atg(F) :- orientation(F, 0), 
                       char_at(F, 0, a), char_at(F, 1, t), char_at(F, 2, g).

%% Reverse: RC of last 3 bases of original = ATG
%% So original's last 3 bases must be CAT (since RC(CAT)=ATG)
starts_with_atg_rc(F) :- orientation(F, 1), frag_len(F, L), L >= 3,
                          char_at(F, L-3, c), char_at(F, L-2, a), char_at(F, L-1, t).

starts_contig_with_atg(F) :- starts_with_atg(F).
starts_contig_with_atg(F) :- starts_with_atg_rc(F).

%% First fragment of each contig must start with ATG
:- used(F, C, 0), not starts_contig_with_atg(F).

%% ================================
%% Stop codon: each contig must end with a stop codon
%% ================================

%% Forward: last 3 bases are TAA, TAG, or TGA
ends_with_stop(F) :- orientation(F, 0), frag_len(F, L), L >= 3,
                      char_at(F, L-3, t), char_at(F, L-2, a), char_at(F, L-1, a).
ends_with_stop(F) :- orientation(F, 0), frag_len(F, L), L >= 3,
                      char_at(F, L-3, t), char_at(F, L-2, a), char_at(F, L-1, g).
ends_with_stop(F) :- orientation(F, 0), frag_len(F, L), L >= 3,
                      char_at(F, L-3, t), char_at(F, L-2, g), char_at(F, L-1, a).

%% Reverse: RC of first 3 bases of original = stop codon
%% So original's first 3 bases = RC(stop codon)
%% RC(TAA)=TTA, RC(TAG)=CTA, RC(TGA)=TCA
ends_with_stop_rc(F) :- orientation(F, 1), 
                         char_at(F, 0, t), char_at(F, 1, t), char_at(F, 2, a).
ends_with_stop_rc(F) :- orientation(F, 1), 
                         char_at(F, 0, c), char_at(F, 1, t), char_at(F, 2, a).
ends_with_stop_rc(F) :- orientation(F, 1), 
                         char_at(F, 0, t), char_at(F, 1, c), char_at(F, 2, a).

ends_contig_with_stop(F) :- ends_with_stop(F).
ends_contig_with_stop(F) :- ends_with_stop_rc(F).

%% Last fragment of each contig must end with a stop codon
last_pos(C, MaxPos) :- contig_id(C), MaxPos = #max{P : used(_, C, P)}.
:- used(F, C, P), last_pos(C, P), not ends_contig_with_stop(F).

%% ================================
%% Minimize number of contigs
%% ================================

used_contig(C) :- used(_, C, _).
num_contigs(N) :- N = #count{C : used_contig(C)}.

#minimize { N : num_contigs(N) }.

%% ================================
%% Output
%% ================================

#show used/3.
#show orientation/2.
#show chimeric/1.
#show num_contigs/1.