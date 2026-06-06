% Define the scientists and their types
scientist(f; g; h; k; l; m; p; q; r).

% Types: botanist, chemist, zoologist
type(f, botanist). type(g, botanist). type(h, botanist).
type(k, chemist). type(l, chemist). type(m, chemist).
type(p, zoologist). type(q, zoologist). type(r, zoologist).

% Panel size
panel_size(5).

% Selection predicate: selected(S) means scientist S is selected
{ selected(S) : scientist(S) }.

% At least one scientist of each type
:- not 1 { selected(S) : type(S, botanist) } 1.
:- not 1 { selected(S) : type(S, chemist) } 1.
:- not 1 { selected(S) : type(S, zoologist) } 1.

% If more than one botanist is selected, then at most one zoologist is selected
num_botanists(N) :- N = #count { S : selected(S), type(S, botanist) }.
num_zoologists(M) :- M = #count { S : selected(S), type(S, zoologist) }.
:- num_botanists(N), N > 1, num_zoologists(M), M > 1.

% F and K cannot both be selected
:- selected(f), selected(k).

% K and M cannot both be selected
:- selected(k), selected(m).

% If M is selected, both P and R must be selected
:- selected(m), not selected(p).
:- selected(m), not selected(r).

% P is the only zoologist selected
:- selected(p), not selected(q), not selected(r).
:- not selected(p), num_zoologists(1).
:- selected(q).
:- selected(r).

% Helper predicates for the options
selected_chemist(k) :- selected(k).
selected_chemist(l) :- selected(l).
selected_chemist(m) :- selected(m).

num_chemists(N) :- N = #count { S : selected(S), type(S, chemist) }.

% Define conditions for each option
% Option A: If K is selected, G cannot be selected
condition_a :- selected(k), not selected(g).

% Option B: If L is selected, F cannot be selected
condition_b :- selected(l), not selected(f).

% Option C: If exactly one chemist is selected, it must be K
condition_c :- num_chemists(1), selected(k).

% Option D: If exactly two chemists are selected, F cannot be selected
condition_d :- num_chemists(2), not selected(f).

% Option E: If exactly two chemists are selected, G cannot be selected
condition_e :- num_chemists(2), not selected(g).

% Ensure only one option is true
:- condition_a, condition_b.
:- condition_a, condition_c.
:- condition_a, condition_d.
:- condition_a, condition_e.
:- condition_b, condition_c.
:- condition_b, condition_d.
:- condition_b, condition_e.
:- condition_c, condition_d.
:- condition_c, condition_e.
:- condition_d, condition_e.

% Map the correct answer to option/1 (MANDATORY)
option(a) :- condition_a.
option(b) :- condition_b.
option(c) :- condition_c.
option(d) :- condition_d.
option(e) :- condition_e.

#show option/1.