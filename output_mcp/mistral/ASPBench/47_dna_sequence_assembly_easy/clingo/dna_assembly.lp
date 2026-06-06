% Define the DNA fragments
fragment(0,"ATCGATCG").
fragment(1,"CGATCGTA").
fragment(2,"ATCGTAAC").
fragment(3,"CGTAACGG").
fragment(4,"TAACGGCT").
fragment(5,"ACGGCTGA").
fragment(6,"GGCTGAAA").
fragment(7,"CTGAAATC").

% Precomputed overlaps (fragment1, fragment2, overlap_length):
% Overlaps are computed as the maximum length where suffix of F1 matches prefix of F2
% Only overlaps >= 3 are considered valid for adjacency

% Overlap facts: overlap(F1, F2, L) means F1's suffix of length L matches F2's prefix of length L

% Overlaps for fragment 0
% Fragment 0: ATCGATCG
% Fragment 1: CGATCGTA -> suffix(0,6) = TCGATC, prefix(1,6) = CGATCG -> match: CGATCG (6)
overlap(0,1,6).
% Fragment 2: ATCGTAAC -> suffix(0,4) = TCGA, prefix(2,4) = ATCG -> match: ATCG (4)
overlap(0,2,4).
% Fragment 3: CGTAACGG -> suffix(0,2) = TC, prefix(3,2) = CG -> no match >=3
overlap(0,3,2).
% Fragment 4: TAACGGCT -> suffix(0,1) = C, prefix(4,1) = T -> no match >=3
overlap(0,4,1).
% Fragments 5-7: no overlap >=3
overlap(0,5,0).
overlap(0,6,0).
overlap(0,7,0).

% Overlaps for fragment 1
% Fragment 1: CGATCGTA
% Fragment 0: ATCGATCG -> prefix(0,6) = ATCGAT, suffix(1,6) = GATCGT -> no match >=3
overlap(1,0,0).
% Fragment 2: ATCGTAAC -> prefix(2,2) = AT, suffix(1,2) = TA -> no match >=3
overlap(1,2,2).
% Fragment 3: CGTAACGG -> prefix(3,4) = CGTA, suffix(1,4) = TCGT -> no match >=3
overlap(1,3,4).
% Fragment 4: TAACGGCT -> prefix(4,1) = T, suffix(1,1) = A -> no match >=3
overlap(1,4,1).
% Fragments 5-7: no overlap >=3
overlap(1,5,0).
overlap(1,6,0).
overlap(1,7,0).

% Overlaps for fragment 2
% Fragment 2: ATCGTAAC
% Fragment 0: ATCGATCG -> prefix(0,3) = ATC, suffix(2,3) = TAA -> no match >=3
overlap(2,0,3).
% Fragment 1: CGATCGTA -> prefix(1,4) = CGAT, suffix(2,4) = CGTA -> match: CGTA (4)
overlap(2,1,4).
% Fragment 3: CGTAACGG -> prefix(3,6) = CGTAAC, suffix(2,6) = TCGTAA -> no match >=3
overlap(2,3,6).
% Fragment 4: TAACGGCT -> prefix(4,5) = TAACG, suffix(2,5) = CGTAA -> no match >=3
overlap(2,4,5).
% Fragment 5: ACGGCTGA -> prefix(5,2) = AC, suffix(2,2) = AA -> no match >=3
overlap(2,5,2).
% Fragments 6-7: no overlap >=3
overlap(2,6,0).
overlap(2,7,0).

% Overlaps for fragment 3
% Fragment 3: CGTAACGG
% Fragment 0: ATCGATCG -> prefix(0,0) = (empty), suffix(3,0) = (empty) -> no match >=3
overlap(3,0,0).
% Fragment 1: CGATCGTA -> prefix(1,3) = CGA, suffix(3,3) = AAC -> no match >=3
overlap(3,1,3).
% Fragment 2: ATCGTAAC -> prefix(2,2) = AT, suffix(3,2) = CG -> no match >=3
overlap(3,2,2).
% Fragment 4: TAACGGCT -> prefix(4,6) = TAACGG, suffix(3,6) = TAACGG -> match: TAACGG (6)
overlap(3,4,6).
% Fragment 5: ACGGCTGA -> prefix(5,4) = ACGG, suffix(3,4) = AACG -> no match >=3
overlap(3,5,4).
% Fragment 6: GGCTGAAA -> prefix(6,2) = GG, suffix(3,2) = CG -> no match >=3
overlap(3,6,2).
% Fragment 7: CTGAAATC -> prefix(7,0) = (empty), suffix(3,0) = (empty) -> no match >=3
overlap(3,7,0).

