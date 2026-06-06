% Define scientists and their types
scientist(f). scientist(g). scientist(h).
scientist(k). scientist(l). scientist(m).
scientist(p). scientist(q). scientist(r).

botanist(f). botanist(g). botanist(h).
chemist(k). chemist(l). chemist(m).
zoologist(p). zoologist(q). zoologist(r).

% Define the options explicitly
option(a) :- selected(f), selected(g), selected(k), selected(p), selected(q).
option(b) :- selected(g), selected(h), selected(k), selected(l), selected(m).
option(c) :- selected(g), selected(h), selected(k), selected(l), selected(r).
option(d) :- selected(h), selected(k), selected(m), selected(p), selected(r).
option(e) :- selected(h), selected(l), selected(m), selected(p), selected(q).

% Selection of exactly 5 scientists
1 { selected(S) : scientist(S) } 5.

% At least one of each type
:- not 1 { selected(B) : botanist(B) }.
:- not 1 { selected(C) : chemist(C) }.
:- not 1 { selected(Z) : zoologist(Z) }.

% More than one botanist implies at most one zoologist
num_botanists(N) :- N = #count { B : selected(B), botanist(B) }.
num_zoologists(M) :- M = #count { Z : selected(Z), zoologist(Z) }.
:- num_botanists(N), N > 1, num_zoologists(M), M > 1.

% Pairwise constraints
:- selected(f), selected(k).
:- selected(k), selected(m).
:- selected(m), not selected(p).
:- selected(m), not selected(r).

#show option/1.