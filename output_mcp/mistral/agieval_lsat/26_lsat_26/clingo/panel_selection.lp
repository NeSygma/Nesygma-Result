% Domain
botanist(f; g; h).
chemist(k; l; m).
zoologist(p; q; r).

% Panel size
panel_size(5).

% Selection (choice rule for who is selected)
{ selected(X) : botanist(X) }.
{ selected(X) : chemist(X) }.
{ selected(X) : zoologist(X) }.

% Counts
num_botanist(N) :- N = #count { B : botanist(B), selected(B) }.
num_chemist(N) :- N = #count { C : chemist(C), selected(C) }.
num_zoologist(N) :- N = #count { Z : zoologist(Z), selected(Z) }.

% At least one of each type
:- num_botanist(0).
:- num_chemist(0).
:- num_zoologist(0).

% If more than one botanist, then at most one zoologist
:- num_botanist(N), N > 1, num_zoologist(M), M > 1.

% F and K cannot both be selected
:- selected(f), selected(k).

% K and M cannot both be selected
:- selected(k), selected(m).

% If M is selected, both P and R must be selected
:- selected(m), not selected(p).
:- selected(m), not selected(r).

% Question constraint: M is the only chemist selected
:- chemist(C), C != m, selected(C).  % No other chemist is selected
:- chemist(m), not selected(m).       % M is selected

% Panel size constraint
:- #count { X : selected(X) } != 5.

% Map answer choices
% (A) F and G are both selected
option(a) :- selected(f), selected(g).

% (B) G and H are both selected
option(b) :- selected(g), selected(h).

% (C) H and P are both selected
option(c) :- selected(h), selected(p).

% (D) F, G, and H are all selected
option(d) :- selected(f), selected(g), selected(h).

% (E) P, Q, and R are all selected
option(e) :- selected(p), selected(q), selected(r).

#show option/1.