% Overlaps for fragment 4
% Fragment 4: TAACGGCT
% Fragment 0: ATCGATCG -> prefix(0,0) = (empty), suffix(4,0) = (empty) -> no match >=3
overlap(4,0,0).
% Fragment 1: CGATCGTA -> prefix(1,0) = (empty), suffix(4,0) = (empty) -> no match >=3
overlap(4,1,0).
% Fragment 2: ATCGTAAC -> prefix(2,3) = ATC, suffix(4,3) = GGC -> no match >=3
overlap(4,2,3).
% Fragment 3: CGTAACGG -> prefix(3,5) = CGTAA, suffix(4,5) = CGGCT -> no match >=3
overlap(4,3,5).
% Fragment 5: ACGGCTGA -> prefix(5,6) = ACGGCT, suffix(4,6) = AACGGC -> no match >=3
overlap(4,5,6).
% Fragment 6: GGCTGAAA -> prefix(6,4) = GGCT, suffix(4,4) = GGCT -> match: GGCT (4)
overlap(4,6,4).
% Fragment 7: CTGAAATC -> prefix(7,2) = CT, suffix(4,2) = GC -> no match >=3
overlap(4,7,2).

% Overlaps for fragment 5
% Fragment 5: ACGGCTGA
% Fragment 0: ATCGATCG -> prefix(0,0) = (empty), suffix(5,0) = (empty) -> no match >=3
overlap(5,0,0).
% Fragment 1: CGATCGTA -> prefix(1,0) = (empty), suffix(5,0) = (empty) -> no match >=3
overlap(5,1,0).
% Fragment 2: ATCGTAAC -> prefix(2,0) = (empty), suffix(5,0) = (empty) -> no match >=3
overlap(5,2,0).
% Fragment 3: CGTAACGG -> prefix(3,3) = CGT, suffix(5,3) = GCT -> no match >=3
overlap(5,3,3).
% Fragment 4: TAACGGCT -> prefix(4,4) = TAAC, suffix(5,4) = GCTG -> no match >=3
overlap(5,4,4).
% Fragment 6: GGCTGAAA -> prefix(6,6) = GGCTGA, suffix(5,6) = CGTGAA -> no match >=3
overlap(5,6,6).
% Fragment 7: CTGAAATC -> prefix(7,3) = CTG, suffix(5,3) = CTG -> match: CTG (3)
overlap(5,7,3).

% Overlaps for fragment 6
% Fragment 6: GGCTGAAA
% Fragment 0: ATCGATCG -> prefix(0,0) = (empty), suffix(6,0) = (empty) -> no match >=3
overlap(6,0,0).
% Fragment 1: CGATCGTA -> prefix(1,0) = (empty), suffix(6,0) = (empty) -> no match >=3
overlap(6,1,0).
% Fragment 2: ATCGTAAC -> prefix(2,0) = (empty), suffix(6,0) = (empty) -> no match >=3
overlap(6,2,0).
% Fragment 3: CGTAACGG -> prefix(3,2) = CG, suffix(6,2) = AA -> no match >=3
overlap(6,3,2).
% Fragment 4: TAACGGCT -> prefix(4,4) = TAAC, suffix(6,4) = TGAA -> no match >=3
overlap(6,4,4).
% Fragment 5: ACGGCTGA -> prefix(5,5) = ACGGC, suffix(6,5) = CTGAA -> no match >=3
overlap(6,5,5).
% Fragment 7: CTGAAATC -> prefix(7,6) = CTGAAA, suffix(6,6) = GGCTGA -> no match >=3
overlap(6,7,6).

% Overlaps for fragment 7
% Fragment 7: CTGAAATC
% Fragment 0: ATCGATCG -> prefix(0,1) = A, suffix(7,1) = C -> no match >=3
overlap(7,0,1).
% Fragment 1: CGATCGTA -> prefix(1,2) = CG, suffix(7,2) = AA -> no match >=3
overlap(7,1,2).
% Fragment 2: ATCGTAAC -> prefix(2,3) = ATC, suffix(7,3) = AAA -> no match >=3
overlap(7,2,3).
% Fragment 3: CGTAACGG -> prefix(3,4) = CGTA, suffix(7,4) = AAAT -> no match >=3
overlap(7,3,4).
% Fragment 4: TAACGGCT -> prefix(4,5) = TAACG, suffix(7,5) = TGAAA -> no match >=3
overlap(7,4,5).
% Fragment 5: ACGGCTGA -> prefix(5,6) = ACGGCT, suffix(7,6) = TGAAAT -> no match >=3
overlap(7,5,6).
% Fragment 6: GGCTGAAA -> prefix(6,3) = GGC, suffix(7,3) = GAA -> no match >=3
overlap(7,6,3).

% Define the assembly as a permutation using next/2
% Each fragment (except the last) has exactly one successor
{ next(F1, F2) : fragment(F2, _) } = 1 :- fragment(F1, _).

% Each fragment (except the first) has exactly one predecessor
{ next(F1, F2) : fragment(F1, _) } = 1 :- fragment(F2, _).

% Ensure the assembly is a single linear sequence (no cycles)
:- next(F1, F2), next(F2, F1).

% Calculate overlap for each adjacent pair
adj_overlap(F1, F2, L) :- next(F1, F2), overlap(F1, F2, L), L >= 3.

% Ensure all adjacent pairs have a valid overlap of at least 3
:- next(F1, F2), not adj_overlap(F1, F2, _).

% Total overlap is the sum of all adjacent overlaps
total_overlap(L) :- L = #sum { L2 : adj_overlap(_, _, L2) }.

% Maximize the total overlap
#maximize { L : total_overlap(L) }.

% Show the assembly path and total overlap
#show next/2.
#show total_overlap/1.