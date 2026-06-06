% Stable Marriage Problem - All Stable Matchings

% Domain declarations
man(m1). man(m2). man(m3). man(m4).
woman(w1). woman(w2). woman(w3). woman(w4).

% Men's preferences (rank 1 = highest preference)
prefers_man(m1, w1, 1). prefers_man(m1, w2, 2). prefers_man(m1, w3, 3).
prefers_man(m2, w2, 1). prefers_man(m2, w3, 2). prefers_man(m2, w4, 3).
prefers_man(m3, w3, 1). prefers_man(m3, w4, 2). prefers_man(m3, w1, 3).
prefers_man(m4, w4, 1). prefers_man(m4, w1, 2). prefers_man(m4, w2, 3).

% Women's preferences (rank 1 = highest preference)
prefers_woman(w1, m4, 1). prefers_woman(w1, m1, 2). prefers_woman(w1, m3, 3).
prefers_woman(w2, m1, 1). prefers_woman(w2, m2, 2). prefers_woman(w2, m4, 3).
prefers_woman(w3, m2, 1). prefers_woman(w3, m3, 2). prefers_woman(w3, m1, 3).
prefers_woman(w4, m3, 1). prefers_woman(w4, m4, 2). prefers_woman(w4, m2, 3).

% Acceptable pairs (both find each other acceptable)
acceptable(M, W) :- prefers_man(M, W, _), prefers_woman(W, M, _).

% Helper: Man M prefers W1 over W2 (lower rank number = higher preference)
better_than_current_man(M, W1, W2) :- 
    prefers_man(M, W1, R1), prefers_man(M, W2, R2), R1 < R2.

% Helper: Woman W prefers M1 over M2
better_than_current_woman(W, M1, M2) :- 
    prefers_woman(W, M1, R1), prefers_woman(W, M2, R2), R1 < R2.

% Generate all possible matchings using choice rules
% Each man can be matched to at most one woman
{ matched(M, W) : woman(W) } 1 :- man(M).
% Each woman can be matched to at most one man  
{ matched(M, W) : man(M) } 1 :- woman(W).

% Only acceptable pairs can be matched
:- matched(M, W), not acceptable(M, W).

% Define blocking pair: (M, W) is a blocking pair if:
% 1. M and W are not matched to each other
% 2. Both find each other acceptable
% 3. M prefers W over his current partner (or is unmatched)
% 4. W prefers M over her current partner (or is unmatched)

% Case 1: M is matched to someone else, prefers W over current partner
% W prefers M over her current partner OR is unmatched
blocking_pair(M, W) :-
    man(M), woman(W),
    not matched(M, W),
    acceptable(M, W),
    matched(M, Wm),
    better_than_current_man(M, W, Wm),
    (matched(Mw, W) -> better_than_current_woman(W, M, Mw); true).

% Case 2: M is unmatched, W prefers M over her current partner
blocking_pair(M, W) :-
    man(M), woman(W),
    not matched(M, W),
    acceptable(M, W),
    not matched(M, _),
    matched(Mw, W),
    better_than_current_woman(W, M, Mw).

% Case 3: Both are unmatched
blocking_pair(M, W) :-
    man(M), woman(W),
    not matched(M, W),
    acceptable(M, W),
    not matched(M, _),
    not matched(_, W).

% No blocking pairs allowed in a stable matching
:- blocking_pair(M, W).

% Show the matching
#show matched/2.