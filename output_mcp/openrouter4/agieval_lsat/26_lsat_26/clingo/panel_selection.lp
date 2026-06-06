%%% Panel Selection Problem %%%
% Scientists
botanist(f). botanist(g). botanist(h).
chemist(k). chemist(l). chemist(m).
zoologist(p). zoologist(q). zoologist(r).

scientist(X) :- botanist(X).
scientist(X) :- chemist(X).
scientist(X) :- zoologist(X).

% The panel consists of exactly 5 scientists
{ selected(X) : scientist(X) } = 5.

% Condition 1: At least one of each type
1 { selected(X) : botanist(X) } 1 :- true.
1 { selected(X) : chemist(X) } 1 :- true.
1 { selected(X) : zoologist(X) } 1 :- true.

% Condition 2: If more than one botanist is selected, then at most one zoologist is selected
% Let bot_count = N. If N > 1, then zoo_count <= 1.
% Equivalently: cannot have >1 botanist AND >1 zoologist.
bot_count(N) :- N = #count { B : botanist(B), selected(B) }.
zoo_count(N) :- N = #count { Z : zoologist(Z), selected(Z) }.
:- bot_count(B), zoo_count(Z), B > 1, Z > 1.

% Condition 3: F and K cannot both be selected
:- selected(f), selected(k).

% Condition 4: K and M cannot both be selected
:- selected(k), selected(m).

% Condition 5: If M is selected, both P and R must be selected
:- selected(m), not selected(p).
:- selected(m), not selected(r).

% The given condition for this question: M is the only chemist selected
selected(m).  % M is selected
:- selected(X), chemist(X), X != m, selected(X).  % No other chemist is selected

% Now we derive which option must be true
% Option (A): F and G are both selected
option_a :- selected(f), selected(g).

% Option (B): G and H are both selected
option_b :- selected(g), selected(h).

% Option (C): H and P are both selected
option_c :- selected(h), selected(p).

% Option (D): F, G, and H are all selected
option_d :- selected(f), selected(g), selected(h).

% Option (E): P, Q, and R are all selected
option_e :- selected(p), selected(q), selected(r).

% The correct answer is the one that must be true in ALL possible models.
% We check this by seeing if the negation of an option is consistent with the constraints.
% If (not option) is UNSAT, then option is necessarily true.
% So we will generate all valid models and verify.

% For each option, we check if it's forced:
% Show the option that holds in all models (by checking forced conditions)
% Actually, let's just generate all models and inspect.

#show selected/1.
#show option_a/0.
#show option_b/0.
#show option_c/0.
#show option_d/0.
#show option_e/0.