% Define the types of scientists
botanist(f). botanist(g). botanist(h).
chemist(k). chemist(l). chemist(m).
zoologist(p). zoologist(q). zoologist(r).

% Define the panel size
panel_size(5).

% Define the selected scientists for each option
% Option A: F, G, K, P, Q
selected(f) :- option(a).
selected(g) :- option(a).
selected(k) :- option(a).
selected(p) :- option(a).
selected(q) :- option(a).

% Option B: G, H, K, L, M
selected(g) :- option(b).
selected(h) :- option(b).
selected(k) :- option(b).
selected(l) :- option(b).
selected(m) :- option(b).

% Option C: G, H, K, L, R
selected(g) :- option(c).
selected(h) :- option(c).
selected(k) :- option(c).
selected(l) :- option(c).
selected(r) :- option(c).

% Option D: H, K, M, P, R
selected(h) :- option(d).
selected(k) :- option(d).
selected(m) :- option(d).
selected(p) :- option(d).
selected(r) :- option(d).

% Option E: H, L, M, P, Q
selected(h) :- option(e).
selected(l) :- option(e).
selected(m) :- option(e).
selected(p) :- option(e).
selected(q) :- option(e).

% Ensure exactly 5 scientists are selected
:- panel_size(N), {selected(X)} != N.

% At least one of each type must be selected
:- not selected_botanist.
selected_botanist :- selected(X), botanist(X).
:- not selected_chemist.
selected_chemist :- selected(X), chemist(X).
:- not selected_zoologist.
selected_zoologist :- selected(X), zoologist(X).

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
% Option A: F, G, K, P, Q
% Botanists: F, G (2)
% Chemists: K (1)
% Zoologists: P, Q (2)
% Constraints: More than one botanist -> at most one zoologist, but here 2 zoologists -> invalid
option(a) :- option(a),
             selected(f), selected(g), selected(k), selected(p), selected(q),
             selected_botanist, selected_chemist, selected_zoologist,
             {selected(X) : botanist(X)} = 2, {selected(X) : chemist(X)} = 1, {selected(X) : zoologist(X)} = 2.

% Option B: G, H, K, L, M
% Botanists: G, H (2)
% Chemists: K, L, M (3) -> violates panel size of 5
option(b) :- option(b),
             selected(g), selected(h), selected(k), selected(l), selected(m),
             selected_botanist, selected_chemist, selected_zoologist,
             {selected(X) : botanist(X)} = 2, {selected(X) : chemist(X)} = 3, {selected(X) : zoologist(X)} = 0.

% Option C: G, H, K, L, R
% Botanists: G, H (2)
% Chemists: K, L (2)
% Zoologists: R (1)
% Constraints: More than one botanist -> at most one zoologist (satisfied)
% F and K not both selected (satisfied, F not selected)
% K and M not both selected (satisfied, M not selected)
% M not selected, so no need to check P and R
option(c) :- option(c),
             selected(g), selected(h), selected(k), selected(l), selected(r),
             selected_botanist, selected_chemist, selected_zoologist,
             {selected(X) : botanist(X)} = 2, {selected(X) : chemist(X)} = 2, {selected(X) : zoologist(X)} = 1,
             {selected(X) : botanist(X)} > 1, {selected(X) : zoologist(X)} = 1.

% Option D: H, K, M, P, R
% Botanists: H (1)
% Chemists: K, M (2)
% Zoologists: P, R (2)
% Constraints: Only one botanist -> no restriction on zoologists
% F and K not both selected (satisfied, F not selected)
% K and M both selected -> violates constraint
option(d) :- option(d),
             selected(h), selected(k), selected(m), selected(p), selected(r),
             selected_botanist, selected_chemist, selected_zoologist,
             {selected(X) : botanist(X)} = 1, {selected(X) : chemist(X)} = 2, {selected(X) : zoologist(X)} = 2,
             selected(k), selected(m).

% Option E: H, L, M, P, Q
% Botanists: H (1)
% Chemists: L, M (2)
% Zoologists: P, Q (2)
% Constraints: Only one botanist -> no restriction on zoologists
% F and K not both selected (satisfied, F not selected)
% K and M not both selected (satisfied, K not selected)
% M selected -> P and R must be selected, but R is not selected -> violates constraint
option(e) :- option(e),
             selected(h), selected(l), selected(m), selected(p), selected(q),
             selected_botanist, selected_chemist, selected_zoologist,
             {selected(X) : botanist(X)} = 1, {selected(X) : chemist(X)} = 2, {selected(X) : zoologist(X)} = 2,
             selected(m), not selected(r).

% Final mapping of the correct option
option(a) :- selected(f), selected(g), selected(k), selected(p), selected(q),
             selected_botanist, selected_chemist, selected_zoologist,
             {selected(X) : botanist(X)} = 2, {selected(X) : chemist(X)} = 1, {selected(X) : zoologist(X)} = 2,
             {selected(X) : botanist(X)} > 1, {selected(X) : zoologist(X)} > 1.

option(b) :- selected(g), selected(h), selected(k), selected(l), selected(m),
             selected_botanist, selected_chemist, selected_zoologist,
             {selected(X) : botanist(X)} = 2, {selected(X) : chemist(X)} = 3, {selected(X) : zoologist(X)} = 0.

option(c) :- selected(g), selected(h), selected(k), selected(l), selected(r),
             selected_botanist, selected_chemist, selected_zoologist,
             {selected(X) : botanist(X)} = 2, {selected(X) : chemist(X)} = 2, {selected(X) : zoologist(X)} = 1,
             {selected(X) : botanist(X)} > 1, {selected(X) : zoologist(X)} = 1,
             not selected(f), not selected(k), not selected(m).

option(d) :- selected(h), selected(k), selected(m), selected(p), selected(r),
             selected_botanist, selected_chemist, selected_zoologist,
             {selected(X) : botanist(X)} = 1, {selected(X) : chemist(X)} = 2, {selected(X) : zoologist(X)} = 2,
             selected(k), selected(m).

option(e) :- selected(h), selected(l), selected(m), selected(p), selected(q),
             selected_botanist, selected_chemist, selected_zoologist,
             {selected(X) : botanist(X)} = 1, {selected(X) : chemist(X)} = 2, {selected(X) : zoologist(X)} = 2,
             selected(m), not selected(r).

#show option/1.