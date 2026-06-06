% Domain
scientist(f). scientist(g). scientist(h).
scientist(k). scientist(l). scientist(m).
scientist(p). scientist(q). scientist(r).

% Types
type(f, botanist). type(g, botanist). type(h, botanist).
type(k, chemist). type(l, chemist). type(m, chemist).
type(p, zoologist). type(q, zoologist). type(r, zoologist).

% Fixed selected scientists (given)
fixed(f). fixed(l). fixed(q). fixed(r).
selected(X) :- fixed(X).

% Remaining scientists (not fixed)
remaining(X) :- scientist(X), not fixed(X).

% Choose exactly one more scientist from the remaining
{ selected(X) : remaining(X) } 1.

% Constraint 1: At least one of each type
selected_type(T) :- selected(X), type(X, T).
:- not selected_type(botanist).
:- not selected_type(chemist).
:- not selected_type(zoologist).

% Constraint 2: If more than one botanist, then at most one zoologist
botanist_count(N) :- N = #count{ X : selected(X), type(X, botanist) }.
zoologist_count(M) :- M = #count{ X : selected(X), type(X, zoologist) }.
:- botanist_count(N), N > 1, zoologist_count(M), M > 1.

% Constraint 3: F and K cannot both be selected
:- selected(f), selected(k).

% Constraint 4: K and M cannot both be selected
:- selected(k), selected(m).

% Constraint 5: If M is selected, then both P and R must be selected
:- selected(m), not selected(p).
% Note: R is already fixed, so no need to enforce selected(r) again.

% Map the correct answer to option/1
option(a) :- selected(g).
option(b) :- selected(h).
option(c) :- selected(k).
option(d) :- selected(m).
option(e) :- selected(p).

#show option/1.