% Domains and basic facts
movie(horror; mystery; romance; scifi; western).
screen(1; 2; 3).
time(7; 8; 9).

% Each movie is shown exactly once on one screen at one time
1 { showing(M, S, T) : screen(S), time(T) } 1 :- movie(M).

% Screen 1 and 2 show two movies each, screen 3 shows one movie
:- screen(S), S != 3, #count { M : showing(M, S, _) } != 2.
:- screen(3), #count { M : showing(M, 3, _) } != 1.

% Screen 3 shows exactly one movie at 8 P.M.
:- showing(M, 3, T), T != 8.

% The western begins at some time before the horror film does.
:- showing(western, _, T1), showing(horror, _, T2), T1 >= T2.

% The sci-fi film is not shown on screen 3.
:- showing(scifi, 3, _).

% The romance is not shown on screen 2.
:- showing(romance, 2, _).

% The horror film and the mystery are shown on different screens.
:- showing(horror, S1, _), showing(mystery, S2, _), S1 == S2.

% Helper predicates to extract screen and time assignments for each movie
assigned_screen(M, S) :- showing(M, S, _).
assigned_time(M, T) :- showing(M, S, T).

% Define the order of movies on each screen for screen 1 and 2
% Screen 1 and 2 have two movies: one at 7 and one at 9
movie_at_7(S, M) :- showing(M, S, 7), screen(S), S != 3.
movie_at_9(S, M) :- showing(M, S, 9), screen(S), S != 3.

% Define the condition for each option
% Option A: screen 2 has sci-fi at 7 and horror at 9
option(a) :- movie_at_7(2, scifi), movie_at_9(2, horror).

% Option B: screen 2 has sci-fi at 7 and mystery at 9
option(b) :- movie_at_7(2, scifi), movie_at_9(2, mystery).

% Option C: screen 2 has sci-fi at 7 and western at 9
option(c) :- movie_at_7(2, scifi), movie_at_9(2, western).

% Option D: screen 2 has western at 7 and horror at 9
option(d) :- movie_at_7(2, western), movie_at_9(2, horror).

% Option E: screen 2 has western at 7 and mystery at 9
option(e) :- movie_at_7(2, western), movie_at_9(2, mystery).

% Ensure only one option is correct
:- option(X), option(Y), X != Y.

% Sentinel atom to ensure at least one answer set is returned
solution_exists :- option(_).

#show option/1.
#show solution_exists/0.