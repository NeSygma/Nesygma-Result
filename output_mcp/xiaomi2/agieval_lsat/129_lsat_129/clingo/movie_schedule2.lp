% Domains
movie(horror). movie(mystery). movie(romance). movie(scifi). movie(western).

% 5 slots: (screen, time)
slot(1, 7). slot(1, 9). slot(2, 7). slot(2, 9). slot(3, 8).

% Assign each movie to exactly one slot
{ assign(M, S, T) : slot(S, T) } 1 :- movie(M).

% Each slot has at most one movie
:- assign(M1, S, T), assign(M2, S, T), M1 != M2.

% Constraint 1: Western begins before horror (western time < horror time)
:- assign(western, _, TW), assign(horror, _, TH), TW >= TH.

% Constraint 2: Sci-fi not on screen 3
:- assign(scifi, 3, _).

% Constraint 3: Romance not on screen 2
:- assign(romance, 2, _).

% Constraint 4: Horror and mystery on different screens
:- assign(horror, S, _), assign(mystery, S, _).

% For each option, check if it's achievable
% Option A: screen 2 has sci-fi at 7pm, horror at 9pm
test_a :- assign(scifi, 2, 7), assign(horror, 2, 9).

% Option B: screen 2 has sci-fi at 7pm, mystery at 9pm
test_b :- assign(scifi, 2, 7), assign(mystery, 2, 9).

% Option C: screen 2 has sci-fi at 7pm, western at 9pm
test_c :- assign(scifi, 2, 7), assign(western, 2, 9).

% Option D: screen 2 has western at 7pm, horror at 9pm
test_d :- assign(western, 2, 7), assign(horror, 2, 9).

% Option E: screen 2 has western at 7pm, mystery at 9pm
test_e :- assign(western, 2, 7), assign(mystery, 2, 9).

% We want to find which option is NEVER true in any valid schedule
% The answer is the option where test_X never appears
#show test_a.
#show test_b.
#show test_c.
#show test_d.
#show test_e.
#show assign/3.