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

% Given condition: P is the ONLY zoologist selected
:- selected(p), selected(q).
:- selected(p), selected(r).
:- not selected(p).
:- zoologist(Z), selected(Z), Z != p.

% Now check each option with explicit constraints

% Option A: If K is selected, G cannot be selected.
% Counterexample: K and G are both selected
:- not option_a_correct.
option_a_correct :- not (selected(k), selected(g)).

% Option B: If L is selected, F cannot be selected.
% Counterexample: L and F are both selected
:- not option_b_correct.
option_b_correct :- not (selected(l), selected(f)).

% Option C: If exactly one chemist is selected, it must be K.
% Counterexample: exactly one chemist, not K
:- not option_c_correct.
exactly_one_chemist :- #count{C : chemist(C), selected(C)} = 1.
option_c_correct :- not (exactly_one_chemist, not selected(k)).

% Option D: If exactly two chemists are selected, F cannot be selected.
% Counterexample: exactly two chemists, F selected
:- not option_d_correct.
exactly_two_chemists :- #count{C : chemist(C), selected(C)} = 2.
option_d_correct :- not (exactly_two_chemists, selected(f)).

% Option E: If exactly two chemists are selected, G cannot be selected.
% Counterexample: exactly two chemists, G selected
:- not option_e_correct.
option_e_correct :- not (exactly_two_chemists, selected(g)).

% Show which options are correct
#show selected/1.
#show option_a_correct/0.
#show option_b_correct/0.
#show option_c_correct/0.
#show option_d_correct/0.
#show option_e_correct/0.