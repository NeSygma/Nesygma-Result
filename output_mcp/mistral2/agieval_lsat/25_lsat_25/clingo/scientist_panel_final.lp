% Define the types of scientists
botanist(f). botanist(g). botanist(h).
chemist(k). chemist(l). chemist(m).
zoologist(p). zoologist(q). zoologist(r).

% Define the selected scientists for each option as facts
% Option A: F, G, K, P, Q
selected_option_a(f). selected_option_a(g). selected_option_a(k). selected_option_a(p). selected_option_a(q).
% Option B: G, H, K, L, M
selected_option_b(g). selected_option_b(h). selected_option_b(k). selected_option_b(l). selected_option_b(m).
% Option C: G, H, K, L, R
selected_option_c(g). selected_option_c(h). selected_option_c(k). selected_option_c(l). selected_option_c(r).
% Option D: H, K, M, P, R
selected_option_d(h). selected_option_d(k). selected_option_d(m). selected_option_d(p). selected_option_d(r).
% Option E: H, L, M, P, Q
selected_option_e(h). selected_option_e(l). selected_option_e(m). selected_option_e(p). selected_option_e(q).

% Define a predicate to represent the selected scientists for the panel
selected(X) :- selected_option_a(X).
selected(X) :- selected_option_b(X).
selected(X) :- selected_option_c(X).
selected(X) :- selected_option_d(X).
selected(X) :- selected_option_e(X).

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

% Map the correct answer to option/1
% Option A is invalid (2 botanists and 2 zoologists)
option(a) :- selected_option_a(f), selected_option_a(g), selected_option_a(k), selected_option_a(p), selected_option_a(q),
             {selected_option_a(X) : botanist(X)} = 2, {selected_option_a(X) : zoologist(X)} = 2.

% Option B is invalid (no zoologists)
option(b) :- selected_option_b(g), selected_option_b(h), selected_option_b(k), selected_option_b(l), selected_option_b(m),
             {selected_option_b(X) : zoologist(X)} = 0.

% Option C is valid
option(c) :- selected_option_c(g), selected_option_c(h), selected_option_c(k), selected_option_c(l), selected_option_c(r),
             {selected_option_c(X) : botanist(X)} = 2, {selected_option_c(X) : chemist(X)} = 2, {selected_option_c(X) : zoologist(X)} = 1.

% Option D is invalid (K and M both selected)
option(d) :- selected_option_d(h), selected_option_d(k), selected_option_d(m), selected_option_d(p), selected_option_d(r),
             selected(k), selected(m).

% Option E is invalid (M selected but R not selected)
option(e) :- selected_option_e(h), selected_option_e(l), selected_option_e(m), selected_option_e(p), selected_option_e(q),
             selected(m), not selected(r).

% Ensure only one option is valid
:- option(A), option(B), A != B.
:- option(A), option(C), A != C.
:- option(A), option(D), A != D.
:- option(A), option(E), A != E.
:- option(B), option(C), B != C.
:- option(B), option(D), B != D.
:- option(B), option(E), B != E.
:- option(C), option(D), C != D.
:- option(C), option(E), C != E.
:- option(D), option(E), D != E.

#show option/1.