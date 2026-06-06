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

% Screen 2 movies at each time
s2_7pm(M) :- assign(M, 2, 7).
s2_9pm(M) :- assign(M, 2, 9).

% Check each option
matches_a :- s2_7pm(scifi), s2_9pm(horror).
matches_b :- s2_7pm(scifi), s2_9pm(mystery).
matches_c :- s2_7pm(scifi), s2_9pm(western).
matches_d :- s2_7pm(western), s2_9pm(horror).
matches_e :- s2_7pm(western), s2_9pm(mystery).

#show assign/3.
#show matches_a.
#show matches_b.
#show matches_c.
#show matches_d.
#show matches_e.