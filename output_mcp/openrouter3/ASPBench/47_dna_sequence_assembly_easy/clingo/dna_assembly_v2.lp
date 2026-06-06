% DNA Fragment Assembly Problem
% Assemble overlapping DNA fragments to maximize total overlap

% ==================== DOMAIN DEFINITIONS ====================
% Fragment indices
fragment(0..7).

% DNA sequences for each fragment (as strings)
sequence(0, "ATCGATCG").
sequence(1, "CGATCGTA").
sequence(2, "ATCGTAAC").
sequence(3, "CGTAACGG").
sequence(4, "TAACGGCT").
sequence(5, "ACGGCTGA").
sequence(6, "GGCTGAAA").
sequence(7, "CTGAAATC").

% ==================== POSITION DOMAIN ====================
% Maximum fragment length is 8
position(0..7).

% ==================== ASSEMBLY ORDERING ====================
% Each fragment appears exactly once in the assembly
1 { position_in_assembly(F, Pos) : fragment(F) } 1 :- position(Pos).

% Each fragment has exactly one position
1 { position_in_assembly(F, Pos) : position(Pos) } 1 :- fragment(F).

% ==================== CHARACTER EXTRACTION ====================
% Extract characters from sequences manually
% Fragment 0: ATCGATCG
char(0, 0, "A"). char(0, 1, "T"). char(0, 2, "C"). char(0, 3, "G").
char(0, 4, "A"). char(0, 5, "T"). char(0, 6, "C"). char(0, 7, "G").

% Fragment 1: CGATCGTA
char(1, 0, "C"). char(1, 1, "G"). char(1, 2, "A"). char(1, 3, "T").
char(1, 4, "C"). char(1, 5, "G"). char(1, 6, "T"). char(1, 7, "A").

% Fragment 2: ATCGTAAC
char(2, 0, "A"). char(2, 1, "T"). char(2, 2, "C"). char(2, 3, "G").
char(2, 4, "T"). char(2, 5, "A"). char(2, 6, "A"). char(2, 7, "C").

% Fragment 3: CGTAACGG
char(3, 0, "C"). char(3, 1, "G"). char(3, 2, "T"). char(3, 3, "A").
char(3, 4, "A"). char(3, 5, "C"). char(3, 6, "G"). char(3, 7, "G").

% Fragment 4: TAACGGCT
char(4, 0, "T"). char(4, 1, "A"). char(4, 2, "A"). char(4, 3, "C").
char(4, 4, "G"). char(4, 5, "G"). char(4, 6, "C"). char(4, 7, "T").

% Fragment 5: ACGGCTGA
char(5, 0, "A"). char(5, 1, "C"). char(5, 2, "G"). char(5, 3, "G").
char(5, 4, "C"). char(5, 5, "T"). char(5, 6, "G"). char(5, 7, "A").

% Fragment 6: GGCTGAAA
char(6, 0, "G"). char(6, 1, "G"). char(6, 2, "C"). char(6, 3, "T").
char(6, 4, "G"). char(6, 5, "A"). char(6, 6, "A"). char(6, 7, "A").

% Fragment 7: CTGAAATC
char(7, 0, "C"). char(7, 1, "T"). char(7, 2, "G"). char(7, 3, "A").
char(7, 4, "A"). char(7, 5, "A"). char(7, 6, "T"). char(7, 7, "C").

% ==================== ADJACENCY RELATION ====================
% Two fragments are adjacent if their positions differ by 1
adjacent(F1, F2) :- position_in_assembly(F1, P1), 
                    position_in_assembly(F2, P2), 
                    P2 = P1 + 1.

% ==================== OVERLAP LENGTH CALCULATION ====================
% For each adjacent pair, calculate maximum possible overlap
% Overlap length L means last L chars of F1 match first L chars of F2
overlap_length(F1, F2, L) :- adjacent(F1, F2),
                             L = 3..8,
                             % Check character by character match
                             K = 0..L-1,
                             char(F1, 8-L+K, C1),
                             char(F2, K, C2),
                             C1 = C2.

% For each adjacent pair, take the maximum valid overlap
max_overlap(F1, F2, L) :- adjacent(F1, F2),
                          L = #max { OL : overlap_length(F1, F2, OL) }.

% ==================== CONSTRAINTS ====================
% Minimum overlap of 3 nucleotides
:- adjacent(F1, F2), max_overlap(F1, F2, L), L < 3.

% ==================== OBJECTIVE: MAXIMIZE TOTAL OVERLAP ====================
% Calculate total overlap length
total_overlap(T) :- T = #sum { L, F1, F2 : max_overlap(F1, F2, L) }.

% ==================== OUTPUT PREDICATES ====================
% Assembly path: ordered list of fragment indices
assembly_path(P, F) :- position_in_assembly(F, P).

% Overlap details for each adjacent pair
overlap_details(F1, F2, L, Pos1, Pos2) :- adjacent(F1, F2),
                                         max_overlap(F1, F2, L),
                                         Pos1 = 8 - L,  % Start position in first fragment
                                         Pos2 = 0.      % Start position in second fragment (always 0)

% Consensus sequence (simplified - just show fragments in order)
consensus_fragment(F, P) :- position_in_assembly(F, P).

% ==================== SHOW DIRECTIVES ====================
#show assembly_path/2.
#show overlap_details/5.
#show consensus_fragment/2.
#show total_overlap/1.

% ==================== OPTIMIZATION ====================
#maximize { T : total_overlap(T) }.