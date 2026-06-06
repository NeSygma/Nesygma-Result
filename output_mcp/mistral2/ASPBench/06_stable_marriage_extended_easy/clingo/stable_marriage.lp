% Domains
man(m1; m2; m3; m4).
woman(w1; w2; w3; w4).

% Men's preferences (in order of decreasing preference)
prefers_man(m1, w1, w2). prefers_man(m1, w2, w3).
prefers_man(m2, w2, w3). prefers_man(m2, w3, w4).
prefers_man(m3, w3, w4). prefers_man(m3, w4, w1).
prefers_man(m4, w4, w1). prefers_man(m4, w1, w2).

% Women's preferences (in order of decreasing preference)
prefers_woman(w1, m4, m1). prefers_woman(w1, m1, m3).
prefers_woman(w2, m1, m2). prefers_woman(w2, m2, m4).
prefers_woman(w3, m2, m3). prefers_woman(w3, m3, m1).
prefers_woman(w4, m3, m4). prefers_woman(w4, m4, m2).

% Acceptability (only listed partners are acceptable)
acceptable_man(w1, m4). acceptable_man(w1, m1). acceptable_man(w1, m3).
acceptable_man(w2, m1). acceptable_man(w2, m2). acceptable_man(w2, m4).
acceptable_man(w3, m2). acceptable_man(w3, m3). acceptable_man(w3, m1).
acceptable_man(w4, m3). acceptable_man(w4, m4). acceptable_man(w4, m2).

acceptable_woman(m1, w1). acceptable_woman(m1, w2). acceptable_woman(m1, w3).
acceptable_woman(m2, w2). acceptable_woman(m2, w3). acceptable_woman(m2, w4).
acceptable_woman(m3, w3). acceptable_woman(m3, w4). acceptable_woman(m3, w1).
acceptable_woman(m4, w4). acceptable_woman(m4, w1). acceptable_woman(m4, w2).

% Generate possible matchings
{ matched(M, W) : woman(W) } 1 :- man(M).
{ matched(W, M) : man(M) } 1 :- woman(W).

% Ensure only acceptable pairs are matched
:- matched(M, W), not acceptable_woman(M, W).
:- matched(W, M), not acceptable_man(W, M).

% Ensure no two people are matched to each other in conflicting ways
:- matched(M, W1), matched(M, W2), W1 != W2.
:- matched(W, M1), matched(W, M2), M1 != M2.

% Define a helper to check if a man prefers a woman over his current partner
prefers_man_over_current(M, W) :-
    matched(M, W_current),
    prefers_man(M, W, W_current),
    acceptable_woman(M, W).

prefers_man_over_current(M, W) :-
    not matched(M, _),
    acceptable_woman(M, W).

% Define a helper to check if a woman prefers a man over her current partner
prefers_woman_over_current(W, M) :-
    matched(W, M_current),
    prefers_woman(W, M, M_current),
    acceptable_man(W, M).

prefers_woman_over_current(W, M) :-
    not matched(W, _),
    acceptable_man(W, M).

% Define a blocking pair
blocking_pair(M, W) :-
    not matched(M, W),
    acceptable_woman(M, W),
    acceptable_man(W, M),
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