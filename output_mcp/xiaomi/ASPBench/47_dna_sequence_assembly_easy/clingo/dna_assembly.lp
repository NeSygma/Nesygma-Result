% DNA Fragment Assembly Problem
% Goal: Order fragments to maximize total overlap

% ============ FRAGMENT DATA ============
% Fragment sequences as facts
fragment(0, "ATCGATCG").
fragment(1, "CGATCGTA").
fragment(2, "ATCGTAAC").
fragment(3, "CGTAACGG").
fragment(4, "TAACGGCT").
fragment(5, "ACGGCTGA").
fragment(6, "GGCTGAAA").
fragment(7, "CTGAAATC").

% Fragment IDs
fid(0). fid(1). fid(2). fid(3). fid(4). fid(5). fid(6). fid(7).

% ============ NUCLEOTIDE POSITIONS ============
% Extract nucleotide at each position
% We'll use string indexing - position 0-based
% Fragment 0: ATCGATCG (length 8)
pos(0,0,"A"). pos(0,1,"T"). pos(0,2,"C"). pos(0,3,"G").
pos(0,4,"A"). pos(0,5,"T"). pos(0,6,"C"). pos(0,7,"G").

% Fragment 1: CGATCGTA (length 8)
pos(1,0,"C"). pos(1,1,"G"). pos(1,2,"A"). pos(1,3,"T").
pos(1,4,"C"). pos(1,5,"G"). pos(1,6,"T"). pos(1,7,"A").

% Fragment 2: ATCGTAAC (length 8)
pos(2,0,"A"). pos(2,1,"T"). pos(2,2,"C"). pos(2,3,"G").
pos(2,4,"T"). pos(2,5,"A"). pos(2,6,"A"). pos(2,7,"C").

% Fragment 3: CGTAACGG (length 8)
pos(3,0,"C"). pos(3,1,"G"). pos(3,2,"T"). pos(3,3,"A").
pos(3,4,"A"). pos(3,5,"C"). pos(3,6,"G"). pos(3,7,"G").

% Fragment 4: TAACGGCT (length 8)
pos(4,0,"T"). pos(4,1,"A"). pos(4,2,"A"). pos(4,3,"C").
pos(4,4,"G"). pos(4,5,"G"). pos(4,6,"C"). pos(4,7,"T").

% Fragment 5: ACGGCTGA (length 8)
pos(5,0,"A"). pos(5,1,"C"). pos(5,2,"G"). pos(5,3,"G").
pos(5,4,"C"). pos(5,5,"T"). pos(5,6,"G"). pos(5,7,"A").

% Fragment 6: GGCTGAAA (length 8)
pos(6,0,"G"). pos(6,1,"G"). pos(6,2,"C"). pos(6,3,"T").
pos(6,4,"G"). pos(6,5,"A"). pos(6,6,"A"). pos(6,7,"A").

% Fragment 7: CTGAAATC (length 8)
pos(7,0,"C"). pos(7,1,"T"). pos(7,2,"G"). pos(7,3,"A").
pos(7,4,"A"). pos(7,5,"A"). pos(7,6,"T"). pos(7,7,"C").

% All fragments have length 8
flen(8).

% ============ OVERLAP DETECTION ============
% Check if fragment F1 ending overlaps with fragment F2 beginning
% Overlap of length L means: last L chars of F1 = first L chars of F2
% i.e., pos(F1, 8-L+i, N) = pos(F2, i, N) for i in 0..L-1

% Overlap lengths to consider (3 to 7, since min overlap is 3)
olen(3). olen(4). olen(5). olen(6). olen(7).

% A valid overlap of length L between F1 and F2
valid_overlap(F1, F2, L) :- 
    fid(F1), fid(F2), F1 != F2, olen(L),
    flen(FL),
    #count{I : pos(F1, FL-L+I, N), pos(F2, I, N), I = 0..L-1} = L.

% Actually, let's use a different approach - check each position
% Overlap of length L is valid if all positions match
valid_overlap(F1, F2, L) :-
    fid(F1), fid(F2), F1 != F2, olen(L),
    flen(FL),
    not mismatch(F1, F2, L).

% There's a mismatch at some position
mismatch(F1, F2, L) :-
    fid(F1), fid(F2), F1 != F2, olen(L),
    flen(FL),
    I = 0..L-1,
    pos(F1, FL-L+I, N1), pos(F2, I, N2), N1 != N2.

% ============ ASSEMBLY STRUCTURE ============
% Choose which fragment is first
1 { first(F) : fid(F) } 1.

% Choose which fragment is last
1 { last(F) : fid(F) } 1.

% First and last must be different
:- first(F), last(F).

% Choose adjacency: each fragment (except last) has exactly one successor
1 { adjacent(F1, F2) : fid(F2) } 1 :- fid(F1), not last(F1).

% Each fragment (except first) has exactly one predecessor
1 { adjacent(F1, F2) : fid(F1) } 1 :- fid(F2), not first(F2).

% No self-loops
:- adjacent(F, F).

% ============ OVERLAP CONSTRAINTS ============
% Adjacent fragments must have valid overlap of at least 3
:- adjacent(F1, F2), not valid_overlap(F1, F2, _).

% Choose the overlap length for each adjacent pair
1 { overlap_len(F1, F2, L) : olen(L), valid_overlap(F1, F2, L) } 1 :- adjacent(F1, F2).

% ============ LINEARITY ============
% Ensure single linear chain (no cycles)
% Use reachability
reached(F) :- first(F).
reached(F2) :- reached(F1), adjacent(F1, F2).

% All fragments must be reached
:- fid(F), not reached(F).

% ============ OBJECTIVE ============
% Maximize total overlap
total_overlap(S) :- S = #sum{L, F1, F2 : overlap_len(F1, F2, L)}.

#maximize { L : overlap_len(F1, F2, L) }.

% ============ OUTPUT ============
#show first/1.
#show last/1.
#show adjacent/2.
#show overlap_len/3.
#show total_overlap/1.