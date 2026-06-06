% Base facts: movies and screens
movie(horror).
movie(mystery).
movie(romance).
movie(scifi).
movie(western).

screen(1).
screen(2).
screen(3).

% Time slots
% Screen 1 and 2 have two time slots: 7pm and 9pm
% Screen 3 has one time slot: 8pm
time(7).
time(8).
time(9).

% Assign each movie to a screen and a time slot
% We need to assign exactly one screen and one time to each movie
% Use choice rules to allow Clingo to assign screens and times
{ assigned_to_screen(M, S) : screen(S) } = 1 :- movie(M).
{ assigned_to_time(M, T) : time(T) } = 1 :- movie(M).

% Ensure that screen 3 has exactly one movie at 8pm
:- { assigned_to_screen(M, 3) : movie(M) } != 1.
:- { assigned_to_time(M, 8) : movie(M) } != 1.

% Ensure that screens 1 and 2 have exactly two movies each
:- { assigned_to_screen(M, 1) : movie(M) } != 2.
:- { assigned_to_screen(M, 2) : movie(M) } != 2.

% Ensure that the movie on screen 3 is at 8pm
:- assigned_to_screen(M, 3), not assigned_to_time(M, 8).

% The western begins at some time before the horror film does.
% This means the time of western is less than the time of horror
:- assigned_to_screen(western, S1), assigned_to_time(western, T1),
   assigned_to_screen(horror, S2), assigned_to_time(horror, T2),
   T1 >= T2.

% The sci-fi film is not shown on screen 3.
:- assigned_to_screen(scifi, 3).

% The romance is not shown on screen 2.
:- assigned_to_screen(romance, 2).

% The horror film and the mystery are shown on different screens.
:- assigned_to_screen(horror, S), assigned_to_screen(mystery, S).

% Additional constraint: If the romance is scheduled to begin before the western does,
% then derive the consequences.
% Romance begins before western: time(romance) < time(western)
:- assigned_to_time(romance, T_romance), assigned_to_time(western, T_western),
   T_romance >= T_western.

% --- Answer Mapping ---
% We need to check which of the options (A-E) must be true under the given constraints.

% (A) The horror film is shown on screen 1.
option(a) :- assigned_to_screen(horror, 1).

% (B) The mystery begins at 7 P.M.
option(b) :- assigned_to_time(mystery, 7).

% (C) The mystery is shown on screen 2.
option(c) :- assigned_to_screen(mystery, 2).

% (D) The sci-fi film begins at 9 P.M.
option(d) :- assigned_to_time(scifi, 9).

% (E) The sci-fi film is shown on screen 2.
option(e) :- assigned_to_screen(scifi, 2).

#show option/1.