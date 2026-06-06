% Domain definitions
movie(horror; mystery; romance; scifi; western).
screen(1; 2; 3).
time(7; 8; 9).

% Each movie is shown exactly once, on one screen at one time
1 { showing(M, S, T) : screen(S), time(T) } 1 :- movie(M).

% Screen 1 shows exactly 2 movies: one at 7 and one at 9
:- #count { M : showing(M, 1, 7) } != 1.
:- #count { M : showing(M, 1, 9) } != 1.

% Screen 2 shows exactly 2 movies: one at 7 and one at 9
:- #count { M : showing(M, 2, 7) } != 1.
:- #count { M : showing(M, 2, 9) } != 1.

% Screen 3 shows exactly 1 movie at 8
:- #count { M : showing(M, 3, 8) } != 1.

% No other showings on screen 3
:- showing(M, 3, T), T != 8.

% No showings at 8 on screens 1 or 2
:- showing(M, S, 8), S != 3.

% No showings at 7 or 9 on screen 3
:- showing(M, 3, T), T != 8.

% The western begins at some time before the horror film does.
:- showing(western, _, Tw), showing(horror, _, Th), Tw >= Th.

% The sci-fi film is not shown on screen 3.
:- showing(scifi, 3, _).

% The romance is not shown on screen 2.
:- showing(romance, 2, _).

% The horror film and the mystery are shown on different screens.
:- showing(horror, S1, _), showing(mystery, S2, _), S1 = S2.

% --- Now evaluate each option ---
% Each option lists two movies for screen 1: 7PM first, then 9PM.

% Option A: scifi at 7, horror at 9 on screen 1
option_a_possible :- showing(scifi, 1, 7), showing(horror, 1, 9).

% Option B: scifi at 7, mystery at 9 on screen 1
option_b_possible :- showing(scifi, 1, 7), showing(mystery, 1, 9).

% Option C: western at 7, horror at 9 on screen 1
option_c_possible :- showing(western, 1, 7), showing(horror, 1, 9).

% Option D: western at 7, mystery at 9 on screen 1
option_d_possible :- showing(western, 1, 7), showing(mystery, 1, 9).

% Option E: western at 7, scifi at 9 on screen 1
option_e_possible :- showing(western, 1, 7), showing(scifi, 1, 9).

% The answer is the option that CANNOT be possible
option(a) :- not option_a_possible.
option(b) :- not option_b_possible.
option(c) :- not option_c_possible.
option(d) :- not option_d_possible.
option(e) :- not option_e_possible.

% Ensure exactly one option is derived
:- #count { O : option(O) } != 1.

#show option/1.