% Define all scientists
scientist(f). scientist(g). scientist(h).
scientist(k). scientist(l). scientist(m).
scientist(p). scientist(q). scientist(r).

% Define types
botanist(f). botanist(g). botanist(h).
chemist(k). chemist(l). chemist(m).
zoologist(p). zoologist(q). zoologist(r).

% Exactly five scientists must be selected
5 { selected(S) : scientist(S) } 5.

% The four given scientists must be selected
selected(f). selected(l). selected(q). selected(r).

% Constraints
% At least one of each type
:- not selected(S1), botanist(S1).
:- not selected(S1), chemist(S1).
:- not selected(S1), zoologist(S1).

% If more than one botanist selected, then at most one zoologist
:- selected(S1), selected(S2), botanist(S1), botanist(S2), S1 != S2,
   selected(S3), selected(S4), zoologist(S3), zoologist(S4), S3 != S4.

% F and K cannot both be selected
:- selected(f), selected(k).

% K and M cannot both be selected
:- selected(k), selected(m).

% If M is selected, both P and R must be selected
:- selected(m), not selected(p).
:- selected(m), not selected(r).

% Map the correct answer to option/1 (MANDATORY)
option(a) :- selected(g).
option(b) :- selected(h).
option(c) :- selected(k).
option(d) :- selected(m).
option(e) :- selected(p).

#show option/1.