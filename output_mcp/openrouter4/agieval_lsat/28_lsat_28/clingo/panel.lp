% Scientists
scientist(f; g; h; k; l; m; p; q; r).

% Types
botanist(f; g; h).
chemist(k; l; m).
zoologist(p; q; r).

% Selection choice
{selected(X)} :- scientist(X).

% Condition 1: At least one of each type
:- not selected(X) : botanist(X).
:- not selected(X) : chemist(X).
:- not selected(X) : zoologist(X).

% Condition 2: If more than one botanist selected, then at most one zoologist selected
more_than_one_botanist :- #count{X : botanist(X), selected(X)} > 1.
:- more_than_one_botanist, #count{Z : zoologist(Z), selected(Z)} > 1.

% Condition 3: F and K cannot both be selected
:- selected(f), selected(k).

% Condition 4: K and M cannot both be selected
:- selected(k), selected(m).

% Condition 5: If M is selected, both P and R must be selected
:- selected(m), not selected(p).
:- selected(m), not selected(r).

% Given condition for this question: P is the ONLY zoologist selected
:- selected(p), selected(q).
:- selected(p), selected(r).
:- not selected(p).
:- zoologist(Z), selected(Z), Z != p.

% Now let's evaluate each option

% Option A: If K is selected, G cannot be selected.
% Check if there exists a model where K is selected AND G is selected
counterexample_a :- selected(k), selected(g).

% Option B: If L is selected, F cannot be selected.
counterexample_b :- selected(l), selected(f).

% Option C: If exactly one chemist is selected, it must be K.
exactly_one_chemist :- #count{C : chemist(C), selected(C)} = 1.
counterexample_c :- exactly_one_chemist, not selected(k).

% Option D: If exactly two chemists are selected, F cannot be selected.
exactly_two_chemists :- #count{C : chemist(C), selected(C)} = 2.
counterexample_d :- exactly_two_chemists, selected(f).

% Option E: If exactly two chemists are selected, G cannot be selected.
counterexample_e :- exactly_two_chemists, selected(g).

% An option is "must be true" if NO counterexample exists. 
% But since we need to find the SINGLE correct answer among A-E,
% let's directly check which options have NO counterexample.

% Show what's selected and any counterexamples
#show selected/1.
#show counterexample_a/0.
#show counterexample_b/0.
#show counterexample_c/0.
#show counterexample_d/0.
#show counterexample_e/0.