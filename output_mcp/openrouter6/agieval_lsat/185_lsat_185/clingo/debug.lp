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

% Show all members and leader
#show member/1.
#show leader/1.

% Also show which option matches
option(a) :- member(ruiz), leader(ruiz), member(taylor), member(wells).
option(b) :- member(verma), leader(verma), member(quinn), member(taylor).
option(c) :- member(verma), leader(verma), member(smith), member(taylor).
option(d) :- member(verma), leader(verma), member(smith), member(xue).
option(e) :- member(xue), leader(xue), member(verma), member(wells).

#show option/1.