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

% Now let's check each option by seeing if it's forced in ALL models
% Option A: F and G are both selected
option_a_holds :- selected(f), selected(g).

% Option B: G and H are both selected
option_b_holds :- selected(g), selected(h).

% Option C: H and P are both selected
option_c_holds :- selected(h), selected(p).

% Option D: F, G, and H are all selected
option_d_holds :- selected(f), selected(g), selected(h).

% Option E: P, Q, and R are all selected
option_e_holds :- selected(p), selected(q), selected(r).

% To find what MUST be true, we need to check if an option holds in ALL models.
% We can use #show to see all models and manually check, or we can use
% a trick: add constraints that block the option and see if it's still satisfiable.

% Let's just enumerate all models and see which options are always true.
#show selected/1.
#show option_a_holds/0.
#show option_b_holds/0.
#show option_c_holds/0.
#show option_d_holds/0.
#show option_e_holds/0.