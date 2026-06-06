%% DNA Fragment Assembly Problem
%% Find ordering that maximizes total overlap length

%% Fragment data
fragment(0, "ATCGATCG").
fragment(1, "CGATCGTA").
fragment(2, "ATCGTAAC").
fragment(3, "CGTAACGG").
fragment(4, "TAACGGCT").
fragment(5, "ACGGCTGA").
fragment(6, "GGCTGAAA").
fragment(7, "CTGAAATC").

%% Fragment indices
frag_idx(0..7).

%% Positions within fragments (0-indexed)
pos(0..7).

%% Define nucleotide at each position for each fragment using facts
%% Fragment 0: ATCGATCG
nucleotide(0,0,a). nucleotide(0,1,t). nucleotide(0,2,c). nucleotide(0,3,g).
nucleotide(0,4,a). nucleotide(0,5,t). nucleotide(0,6,c). nucleotide(0,7,g).

%% Fragment 1: CGATCGTA
nucleotide(1,0,c). nucleotide(1,1,g). nucleotide(1,2,a). nucleotide(1,3,t).
nucleotide(1,4,c). nucleotide(1,5,g). nucleotide(1,6,t). nucleotide(1,7,a).

%% Fragment 2: ATCGTAAC
nucleotide(2,0,a). nucleotide(2,1,t). nucleotide(2,2,c). nucleotide(2,3,g).
nucleotide(2,4,t). nucleotide(2,5,a). nucleotide(2,6,a). nucleotide(2,7,c).

%% Fragment 3: CGTAACGG
nucleotide(3,0,c). nucleotide(3,1,g). nucleotide(3,2,t). nucleotide(3,3,a).
nucleotide(3,4,a). nucleotide(3,5,c). nucleotide(3,6,g). nucleotide(3,7,g).

%% Fragment 4: TAACGGCT
nucleotide(4,0,t). nucleotide(4,1,a). nucleotide(4,2,a). nucleotide(4,3,c).
nucleotide(4,4,g). nucleotide(4,5,g). nucleotide(4,6,c). nucleotide(4,7,t).

%% Fragment 5: ACGGCTGA
nucleotide(5,0,a). nucleotide(5,1,c). nucleotide(5,2,g). nucleotide(5,3,g).
nucleotide(5,4,c). nucleotide(5,5,t). nucleotide(5,6,g). nucleotide(5,7,a).

%% Fragment 6: GGCTGAAA
nucleotide(6,0,g). nucleotide(6,1,g). nucleotide(6,2,c). nucleotide(6,3,t).
nucleotide(6,4,g). nucleotide(6,5,a). nucleotide(6,6,a). nucleotide(6,7,a).

%% Fragment 7: CTGAAATC
nucleotide(7,0,c). nucleotide(7,1,t). nucleotide(7,2,g). nucleotide(7,3,a).
nucleotide(7,4,a). nucleotide(7,5,a). nucleotide(7,6,t). nucleotide(7,7,c).

%% Overlap: fragment I can precede fragment J with overlap length L
%% Suffix of I of length L matches prefix of J of length L
%% Minimum overlap is 3
possible_overlap(I, J, L) :- frag_idx(I), frag_idx(J), I != J,
    L = #count{ P : pos(P), P < 8, P >= 8-L, 
                nucleotide(I, P, N1), 
                nucleotide(J, P-(8-L), N2), N1 = N2 },
    L >= 3,
    L <= 8.

%% Each fragment appears exactly once in the ordering
{ order(Pos, F) : frag_idx(F) } 1 :- pos(Pos).
:- frag_idx(F), not { order(Pos, F) : pos(Pos) } 1.

%% Adjacent pairs: positions P and P+1
adjacent(P, P+1) :- pos(P), P < 7.

%% If two fragments are adjacent, they must have a valid overlap
overlap_used(I, J, L) :- adjacent(P1, P2), order(P1, I), order(P2, J), possible_overlap(I, J, L).

%% Each adjacent pair must use exactly one overlap length
:- adjacent(P1, P2), order(P1, I), order(P2, J), 
    not possible_overlap(I, J, _).

%% Total overlap sum
total_overlap(S) :- S = #sum{ L, I, J : overlap_used(I, J, L) }.

%% Maximize total overlap
#maximize { L@1, I, J : overlap_used(I, J, L) }.

%% Show results
#show order/2.
#show overlap_used/3.
#show total_overlap/1.