% Scientists
scientist(f; g; h; k; l; m; p; q; r).

% Types
botanist(f; g; h).
chemist(k; l; m).
zoologist(p; q; r).

% Selection: each scientist is either selected or not
{ selected(X) } :- scientist(X).

% At least one of each type
:- not selected(X) : botanist(X).
:- not selected(X) : chemist(X).
:- not selected(X) : zoologist(X).

% If more than one botanist selected, then at most one zoologist selected
% More than one botanist: count botanists > 1
more_than_one_botanist :- #count{ B : botanist(B), selected(B) } > 1.
:- more_than_one_botanist, #count{ Z : zoologist(Z), selected(Z) } > 1.

% F and K cannot both be selected
:- selected(f), selected(k).

% K and M cannot both be selected
:- selected(k), selected(m).

% If M is selected, both P and R must be selected
:- selected(m), not selected(p).
:- selected(m), not selected(r).

% Exactly 5 panelists
:- #count{ X : selected(X) } != 5.

% Condition: both G and H are selected
:- not selected(g).
:- not selected(h).

% Now evaluate the answer choices.
% The question: "If both G and H are among the scientists selected, then the panel must include either ..."
% This means: under the condition that G and H are selected, which pair (X or Y) is such that at least one of them MUST be selected?

% For each option, check if it's forced: i.e., in ALL valid models (with G and H selected), at least one of the two is selected.
% We can check this by seeing if there exists a model where NEITHER is selected (which would violate the "must include" claim).
% So we test each option by adding a constraint that NEITHER is selected, and see if it's UNSAT (meaning the option is forced).

% We'll encode this by checking each option individually.

% Option A: F or else K
% Check if it's possible to have neither F nor K selected
possible_no_fk :- not selected(f), not selected(k).

% Option B: F or else M
possible_no_fm :- not selected(f), not selected(m).

% Option C: K or else M
possible_no_km :- not selected(k), not selected(m).

% Option D: M or else Q
possible_no_mq :- not selected(m), not selected(q).

% Option E: P or else Q
possible_no_pq :- not selected(p), not selected(q).

% To determine which option is forced, we need to see which ones CANNOT have both absent.
% We'll use a choice rule to explore all possibilities, then derive which options are forced.

% Let's just enumerate all valid selections and check which options always hold.
% We'll use a helper to check each option.

% For each option, we say the option is "satisfied" if at least one of its two is selected.
option_a_satisfied :- selected(f).
option_a_satisfied :- selected(k).

option_b_satisfied :- selected(f).
option_b_satisfied :- selected(m).

option_c_satisfied :- selected(k).
option_c_satisfied :- selected(m).

option_d_satisfied :- selected(m).
option_d_satisfied :- selected(q).

option_e_satisfied :- selected(p).
option_e_satisfied :- selected(q).

% Now, we want to find if there exists a model where an option is NOT satisfied.
% We'll use a "check" predicate that is true if we find a counterexample.
% Since we can't directly check across models in ASP, we'll use a different approach:
% We'll add constraints to test each option individually.

% Actually, let's use a simpler approach: we'll generate all valid selections and
% use #show to see which options are always satisfied.

% Let's just run the model and see what selections are possible.
% We'll show the selected scientists and which options are satisfied.

#show selected/1.
#show option_a_satisfied/0.
#show option_b_satisfied/0.
#show option_c_satisfied/0.
#show option_d_satisfied/0.
#show option_e_satisfied/0.