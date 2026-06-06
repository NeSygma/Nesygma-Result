% Define the scientists and their types
scientist(f; g; h; k; l; m; p; q; r).

% Types: botanist, chemist, zoologist
type(f, botanist). type(g, botanist). type(h, botanist).
type(k, chemist). type(l, chemist). type(m, chemist).
type(p, zoologist). type(q, zoologist). type(r, zoologist).

% Panel size constraint
panel_size(5).

% At least one scientist of each type must be selected
:- not 1 { S : selected(S), type(S, botanist) } 1.
:- not 1 { S : selected(S), type(S, zoologist) } 1.
:- not 1 { S : selected(S), type(S, chemist) } 1.

% If more than one botanist is selected, then at most one zoologist is selected
:- { S : selected(S), type(S, botanist) } > 1, { S : selected(S), type(S, zoologist) } > 1.

% F and K cannot both be selected
:- selected(f), selected(k).

% K and M cannot both be selected
:- selected(k), selected(m).

% If M is selected, both P and R must be selected
:- selected(m), not selected(p).
:- selected(m), not selected(r).

% Given: Four of the scientists selected are F, L, Q, and R
selected(f). selected(l). selected(q). selected(r).

% Panel size constraint: exactly 5 scientists
1 { selected(S) : scientist(S) } 5.

% Ensure the panel includes exactly the given four plus one more
:- { selected(S) : scientist(S) } != 5.
:- not 4 { selected(f); selected(l); selected(q); selected(r) } 4.

% Define the possible fifth scientist
% The fifth scientist must be one of: g, h, k, m, p

% Option A: G
option(a) :- selected(g).

% Option B: H
option(b) :- selected(h).

% Option C: K
option(c) :- selected(k).

% Option D: M
option(d) :- selected(m).

% Option E: P
option(e) :- selected(p).

#show option/1.