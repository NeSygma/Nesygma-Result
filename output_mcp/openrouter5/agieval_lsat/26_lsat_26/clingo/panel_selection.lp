% Scientists
scientist(f; g; h; k; l; m; p; q; r).

% Types
botanist(f; g; h).
chemist(k; l; m).
zoologist(p; q; r).

% Selection choice
{ selected(X) } :- scientist(X).

% At least one of each type
:- #count{ B : botanist(B), selected(B) } = 0.
:- #count{ C : chemist(C), selected(C) } = 0.
:- #count{ Z : zoologist(Z), selected(Z) } = 0.

% If more than one botanist selected, then at most one zoologist selected
more_than_one_botanist :- #count{ B : botanist(B), selected(B) } > 1.
:- more_than_one_botanist, #count{ Z : zoologist(Z), selected(Z) } > 1.

% F and K cannot both be selected
:- selected(f), selected(k).

% K and M cannot both be selected
:- selected(k), selected(m).

% If M is selected, both P and R must be selected
:- selected(m), not selected(p).
:- selected(m), not selected(r).

% Additional condition from the question: M is the only chemist selected
:- selected(k).  % K cannot be selected
:- selected(l).  % L cannot be selected
selected(m).     % M must be selected

% Now evaluate each option - we need to find what MUST be true
% So we check which options hold in ALL possible models

% First, let's see all models to determine what's forced
#show selected/1.