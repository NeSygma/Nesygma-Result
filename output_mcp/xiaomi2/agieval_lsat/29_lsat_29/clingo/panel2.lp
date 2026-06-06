% Candidates and their types
botanist(f). botanist(g). botanist(h).
chemist(k). chemist(l). chemist(m).
zoologist(p). zoologist(q). zoologist(r).

% All candidates
candidate(X) :- botanist(X).
candidate(X) :- chemist(X).
candidate(X) :- zoologist(X).

% Select exactly 5 candidates
{ selected(X) : candidate(X) } 5.

% Premise: G and H are selected
selected(g).
selected(h).

% Constraint 1: At least one of each type
:- not 1 { selected(X) : botanist(X) }.
:- not 1 { selected(X) : chemist(X) }.
:- not 1 { selected(X) : zoologist(X) }.

% Constraint 2: If more than one botanist selected, then at most one zoologist selected.
botanist_count(N) :- N = #count { X : selected(X), botanist(X) }.
zoologist_count(N) :- N = #count { X : selected(X), zoologist(X) }.
:- botanist_count(N), N > 1, zoologist_count(M), M > 1.

% Constraint 3: F and K cannot both be selected.
:- selected(f), selected(k).

% Constraint 4: K and M cannot both be selected.
:- selected(k), selected(m).

% Constraint 5: If M is selected, then both P and R must be selected.
:- selected(m), not selected(p).
:- selected(m), not selected(r).

% Check each option's satisfaction
satisfied(a) :- selected(f).
satisfied(a) :- selected(k).
satisfied(b) :- selected(f).
satisfied(b) :- selected(m).
satisfied(c) :- selected(k).
satisfied(c) :- selected(m).
satisfied(d) :- selected(m).
satisfied(d) :- selected(q).
satisfied(e) :- selected(p).
satisfied(e) :- selected(q).

% For each option, check if it's violated in this model
violated(Option) :- option(Option), not satisfied(Option).

option(a). option(b). option(c). option(d). option(e).

% Show which options are violated in each model
#show violated/1.
#show selected/1.