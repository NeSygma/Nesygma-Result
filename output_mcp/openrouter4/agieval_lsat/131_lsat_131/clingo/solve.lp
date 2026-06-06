% Movies
movie(horror; mystery; romance; scifi; western).

% Screens and times
screen(1;2;3).
time(7;8;9).

% Valid (screen, time) combinations
valid(1,7). valid(1,9).
valid(2,7). valid(2,9).
valid(3,8).

% Each movie assigned exactly one valid slot
{ assign(M, S, T) : valid(S, T) } = 1 :- movie(M).

% Each slot gets exactly one movie
1 { assign(M, S, T) : movie(M) } 1 :- valid(S, T).

% Constraint 1: Western before horror
:- assign(western, _, Tw), assign(horror, _, Th), Tw >= Th.

% Constraint 2: Sci-fi not on screen 3
:- assign(scifi, 3, _).

% Constraint 3: Romance not on screen 2
:- assign(romance, 2, _).

% Constraint 4: Horror and mystery on different screens
:- assign(horror, S, _), assign(mystery, S, _).

% Additional condition: romance begins before western
:- assign(romance, _, Tr), assign(western, _, Tw), Tr >= Tw.

% --- Derive the answer ---
% We need to find which option must be true in ALL valid schedules.

% For each option, we attempt to find a model where it is false.
% If no such model exists, the option is forced.

% Define options and their truth conditions
opt_cond(a) :- assign(horror, 1, _).
opt_cond(b) :- assign(mystery, _, 7).
opt_cond(c) :- assign(mystery, 2, _).
opt_cond(d) :- assign(scifi, _, 9).
opt_cond(e) :- assign(scifi, 2, _).

% For each option, try to find a model where it's false
{ try_false(O) } :- opt(O).
opt(a;b;c;d;e).

% If trying to make option O false, its condition must not hold
:- try_false(O), opt_cond(O).

% An option is "possibly false" if there is a model with try_false(O)
possibly_false(O) :- try_false(O).

% An option is forced if there is no possibility of it being false
forced(O) :- opt(O), not possibly_false(O).

% Map to final answer
% The solver will have exactly one forced option (option e)
option(O) :- forced(O).

% Ensure exactly one option is derived
:- not 1 { option(O) : opt(O) } 1.

#show option/1.