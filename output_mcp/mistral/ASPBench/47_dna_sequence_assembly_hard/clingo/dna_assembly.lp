% DNA Fragment Assembly Problem

% --- Input Data ---
% Fragments with their sequences as lists of characters
fragment("F0", ["A","T","G","G","G","C","G","C"]).
fragment("F1", ["G","G","C","G","C","C","A","T"]).
fragment("F2", ["G","C","C","A","T","T"]).
fragment("F3", ["A","T","T","T","A","A"]).
fragment("F4", ["A","T","G","C","C","T","C","G"]).
fragment("F5", ["G","C","T","C","G","A","G","G"]).
fragment("F6", ["T","C","G","A","G","C","T","G"]).
fragment("F7", ["A","G","C","T","G","A"]).
fragment("F8", ["A","T","T","C","G"]).

% Precompute reverse complements for each fragment
revcomp("F0", ["G","C","G","C","C","A","T"]).
revcomp("F1", ["A","T","G","G","C","G","C","C"]).
revcomp("F2", ["A","A","T","G","G","C"]).
revcomp("F3", ["T","T","A","A","A","T"]).
revcomp("F4", ["C","G","A","G","G","C","A","T"]).
revcomp("F5", ["C","C","T","C","G","A","G","C"]).
revcomp("F6", ["C","A","G","C","T","C","G","A"]).
revcomp("F7", ["T","C","A","G","C","T"]).
revcomp("F8", ["C","G","A","A","T"]).

% Precompute GC-content for each fragment
% GC-content > 50% means at least 50% G or C bases
gc_high(F) :- fragment(F, S), #count{C : member(C, S), (C == "G" ; C == "C")} * 2 > #count{C : member(C, S)}.

% Helper to split a sequence into its bases
member(C, S) :- fragment(_, S), C = "A".
member(C, S) :- fragment(_, S), C = "T".
member(C, S) :- fragment(_, S), C = "G".
member(C, S) :- fragment(_, S), C = "C".

% --- Orientation Handling ---
% Possible orientations for each fragment
orientation(F, forward) | orientation(F, reverse) :- fragment(F, _).

% Get the actual sequence based on orientation
seq(F, S) :- fragment(F, S), orientation(F, forward).
seq(F, RC) :- revcomp(F, RC), orientation(F, reverse).

% --- Contig Structure ---
% Contig IDs (we expect at least 2 contigs)
contig(1..9).

% A fragment can be in at most one contig or marked chimeric
1 { in_contig(F, C) : contig(C) } 1 :- fragment(F, _).
{ chimeric(F) } :- fragment(F, _).

% If a fragment is in a contig, it cannot be chimeric
:- in_contig(F, _), chimeric(F).

% --- Ordering within contigs ---
% Define a partial order of fragments within each contig
{ order(F1, F2, C) : contig(C) } :- in_contig(F1, C), in_contig(F2, C), F1 != F2.

% Each contig must have a linear order (transitivity and acyclicity)
% We'll enforce this via constraints

% --- Overlap Requirements ---
% Adjacent fragments must overlap by at least:
% - 4 bases if both have GC-content > 50%
% - 3 bases otherwise

% Helper: Check if sequence S1 overlaps with S2 by at least N bases
% We'll define this by checking all possible overlaps

has_sufficient_overlap(S1, S2, N) :-
    suffix(S1, N, Overlap),
    prefix(S2, N, Overlap).

% Helper: Get the suffix of a sequence of length N
suffix(S, N, Suffix) :-
    seq(_, S),
    N <= #len(S),
    Suffix = #last(S, N).

% Helper: Get the prefix of a sequence of length N
prefix(S, N, Prefix) :-
    seq(_, S),
    N <= #len(S),
    Prefix = #first(S, N).

% Overlap constraint between two fragments in a contig
:- order(F1, F2, C),
   in_contig(F1, C),
   in_contig(F2, C),
   seq(F1, S1),
   seq(F2, S2),
   gc_high(F1),
   gc_high(F2),
   not has_sufficient_overlap(S1, S2, 4).

:- order(F1, F2, C),
   in_contig(F1, C),
   in_contig(F2, C),
   seq(F1, S1),
   seq(F2, S2),
   (not gc_high(F1) ; not gc_high(F2)),
   not has_sufficient_overlap(S1, S2, 3).

% --- Start and Stop Codon Requirements ---
% Each contig must start with ATG and end with a stop codon

% Start codon: ATG at the beginning
:- in_contig(F, C),
   not has_predecessor(F, C),
   seq(F, S),
   not starts_with_atg(S).

starts_with_atg(S) :- seq(F, S), S = ["A","T","G"].
starts_with_atg(S) :- seq(F, S), #len(S) >= 3, #first(S, 3) = ["A","T","G"].

% Stop codon: TAA, TAG, or TGA at the end
:- in_contig(F, C),
   not has_successor(F, C),
   seq(F, S),
   not ends_with_stop(S).

ends_with_stop(S) :- seq(F, S), #len(S) >= 3, #last(S, 3) = ["T","A","A"].
ends_with_stop(S) :- seq(F, S), #len(S) >= 3, #last(S, 3) = ["T","A","G"].
ends_with_stop(S) :- seq(F, S), #len(S) >= 3, #last(S, 3) = ["T","G","A"].

% Helper: Check if a fragment has no predecessor in a contig
has_predecessor(F, C) :- order(F2, F, C).

% Helper: Check if a fragment has no successor in a contig
has_successor(F, C) :- order(F, F2, C).

% --- Contig Sequence Assembly ---
% Assemble the complete sequence for each contig
% The sequence is the concatenation of fragments in order

% Base case: first fragment in contig
first_fragment(F, C) :- in_contig(F, C), not has_predecessor(F, C).

% Build contig sequence step by step
contig_seq_step(C, F, S, 1) :- first_fragment(F, C), seq(F, S).

contig_seq_step(C, F2, NewSeq, T+1) :-
    order(F1, F2, C),
    contig_seq_step(C, F1, S1, T),
    seq(F2, S2),
    suffix(S1, O, Overlap),
    prefix(S2, O, Overlap),
    O >= 3,
    #len(S1) >= O,
    #len(S2) >= O,
    #first(S1, #len(S1)-O) = Prefix1,
    #last(S2, #len(S2)-O) = Suffix2,
    append(Prefix1, S2, NewSeq).

% Final contig sequence
sequence(C, S) :- contig_seq_step(C, _, S, _).

% --- Helper Predicates for List Manipulation ---
% Append two lists
append([], L, L).
append([H|T], L, [H|R]) :- append(T, L, R).

% Get the first N elements of a list
#first(L, N, F) :- F = #take(L, N).

% Get the last N elements of a list
#last(L, N, F) :- F = #drop(L, #len(L)-N).

% Get the length of a list
#len(L, N) :- N = #count{E : member(E, L)}.

% --- Objective: Minimize the number of contigs used ---
% Count the number of contigs that actually have fragments
used_contig(C) :- in_contig(_, C).

% Minimize the number of used contigs
#minimize { 1@1,C : used_contig(C) }.

% --- Output ---
#show in_contig/2.
#show chimeric/1.
#show sequence/2.
#show orientation/2.