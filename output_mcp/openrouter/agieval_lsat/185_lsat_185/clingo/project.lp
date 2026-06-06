% Workers are represented as constants
% Answer choices
1 { ans(a); ans(b); ans(c); ans(d); ans(e) } 1.

% Define members and leader for each answer
member(ruiz) :- ans(a).
member(taylor) :- ans(a).
member(wells) :- ans(a).
leader(ruiz) :- ans(a).

member(verma) :- ans(b).
member(quinn) :- ans(b).
member(taylor) :- ans(b).
leader(verma) :- ans(b).

member(verma) :- ans(c).
member(smith) :- ans(c).
member(taylor) :- ans(c).
leader(verma) :- ans(c).

member(verma) :- ans(d).
member(smith) :- ans(d).
member(xue) :- ans(d).
leader(verma) :- ans(d).

member(xue) :- ans(e).
member(verma) :- ans(e).
member(wells) :- ans(e).
leader(xue) :- ans(e).

% Constraints
% Exactly three members
:- #count { X : member(X) } != 3.
% Exactly one leader
:- #count { X : leader(X) } != 1.
% Leader must be a member
:- leader(L), not member(L).
% Quinn or Ruiz can be a member only if they are leader
:- member(quinn), not leader(quinn).
:- member(ruiz), not leader(ruiz).
% If Smith is a member, Taylor must also be a member
:- member(smith), not member(taylor).
% If Wells is a member, neither Ruiz nor Verma can be members
:- member(wells), member(ruiz).
:- member(wells), member(verma).

% Map the correct answer to option/1 (MANDATORY)
option(a) :- ans(a).
option(b) :- ans(b).
option(c) :- ans(c).
option(d) :- ans(d).
option(e) :- ans(e).

#show option/1.