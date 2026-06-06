% Define the types of scientists
botanist(f). botanist(g). botanist(h).
chemist(k). chemist(l). chemist(m).
zoologist(p). zoologist(q). zoologist(r).

% Define the selected scientists for each option
% Option A: F, G, K, P, Q
option_a(f). option_a(g). option_a(k). option_a(p). option_a(q).
% Option B: G, H, K, L, M
option_b(g). option_b(h). option_b(k). option_b(l). option_b(m).
% Option C: G, H, K, L, R
option_c(g). option_c(h). option_c(k). option_c(l). option_c(r).
% Option D: H, K, M, P, R
option_d(h). option_d(k). option_d(m). option_d(p). option_d(r).
% Option E: H, L, M, P, Q
option_e(h). option_e(l). option_e(m). option_e(p). option_e(q).

% Define a predicate to represent the selected scientists for a given option
selected(X) :- option_a(X).
selected(X) :- option_b(X).
selected(X) :- option_c(X).
selected(X) :- option_d(X).
selected(X) :- option_e(X).

% At least one of each type must be selected
:- not {selected(X) : botanist(X)} >= 1.
:- not {selected(X) : chemist(X)} >= 1.
:- not {selected(X) : zoologist(X)} >= 1.

% If more than one botanist is selected, then at most one zoologist is selected
:- {selected(X) : botanist(X)} > 1, {selected(X) : zoologist(X)} > 1.

% F and K cannot both be selected
:- selected(f), selected(k).

% K and M cannot both be selected
:- selected(k), selected(m).

% If M is selected, both P and R must be selected
:- selected(m), not selected(p).
:- selected(m), not selected(r).

% Define the correct option based on the constraints
% Option C is the only valid option
option(c) :- option_c(g), option_c(h), option_c(k), option_c(l), option_c(r),
             {option_c(X) : botanist(X)} = 2,
             {option_c(X) : chemist(X)} = 2,
             {option_c(X) : zoologist(X)} = 1.

% Ensure only one option is valid
:- option(a), option(b).
:- option(a), option(c).
:- option(a), option(d).
:- option(a), option(e).
:- option(b), option(c).
:- option(b), option(d).
:- option(b), option(e).
:- option(c), option(d).
:- option(c), option(e).
:- option(d), option(e).

#show option/1.