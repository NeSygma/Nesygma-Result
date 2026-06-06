% Workers
worker(quinn).
worker(ruiz).
worker(smith).
worker(taylor).
worker(verma).
worker(wells).
worker(xue).

% Exactly 3 members
3 { member(W) : worker(W) } 3.

% Exactly 1 leader among members
1 { leader(W) : member(W) } 1.

% Constraints
:- member(quinn), not leader(quinn).
:- member(ruiz), not leader(ruiz).
:- member(smith), not member(taylor).
:- member(wells), member(ruiz).
:- member(wells), member(verma).
:- member(taylor).
:- member(smith).

% Map options
option(a) :- member(quinn), not member(xue).
option(b) :- member(ruiz), not member(xue).
option(c) :- member(verma), not member(xue).
option(d) :- member(wells), not member(xue).
option(e) :- member(xue).

#minimize { 1@1 : member(quinn), 2@1 : member(ruiz), 3@1 : member(verma), 4@1 : member(wells), 5@1 : member(xue) }.

#show option/1.