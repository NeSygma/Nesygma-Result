% DNA Fragment Assembly Problem - Simplified

% ===== 1. FRAGMENT DATA =====
fragment(0). fragment(1). fragment(2). fragment(3).
fragment(4). fragment(5). fragment(6). fragment(7).

% Fragment sequences as strings
fragment_seq(0, "ATCGATCG").
fragment_seq(1, "CGATCGTA").
fragment_seq(2, "ATCGTAAC").
fragment_seq(3, "CGTAACGG").
fragment_seq(4, "TAACGGCT").
fragment_seq(5, "ACGGCTGA").
fragment_seq(6, "GGCTGAAA").
fragment_seq(7, "CTGAAATC").

% ===== 2. POSITION DOMAIN =====
position(0..7).

% ===== 3. ASSIGN FRAGMENTS TO POSITIONS =====
% Each fragment appears exactly once
1 { pos(F, P) : position(P) } 1 :- fragment(F).

% Each position has exactly one fragment
1 { pos(F, P) : fragment(F) } 1 :- position(P).

% ===== 4. ADJACENT POSITIONS =====
adjacent(P, P+1) :- position(P), P < 7.

% ===== 5. PRECOMPUTED OVERLAPS =====
% Overlap(F1, F2, Length, Pos1) means F1's suffix starting at Pos1
% matches F2's prefix of given Length

% Fragment 0: ATCGATCG
% Fragment 1: CGATCGTA - overlap: CGATCG (6 chars, pos 2 in F0)
overlap(0, 1, 6, 2).
% Fragment 2: ATCGTAAC - overlap: ATCG (4 chars, pos 0 in F0)
overlap(0, 2, 4, 0).

% Fragment 1: CGATCGTA
% Fragment 2: ATCGTAAC - overlap: CGTA (4 chars, pos 4 in F1)
overlap(1, 2, 4, 4).
% Fragment 3: CGTAACGG - overlap: CGTAAC (6 chars, pos 2 in F1)
overlap(1, 3, 6, 2).

% Fragment 2: ATCGTAAC
% Fragment 3: CGTAACGG - overlap: TAAC (4 chars, pos 4 in F2)
overlap(2, 3, 4, 4).
% Fragment 4: TAACGGCT - overlap: TAACGG (6 chars, pos 2 in F2)
overlap(2, 4, 6, 2).

% Fragment 3: CGTAACGG
% Fragment 4: TAACGGCT - overlap: TAACGG (6 chars, pos 2 in F3)
overlap(3, 4, 6, 2).
% Fragment 5: ACGGCTGA - overlap: ACGG (4 chars, pos 0 in F3)
overlap(3, 5, 4, 0).

% Fragment 4: TAACGGCT
% Fragment 5: ACGGCTGA - overlap: ACGGCT (6 chars, pos 2 in F4)
overlap(4, 5, 6, 2).
% Fragment 6: GGCTGAAA - overlap: GGCT (4 chars, pos 4 in F4)
overlap(4, 6, 4, 4).

% Fragment 5: ACGGCTGA
% Fragment 6: GGCTGAAA - overlap: GGCTGA (6 chars, pos 2 in F5)
overlap(5, 6, 6, 2).
% Fragment 7: CTGAAATC - overlap: CTGA (4 chars, pos 4 in F5)
overlap(5, 7, 4, 4).

% Fragment 6: GGCTGAAA
% Fragment 7: CTGAAATC - overlap: CTGAAA (6 chars, pos 2 in F6)
overlap(6, 7, 6, 2).

% ===== 6. VALID OVERLAP CONSTRAINT =====
% Adjacent fragments must have a valid overlap
:- pos(F1, P1), pos(F2, P2), adjacent(P1, P2),
   not overlap(F1, F2, L, _).

% ===== 7. TOTAL OVERLAP CALCULATION =====
% Sum of overlap lengths for adjacent pairs
total_overlap(Total) :-
    Total = #sum{L, F1, F2 : pos(F1, P1), pos(F2, P2), adjacent(P1, P2), overlap(F1, F2, L, _)}.

% ===== 8. OPTIMIZATION =====
#maximize { Total : total_overlap(Total) }.

% ===== 9. OUTPUT =====
solution_exists.

% Assembly path: fragment at each position
assembly_path(P, F) :- pos(F, P).

% Overlap details for each adjacent pair
overlap_details(F1, F2, L, Pos1, 0) :-
    pos(F1, P1), pos(F2, P2), adjacent(P1, P2),
    overlap(F1, F2, L, Pos1).

% ===== SHOW DIRECTIVES =====
#show solution_exists/0.
#show assembly_path/2.
#show overlap_details/5.
#show total_overlap/1.
#show pos/2.