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

% ==================== OVERLAP CALCULATION ====================
% Helper: Get character at position in fragment
char(F, P, C) :- sequence(F, Seq), 
                 P = 0, substr(Seq, 0, 1, C).
char(F, P, C) :- sequence(F, Seq), 
                 P = 1, substr(Seq, 1, 1, C).
char(F, P, C) :- sequence(F, Seq), 
                 P = 2, substr(Seq, 2, 1, C).
char(F, P, C) :- sequence(F, Seq), 
                 P = 3, substr(Seq, 3, 1, C).
char(F, P, C) :- sequence(F, Seq), 
                 P = 4, substr(Seq, 4, 1, C).
char(F, P, C) :- sequence(F, Seq), 
                 P = 5, substr(Seq, 5, 1, C).
char(F, P, C) :- sequence(F, Seq), 
                 P = 6, substr(Seq, 6, 1, C).
char(F, P, C) :- sequence(F, Seq), 
                 P = 7, substr(Seq, 7, 1, C).

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
                             % Check that overlap is valid (L <= min(length(F1), length(F2)))
                             L <= 8,
                             % Check character by character match
                             K = 0..L-1,
                             char(F1, 8-L+K, C),
                             char(F2, K, C).

% For each adjacent pair, take the maximum valid overlap
max_overlap(F1, F2, L) :- adjacent(F1, F2),
                          L = #max { OL : overlap_length(F1, F2, OL) }.

% ==================== CONSTRAINTS ====================
% All fragments must be used (already enforced by position_in_assembly)
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