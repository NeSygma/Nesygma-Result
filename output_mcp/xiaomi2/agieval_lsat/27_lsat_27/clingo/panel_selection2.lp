% Domain: scientists and their types
scientist(f). scientist(g). scientist(h).
scientist(k). scientist(l). scientist(m).
scientist(p). scientist(q). scientist(r).

type(f, botanist). type(g, botanist). type(h, botanist).
type(k, chemist). type(l, chemist). type(m, chemist).
type(p, zoologist). type(q, zoologist). type(r, zoologist).

% Given: F, L, Q, R are already selected
selected(f).
selected(l).
selected(q).
selected(r).

% Choose exactly one more scientist from the remaining five
{ selected(X) : scientist(X), X != f, X != l, X != q, X != r } = 1.

% Constraint 1: At least one of each type
has_type(T) :- selected(X), type(X, T).
:- not has_type(botanist).
:- not has_type(chemist).
:- not has_type(zoologist).

% Constraint 2: If more than one botanist, then at most one zoologist
bot_count(N) :- N = #count{X : selected(X), type(X, botanist)}.
zoo_count(N) :- N = #count{X : selected(X), type(X, zoologist)}.
:- bot_count(NB), NB > 1, zoo_count(NZ), NZ > 1.

% Constraint 3: F and K cannot both be selected
:- selected(f), selected(k).

% Constraint 4: K and M cannot both be selected
:- selected(k), selected(m).

% Constraint 5: If M is selected, both P and R must be selected
:- selected(m), not selected(p).
:- selected(m), not selected(r).

% Determine which scientist is the fifth
fifth(X) :- selected(X), X != f, X != l, X != q, X != r.

% Map to answer options
option(a) :- fifth(g).
option(b) :- fifth(h).
option(c) :- fifth(k).
option(d) :- fifth(m).
option(e) :- fifth(p).

#show option/1.
#show selected/1.
#show fifth/1.