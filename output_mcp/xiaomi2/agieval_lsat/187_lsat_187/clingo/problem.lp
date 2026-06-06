% Workers
worker(quinn). worker(ruiz). worker(smith). worker(taylor). worker(verma). worker(wells). worker(xue).

% Two possible selections when Verma is leader (derived from constraints)
selection(1). selection(2).

% Selection 1: members are verma, smith, taylor
members(1, verma). members(1, smith). members(1, taylor).
leader(1, verma).

% Selection 2: members are verma, taylor, xue
members(2, verma). members(2, taylor). members(2, xue).
leader(2, verma).

% Define selected
selected(W, S) :- members(S, W).

% Conditions for each option (need selection(S) to ground S)
condition_a(S) :- selection(S), not selected(quinn, S), not selected(smith, S).
condition_b(S) :- selection(S), not selected(ruiz, S), not selected(taylor, S).
condition_c(S) :- selection(S), not selected(smith, S), not selected(taylor, S).
condition_d(S) :- selection(S), not selected(smith, S), not selected(xue, S).
condition_e(S) :- selection(S), not selected(taylor, S), not selected(wells, S).

% Possible if condition holds for some selection
possible(a) :- condition_a(S), selection(S).
possible(b) :- condition_b(S), selection(S).
possible(c) :- condition_c(S), selection(S).
possible(d) :- condition_d(S), selection(S).
possible(e) :- condition_e(S), selection(S).

% Map the correct answer to option/1
option(a) :- possible(a).
option(b) :- possible(b).
option(c) :- possible(c).
option(d) :- possible(d).
option(e) :- possible(e).

#show option/1.