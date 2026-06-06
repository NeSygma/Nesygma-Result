% Arguments
arg(a1; a2; a3; a4; a5; a6; a7; a8; a9; a10; a11; a12; a13; a14; a15; a16).

% Levels
level(a1, 1). level(a2, 1). level(a3, 1). level(a4, 1). level(a5, 1). level(a6, 1).
level(a7, 2). level(a8, 2). level(a9, 2). level(a10, 2). level(a11, 2). level(a12, 2).
level(a13, 3). level(a14, 3). level(a15, 3). level(a16, 3).

% Attacks
attack(a2, a1, strong).
attack(a9, a8, strong).
attack(a14, a13, strong).
attack(a15, a16, strong).
attack(a1, a14, strong).
attack(a16, a15, strong).
attack(a1, a3, strong).
attack(a1, a4, strong).
attack(a13, a7, strong).
attack(a13, a10, strong).
attack(a3, a5, strong).
attack(a5, a3, strong).

attack(a8, a2, weak).
attack(a13, a9, weak).
attack(a8, a5, weak).
attack(a8, a6, weak).
attack(a16, a11, weak).
attack(a16, a12, weak).
attack(a2, a7, weak).
attack(a10, a13, weak).

% Successful attacks
successful(A, B) :- attack(A, B, strong).
successful(A, B) :- attack(A, B, weak), level(A, LA), level(B, LB), LA > LB.

% Generate extension
{ in(A) } :- arg(A).

% Admissibility
% 1. Conflict-free
:- in(A), in(B), successful(A, B).
% 2. Self-defending
:- in(A), successful(B, A), not defended(B).
defended(B) :- in(C), successful(C, B).

% Maximality (Preferred Extension)
% An admissible set S is preferred if there is no admissible set S' such that S is a proper subset of S'.
% We can define a predicate 'can_add(X)' which is true if adding X to the current set 'in' maintains admissibility.

% Helper: B is defended by S U {X}
defended_by_S_or_X(B, X) :- in(C), successful(C, B).
defended_by_S_or_X(B, X) :- successful(X, B).

% can_add(X) if:
% 1. X is not in S
% 2. S U {X} is conflict-free
% 3. S U {X} is self-defending

% 2. Conflict-free with X
conflict_with_X(X) :- in(A), successful(X, A).
conflict_with_X(X) :- in(A), successful(A, X).
conflict_with_X(X) :- successful(X, X).

% 3. Self-defending with X
% - For all B that attack X, B must be defended by S U {X}
% - For all B that attack A in S, B must be defended by S U {X}
not_defended_with_X(B, X) :- arg(X), successful(B, X), not defended_by_S_or_X(B, X).
not_defended_with_X(B, X) :- arg(X), in(A), successful(B, A), not defended_by_S_or_X(B, X).

can_add(X) :- arg(X), not in(X),
              not conflict_with_X(X),
              not exists_not_defended_with_X(X).

exists_not_defended_with_X(X) :- arg(X), not_defended_with_X(_, X).

:- can_add(_).

#show in/1.