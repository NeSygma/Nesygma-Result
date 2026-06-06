% Repertory Theater Scheduling Problem

% Define the movies and screens
movie(horror).
movie(mystery).
movie(romance).
movie(scifi).
movie(western).

screen(1).
screen(2).
screen(3).

% Time slots
% Screen 1: 7pm and 9pm
% Screen 2: 7pm and 9pm
% Screen 3: 8pm only

% Assign each movie to a screen and a time slot
% We represent assignments as: assigned(Movie, Screen, Time)
% Time: 7, 8, 9 (7pm, 8pm, 9pm)

% Choice rule: Assign each movie to a screen and a time slot
% Each movie is shown exactly once

% Screen 3 can only show one movie at 8pm
% Screen 1 and 2 can show movies at 7pm and 9pm

% Each movie is assigned to exactly one screen and one time slot
1 { assigned(M, S, T) : screen(S), T = 7..9 } 1 :- movie(M).

% Screen 3 can only show one movie at 8pm
:- assigned(M1, 3, 8), assigned(M2, 3, 8), M1 != M2.

% Each screen must have the correct number of movies
% Screen 1 and 2: 2 movies each
% Screen 3: 1 movie

% Count movies per screen
count_screen_movies(S, N) :- N = #count { M : assigned(M, S, _) }, screen(S).

:- screen(S), S != 3, count_screen_movies(S, N), N != 2.
:- screen(3), count_screen_movies(3, N), N != 1.

% Time slot constraints per screen
% Screen 1 and 2: two movies at 7pm and 9pm
% Screen 3: one movie at 8pm

% Ensure no two movies on the same screen at the same time
:- assigned(M1, S, T), assigned(M2, S, T), M1 != M2.

% Ensure screen 3 only has 8pm
:- assigned(M, 3, T), T != 8.

% Constraints from the problem statement

% 1. The western begins at some time before the horror film does.
% This means the time slot of western < time slot of horror
:- assigned(western, _, T1), assigned(horror, _, T2), T1 >= T2.

% 2. The sci-fi film is not shown on screen 3.
:- assigned(scifi, 3, _).

% 3. The romance is not shown on screen 2.
:- assigned(romance, 2, _).

% 4. The horror film and the mystery are shown on different screens.
:- assigned(horror, S1, _), assigned(mystery, S2, _), S1 = S2.

% Helper predicates for screen assignments at specific times
assigned_7pm(S, M) :- assigned(M, S, 7).
assigned_9pm(S, M) :- assigned(M, S, 9).

% Screen 1 has two movies: one at 7pm and one at 9pm
screen1_movies(M1, M2) :-
    assigned_7pm(1, M1),
    assigned_9pm(1, M2).

% Screen 2 has two movies: one at 7pm and one at 9pm
screen2_movies(M1, M2) :-
    assigned_7pm(2, M1),
    assigned_9pm(2, M2).

% Screen 3 has one movie at 8pm
screen3_movie(M) :- assigned(M, 3, 8).

% Define the options for screen 1
% Option A: sci-fi at 7pm, horror at 9pm
option(a) :-
    screen1_movies(scifi, horror).

% Option B: sci-fi at 7pm, mystery at 9pm
option(b) :-
    screen1_movies(scifi, mystery).

% Option C: western at 7pm, horror at 9pm
option(c) :-
    screen1_movies(western, horror).

% Option D: western at 7pm, mystery at 9pm
option(d) :-
    screen1_movies(western, mystery).

% Option E: western at 7pm, sci-fi at 9pm
option(e) :-
    screen1_movies(western, scifi).

#show option/1.