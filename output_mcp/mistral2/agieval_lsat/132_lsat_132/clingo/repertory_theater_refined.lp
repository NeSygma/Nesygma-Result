% Repertory Theater Scheduling Problem

% Define the movies and screens
movie(horror; mystery; romance; scifi; western).
screen(1; 2; 3).

% Time slots: 7pm, 8pm, 9pm
time(7; 8; 9).

% Assign each movie to a screen and a time slot
% Each movie is shown exactly once
1 { assigned(M, S, T) : screen(S), time(T) } 1 :- movie(M).

% Screen 3 can only show one movie at 8pm
:- assigned(M1, 3, 8), assigned(M2, 3, 8), M1 != M2.

% Each screen must have the correct number of movies
% Screen 1 and 2: 2 movies each
% Screen 3: 1 movie
count_screen_movies(S, N) :- N = #count { M : assigned(M, S, _) }, screen(S).
:- screen(S), S != 3, count_screen_movies(S, N), N != 2.
:- screen(3), count_screen_movies(3, N), N != 1.

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

% Define the options for screen 1
% Option A: sci-fi at 7pm, horror at 9pm
option(a) :-
    assigned(scifi, 1, 7),
    assigned(horror, 1, 9).

% Option B: sci-fi at 7pm, mystery at 9pm
option(b) :-
    assigned(scifi, 1, 7),
    assigned(mystery, 1, 9).

% Option C: western at 7pm, horror at 9pm
option(c) :-
    assigned(western, 1, 7),
    assigned(horror, 1, 9).

% Option D: western at 7pm, mystery at 9pm
option(d) :-
    assigned(western, 1, 7),
    assigned(mystery, 1, 9).

% Option E: western at 7pm, sci-fi at 9pm
option(e) :-
    assigned(western, 1, 7),
    assigned(scifi, 1, 9).

#show option/1.