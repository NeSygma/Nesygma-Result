% Domains
man(m1; m2; m3; m4).
woman(w1; w2; w3; w4).

% Preferences: person, partner, rank
% Men's preferences
pref(m1, w1, 1). pref(m1, w2, 2). pref(m1, w3, 3).
pref(m2, w2, 1). pref(m2, w3, 2). pref(m2, w4, 3).
pref(m3, w3, 1). pref(m3, w4, 2). pref(m3, w1, 3).
pref(m4, w4, 1). pref(m4, w1, 2). pref(m4, w2, 3).

% Women's preferences
pref(w1, m4, 1). pref(w1, m1, 2). pref(w1, m3, 3).
pref(w2, m1, 1). pref(w2, m2, 2). pref(w2, m4, 3).
pref(w3, m2, 1). pref(w3, m3, 2). pref(w3, m1, 3).
pref(w4, m3, 1). pref(w4, m4, 2). pref(w4, m2, 3).

% Acceptability: both find each other acceptable
acceptable(M, W) :- pref(M, W, _), pref(W, M, _).

% Matching: any subset of acceptable pairs
{ match(M, W) : acceptable(M, W) }.

% Each person matched to at most one partner
:- man(M), #count { W : match(M, W) } > 1.
:- woman(W), #count { M : match(M, W) } > 1.

% Helper: matched status
matched_man(M, W) :- match(M, W).
matched_woman(W, M) :- match(M, W).

unmatched_man(M) :- man(M), not matched_man(M, _).
unmatched_woman(W) :- woman(W), not matched_woman(W, _).

% Preference comparison
prefers_man(M, W1, W2) :- man(M), woman(W1), woman(W2), pref(M, W1, R1), pref(M, W2, R2), R1 < R2.
prefers_woman(W, M1, M2) :- woman(W), man(M1), man(M2), pref(W, M1, R1), pref(W, M2, R2), R1 < R2.

% Man would prefer to switch to W (either unmatched, or prefers W over current)
man_would_prefer(M, W) :-
    acceptable(M, W), not match(M, W),
    unmatched_man(M).
man_would_prefer(M, W) :-
    acceptable(M, W), not match(M, W),
    matched_man(M, W_cur),
    prefers_man(M, W, W_cur).

% Woman would prefer to switch to M (either unmatched, or prefers M over current)
woman_would_prefer(W, M) :-
    acceptable(M, W), not match(M, W),
    unmatched_woman(W).
woman_would_prefer(W, M) :-
    acceptable(M, W), not match(M, W),
    matched_woman(W, M_cur),
    prefers_woman(W, M, M_cur).

% Blocking pair
blocking(M, W) :-
    acceptable(M, W), not match(M, W),
    man_would_prefer(M, W),
    woman_would_prefer(W, M).

% No blocking pair allowed
:- blocking(M, W).

#show match/2.