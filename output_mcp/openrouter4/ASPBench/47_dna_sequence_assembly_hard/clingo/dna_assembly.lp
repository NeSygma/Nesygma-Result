% DNA Fragment Assembly Problem

% --- Fragment definitions ---
fragment(0..8).
orient(forward; reverse).

% Complement mapping
comp(a, t). comp(t, a). comp(c, g). comp(g, c).

% Forward sequences
base(0, forward, 0, a). base(0, forward, 1, t). base(0, forward, 2, g).
base(0, forward, 3, g). base(0, forward, 4, g). base(0, forward, 5, c).
base(0, forward, 6, g). base(0, forward, 7, c).

base(1, forward, 0, g). base(1, forward, 1, g). base(1, forward, 2, c).
base(1, forward, 3, g). base(1, forward, 4, c). base(1, forward, 5, c).
base(1, forward, 6, a). base(1, forward, 7, t).

base(2, forward, 0, g). base(2, forward, 1, c). base(2, forward, 2, c).
base(2, forward, 3, a). base(2, forward, 4, t). base(2, forward, 5, t).

base(3, forward, 0, a). base(3, forward, 1, t). base(3, forward, 2, t).
base(3, forward, 3, t). base(3, forward, 4, a). base(3, forward, 5, a).

base(4, forward, 0, a). base(4, forward, 1, t). base(4, forward, 2, g).
base(4, forward, 3, c). base(4, forward, 4, c). base(4, forward, 5, t).
base(4, forward, 6, c). base(4, forward, 7, g).

base(5, forward, 0, g). base(5, forward, 1, c). base(5, forward, 2, t).
base(5, forward, 3, c). base(5, forward, 4, g). base(5, forward, 5, a).
base(5, forward, 6, g). base(5, forward, 7, g).

base(6, forward, 0, t). base(6, forward, 1, c). base(6, forward, 2, g).
base(6, forward, 3, a). base(6, forward, 4, g). base(6, forward, 5, c).
base(6, forward, 6, t). base(6, forward, 7, g).

base(7, forward, 0, a). base(7, forward, 1, g). base(7, forward, 2, c).
base(7, forward, 3, t). base(7, forward, 4, g). base(7, forward, 5, a).

base(8, forward, 0, a). base(8, forward, 1, t). base(8, forward, 2, t).
base(8, forward, 3, c). base(8, forward, 4, g).

% Length for each fragment
len(F, L) :- L = #count{P : base(F, forward, P, _)}, fragment(F).

% Reverse complement: position P in reverse = position (L-1-Pf) in forward, complemented
base(F, reverse, P, Bc) :-
    fragment(F), base(F, forward, Pf, B), comp(B, Bc),
    len(F, L), P = L - 1 - Pf.

% All orientations
all_orient(forward; reverse).

% --- GC-content ---
gc_cnt(F, O, N) :-
    fragment(F), all_orient(O),
    N = #count{P : base(F, O, P, g); P : base(F, O, P, c)}.

gc50(F, O) :-
    fragment(F), all_orient(O),
    gc_cnt(F, O, N), len(F, L), N * 2 > L.

% --- Overlap rules ---
% Possible overlap lengths (1..8)
k(1..8).

% Minimum required overlap
min_ovl(F1, O1, F2, O2, 4) :-
    fragment(F1), fragment(F2), F1 != F2, all_orient(O1), all_orient(O2),
    gc50(F1, O1), gc50(F2, O2).

min_ovl(F1, O1, F2, O2, 3) :-
    fragment(F1), fragment(F2), F1 != F2, all_orient(O1), all_orient(O2),
    not gc50(F1, O1), not gc50(F2, O2).

min_ovl(F1, O1, F2, O2, 3) :-
    fragment(F1), fragment(F2), F1 != F2, all_orient(O1), all_orient(O2),
    gc50(F1, O1), not gc50(F2, O2).

min_ovl(F1, O1, F2, O2, 3) :-
    fragment(F1), fragment(F2), F1 != F2, all_orient(O1), all_orient(O2),
    not gc50(F1, O1), gc50(F2, O2).

% Check mismatch between F1[O1] and F2[O2] at overlap K
% Base at P1 of F1 aligns with base at P2 of F2 if P1 = L1 - K + P2
mism(F1, O1, F2, O2, K) :-
    base(F1, O1, P1, B1), base(F2, O2, P2, B2),
    len(F1, L1), k(K), K <= L1,
    K > P2,
    P1 = L1 - K + P2,
    B1 != B2.

% Valid overlap: no mismatch, within lengths
valid_ovl(F1, O1, F2, O2, K) :-
    fragment(F1), fragment(F2), F1 != F2, all_orient(O1), all_orient(O2),
    len(F1, L1), len(F2, L2), k(K), K <= L1, K <= L2,
    not mism(F1, O1, F2, O2, K).

% Adjacent condition: valid overlap with min requirement
adj(F1, O1, F2, O2) :-
    valid_ovl(F1, O1, F2, O2, K),
    min_ovl(F1, O1, F2, O2, M),
    K >= M.

% --- Start and stop codons ---
start_codon(F, O) :-
    base(F, O, 0, a), base(F, O, 1, t), base(F, O, 2, g).

stop_codon(F, O) :-
    len(F, L), L >= 3,
    base(F, O, L-3, t), base(F, O, L-2, a), base(F, O, L-1, a).

stop_codon(F, O) :-
    len(F, L), L >= 3,
    base(F, O, L-3, t), base(F, O, L-2, a), base(F, O, L-1, g).

stop_codon(F, O) :-
    len(F, L), L >= 3,
    base(F, O, L-3, t), base(F, O, L-2, g), base(F, O, L-1, a).

% --- Assembly modeling ---
contig(0..4).
pos_val(0..8).

% Each fragment is in exactly one contig or chimeric
{ in_ctg(F, C) : contig(C) } 1 :- fragment(F).
chimeric(F) :- fragment(F), not in_ctg(F, _).

% Each used fragment gets orientation
{ orient(F, O, C) : all_orient(O) } 1 :- in_ctg(F, C).

% Each used fragment gets a position in its contig
{ pos(F, C, P) : pos_val(P) } 1 :- in_ctg(F, C).

% No two fragments share same position in same contig
:- pos(F1, C, P), pos(F2, C, P), F1 != F2.

% Positions in a contig must be consecutive from 0
used_ctg(C) :- pos(_, C, _).
hp(C, P) :- pos(_, C, P).
:- used_ctg(C), hp(C, P1), hp(C, P2), P2 > P1 + 1, not hp(C, P1 + 1).

% First fragment of contig must start with ATG
:- pos(F, C, 0), orient(F, O, C), not start_codon(F, O).

% Last fragment of contig must end with stop codon
mxpos(C, P) :- P = #max{ P2 : pos(_, C, P2) }, contig(C), used_ctg(C).
:- pos(F, C, P), orient(F, O, C), mxpos(C, P), not stop_codon(F, O).

% Adjacent fragments must have valid overlap
:- pos(F1, C, P1), orient(F1, O1, C),
   pos(F2, C, P2), orient(F2, O2, C),
   P2 = P1 + 1,
   not adj(F1, O1, F2, O2).

% Minimize number of contigs used
used(C) :- in_ctg(_, C).
#minimize { 1@1, C : used(C) }.

% --- Output ---
#show in_ctg/2.
#show orient/3.
#show pos/3.
#show chimeric/1.