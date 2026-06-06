% Domain declaration
man(m1; m2; m3; m4).
woman(w1; w2; w3; w4).

% Men's preference rankings (lower number = higher preference)
rank_man(m1, w1, 1; m1, w2, 2; m1, w3, 3).
rank_man(m2, w2, 1; m2, w3, 2; m2, w4, 3).
rank_man(m3, w3, 1; m3, w4, 2; m3, w1, 3).
rank_man(m4, w4, 1; m4, w1, 2; m4, w2, 3).

% Women's preference rankings (lower number = higher preference)
rank_woman(w1, m4, 1; w1, m1, 2; w1, m3, 3).
rank_woman(w2, m1, 1; w2, m2, 2; w2, m4, 3).
rank_woman(w3, m2, 1; w3, m3, 2; w3, m1, 3).
rank_woman(w4, m3, 1; w4, m4, 2; w4, m2, 3).

% Define acceptable pairs (mutual preference)
acceptable(M, W) :- rank_man(M, W, _).
acceptable(W, M) :- rank_woman(W, M, _).

% Generate possible matchings (each man matched to at most one acceptable woman)
{matched(M, W) : acceptable(M, W)} 1 :- man(M).

% Ensure each woman is matched to at most one man
:- woman(W), man(M1), man(M2), M1 != M2, matched(M1, W), matched(M2, W).

% Define current partner for readability
current_partner(M, W) :- matched(M, W).
current_partner(W, M) :- matched(M, W).

% Helper: man M prefers woman W over his current partner or being unmatched
man_prefers(M, W) :-
    man(M), woman(W),
    acceptable(M, W),
    (not current_partner(M, _);
     current_partner(M, M_current),
     rank_man(M, W, RW),
     rank_man(M, M_current, RM_current),
     RW < RM_current).

% Helper: woman W prefers man M over her current partner or being unmatched
woman_prefers(W, M) :-
    woman(W), man(M),
    acceptable(W, M),
    (not current_partner(W, _);
     current_partner(W, W_current),
     rank_woman(W, M, RM),
     rank_woman(W, W_current, RW_current),
     RM < RW_current).

% Blocking pair: M and W are not matched, both prefer each other over current partners
blocking_pair(M, W) :-
    man(M), woman(W),
    not matched(M, W),
    man_prefers(M, W),
    woman_prefers(W, M).

% Constraint: No blocking pairs allowed in a stable matching
:- blocking_pair(M, W).

% Show all matched pairs in the output
#show matched/2.