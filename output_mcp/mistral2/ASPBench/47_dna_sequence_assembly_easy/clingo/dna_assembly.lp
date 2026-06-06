% Define the DNA fragments.
fragment(0, "ATCGATCG").
fragment(1, "CGATCGTA").
fragment(2, "ATCGTAAC").
fragment(3, "CGTAACGG").
fragment(4, "TAACGGCT").
fragment(5, "ACGGCTGA").
fragment(6, "GGCTGAAA").
fragment(7, "CTGAAATC").

% Precompute all possible overlaps between fragments.
% overlap(I, J, O) means fragment I and fragment J have an overlap of length O.
overlap(0, 1, 6).
overlap(1, 0, 6).
overlap(1, 2, 4).
overlap(2, 1, 4).
overlap(2, 3, 4).
overlap(3, 2, 4).
overlap(3, 4, 4).
overlap(4, 3, 4).
overlap(4, 5, 6).
overlap(5, 4, 6).
overlap(5, 6, 5).
overlap(6, 5, 5).
overlap(6, 7, 6).
overlap(7, 6, 6).
overlap(0, 2, 4).
overlap(2, 0, 4).
overlap(1, 3, 4).
overlap(3, 1, 4).
overlap(2, 4, 4).
overlap(4, 2, 4).
overlap(3, 5, 4).
overlap(5, 3, 4).
overlap(4, 6, 4).
overlap(6, 4, 4).
overlap(5, 7, 4).
overlap(7, 5, 4).

% Generate the assembly path: a permutation of all fragments.
1 { assembly_path(I, J) : fragment(J, _) } 1 :- fragment(I, _).
:- assembly_path(I, J), assembly_path(I, K), J != K.

% Ensure all fragments are used exactly once.
:- fragment(J, _), not used(J).
used(J) :- assembly_path(_, J).

% Ensure the assembly path is a single linear sequence.
:- assembly_path(I, J), assembly_path(K, J), I != K.

% Define a predicate to check overlaps between adjacent fragments in the assembly path.
has_valid_overlap(I, J) :- assembly_path(I, J), overlap(I, J, _).

% Ensure every adjacent pair in the assembly path has a valid overlap.
:- assembly_path(I, J), not has_valid_overlap(I, J).

% Calculate total overlap length.
total_overlap(L) :- L = #sum { OL : assembly_path(I, J), overlap(I, J, OL) }.

% Maximize the total overlap length.
#maximize { L : total_overlap(L) }.

% Show directives.
#show assembly_path/2.
#show total_overlap/1.