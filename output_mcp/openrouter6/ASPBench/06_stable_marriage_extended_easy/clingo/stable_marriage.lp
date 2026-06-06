% Stable Marriage Problem
% Find all stable matchings between 4 men and 4 women

% 1. Define domains
man(m1). man(m2). man(m3). man(m4).
woman(w1). woman(w2). woman(w3). woman(w4).

% 2. Define preferences as ranks (1 = highest preference)
% Men's preferences
rank_man(m1, w1, 1). rank_man(m1, w2, 2). rank_man(m1, w3, 3).
rank_man(m2, w2, 1). rank_man(m2, w3, 2). rank_man(m2, w4, 3).
rank_man(m3, w3, 1). rank_man(m3, w4, 2). rank_man(m3, w1, 3).
rank_man(m4, w4, 1). rank_man(m4, w1, 2). rank_man(m4, w2, 3).

% Women's preferences
rank_woman(w1, m4, 1). rank_woman(w1, m1, 2). rank_woman(w1, m3, 3).
rank_woman(w2, m1, 1). rank_woman(w2, m2, 2). rank_woman(w2, m4, 3).
rank_woman(w3, m2, 1). rank_woman(w3, m3, 2). rank_woman(w3, m1, 3).
rank_woman(w4, m3, 1). rank_woman(w4, m4, 2). rank_woman(w4, m2, 3).

% 3. Define acceptable pairs (both find each other acceptable)
acceptable(M, W) :- rank_man(M, W, _), rank_woman(W, M, _).

% 4. Define matching: each person can be matched to at most one partner
% Use choice rules for acceptable pairs
{ match(M, W) } :- acceptable(M, W).

% Each man matched to at most one woman
:- man(M), #count{ W : match(M, W) } > 1.
% Each woman matched to at most one man
:- woman(W), #count{ M : match(M, W) } > 1.

% 5. Define current partners (for stability checking)
partner_man(M, W) :- match(M, W).
partner_woman(W, M) :- match(M, W).

% 6. Define preference comparisons
% Helper: man is unmatched
man_unmatched(M) :- man(M), not partner_man(M, _).
% Helper: woman is unmatched
woman_unmatched(W) :- woman(W), not partner_woman(W, _).

% Man M prefers woman W over his current partner
prefers_man_over_current(M, W) :-
    man(M), acceptable(M, W), partner_man(M, P), P != W,
    rank_man(M, W, R1), rank_man(M, P, R2), R1 < R2.

% Man M prefers W because he's unmatched
prefers_man_over_current(M, W) :-
    man(M), acceptable(M, W), man_unmatched(M).

% Woman W prefers man M over her current partner
prefers_woman_over_current(W, M) :-
    woman(W), acceptable(M, W), partner_woman(W, P), P != M,
    rank_woman(W, M, R1), rank_woman(W, P, R2), R1 < R2.

% Woman W prefers M because she's unmatched
prefers_woman_over_current(W, M) :-
    woman(W), acceptable(M, W), woman_unmatched(W).

% 7. Stability constraint: no blocking pairs
% A blocking pair is an acceptable pair (M,W) not matched to each other,
% where both prefer each other over their current partners (or being unmatched)
:- acceptable(M, W), not match(M, W),
   prefers_man_over_current(M, W),
   prefers_woman_over_current(W, M).

% 8. Output: show all stable matchings
#show match/2.

% 9. Count stable matchings (will be computed externally by counting answer sets)
% Note: Clingo will output each stable matching as a separate answer set