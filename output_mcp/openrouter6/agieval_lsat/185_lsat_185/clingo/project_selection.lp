% Workers
worker(quinn). worker(ruiz). worker(smith). worker(taylor). worker(verma). worker(wells). worker(xue).

% Exactly three members and exactly one leader
1 { member(W) : worker(W) } 3.
1 { leader(W) : worker(W) } 1.

% Leader must be a member
:- leader(W), not member(W).

% Constraints
:- member(quinn), not leader(quinn).
:- member(ruiz), not leader(ruiz).
:- member(smith), not member(taylor).
:- member(wells), member(ruiz).
:- member(wells), member(verma).

% Define matches for each option
matches_a :- member(ruiz), leader(ruiz), member(taylor), member(wells).
matches_b :- member(verma), leader(verma), member(quinn), member(taylor).
matches_c :- member(verma), leader(verma), member(smith), member(taylor).
matches_d :- member(verma), leader(verma), member(smith), member(xue).
matches_e :- member(xue), leader(xue), member(verma), member(wells).

% Derive option if matches
option(a) :- matches_a.
option(b) :- matches_b.
option(c) :- matches_c.
option(d) :- matches_d.
option(e) :- matches_e.

% Ensure only one option is derived (since only one is acceptable)
:- option(X), option(Y), X != Y.

#show option/1.