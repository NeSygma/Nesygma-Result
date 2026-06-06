% Domains
man(m1; m2; m3; m4).
woman(w1; w2; w3; w4).

% Men's preferences (in order of decreasing preference)
% m1: w1 > w2 > w3
% m2: w2 > w3 > w4
% m3: w3 > w4 > w1
% m4: w4 > w1 > w2
% Represent preferences as a list of acceptable partners in order
prefers_man(m1, w1). prefers_man(m1, w2). prefers_man(m1, w3).
prefers_man(m2, w2). prefers_man(m2, w3). prefers_man(m2, w4).
prefers_man(m3, w3). prefers_man(m3, w4). prefers_man(m3, w1).
prefers_man(m4, w4). prefers_man(m4, w1). prefers_man(m4, w2).

% Women's preferences (in order of decreasing preference)
% w1: m4 > m1 > m3
% w2: m1 > m2 > m4
% w3: m2 > m3 > m1
% w4: m3 > m4 > m2
prefers_woman(w1, m4). prefers_woman(w1, m1). prefers_woman(w1, m3).
prefers_woman(w2, m1). prefers_woman(w2, m2). prefers_woman(w2, m4).
prefers_woman(w3, m2). prefers_woman(w3, m3). prefers_woman(w3, m1).
prefers_woman(w4, m3). prefers_woman(w4, m4). prefers_woman(w4, m2).

% Generate possible matchings
1 { matched(M, W) : woman(W) } 1 :- man(M).
1 { matched(W, M) : man(M) } 1 :- woman(W).

% Define a helper to check if a man prefers a woman over his current partner
% Case 1: man is matched to someone else
prefers_man_over_current(M, W) :-
    matched(M, W_current),
    prefers_man(M, W),
    prefers_man(M, W_current),
    W != W_current.

% Case 2: man is unmatched
prefers_man_over_current(M, W) :-
    not matched(M, _),
    prefers_man(M, W).

% Define a helper to check if a woman prefers a man over her current partner
% Case 1: woman is matched to someone else
prefers_woman_over_current(W, M) :-
    matched(W, M_current),
    prefers_woman(W, M),
    prefers_woman(W, M_current),
    M != M_current.

% Case 2: woman is unmatched
prefers_woman_over_current(W, M) :-
    not matched(W, _),
    prefers_woman(W, M).

% Define a blocking pair
blocking_pair(M, W) :-
    not matched(M, W),
    not matched(W, M),
    prefers_man_over_current(M, W),
    prefers_woman_over_current(W, M).

% Ensure no blocking pairs exist in a stable matching
:- blocking_pair(M, W).

% Collect stable matchings
stable_matching(M, W) :- matched(M, W).

% Count the number of stable matchings
count(N) :- N = #count{ M, W : stable_matching(M, W) }.

% Show the results
#show stable_matching/2.
#show count/1.