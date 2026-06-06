% Fragments
fragment(0..8).

% Transitions (Precomputed based on overlap constraints)
% F0: ATGGGCGC, F1: GGCGCCAT, F2: GCCATT, F3: ATTTAA, F4: ATGCCTCG, F5: GCTCGAGG, F6: TCGAGCTG, F7: AGCTGA, F8: ATTCG
% Valid transitions (F1, O1) -> (F2, O2)
transition(0, forward, 1, forward).
transition(4, forward, 5, forward).
transition(5, forward, 6, forward).
transition(6, forward, 7, forward).
transition(8, forward, 6, forward).

% Contig assembly
contig(1..9).
orientation(forward; reverse).

{ used(F) } :- fragment(F).
{ pos(F, C, P) : contig(C), P = 1..9 } 1 :- used(F).
{ orient(F, C, O) : orientation(O) } 1 :- used(F), pos(F, C, _).

% Constraints
:- pos(F1, C, P), pos(F2, C, P), F1 != F2.
has_pos(C, P) :- pos(_, C, P).
:- has_pos(C, P), P > 1, not has_pos(C, P-1).

% Transitions
:- pos(F1, C, P), pos(F2, C, P+1), orient(F1, C, O1), orient(F2, C, O2),
   not transition(F1, O1, F2, O2).

% Start/Stop
% Start: F0(fwd) starts with ATG, F4(fwd) starts with ATG
is_start(F) :- F == 0.
is_start(F) :- F == 4.
:- pos(F, C, 1), orient(F, C, forward), not is_start(F).

% Stop: F3(fwd) ends with TAA, F7(fwd) ends with TGA
is_stop(F) :- F == 3.
is_stop(F) :- F == 7.
:- pos(F, C, P), has_pos(C, P+1), not has_pos(C, P+1). % Dummy to force P to be last
% Correct way to check last:
last_pos(C, P) :- pos(_, C, P), not has_pos(C, P+1).
:- last_pos(C, P), pos(F, C, P), orient(F, C, forward), not is_stop(F).

% Minimize
active_contig(C) :- has_pos(C, _).
#minimize { 1, C : active_contig(C) }.

#show pos/3.
#show orient/3.
#show active_contig/1.