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

#show assign/3.