% Domains
movie(horror).
movie(mystery).
movie(romance).
movie(sci_fi).
movie(western).

screen(1).
screen(2).
screen(3).

time(7).
time(8).
time(9).

% Each movie is shown exactly once
1 { assigned(M,S,T) : screen(S), time(T) } 1 :- movie(M).

% Screen 3 shows exactly one movie at 8 P.M.
:- #count { M : assigned(M,3,8) } != 1.
:- assigned(M,3,T), T != 8.

% Screens 1 and 2 show two movies each (one at 7 P.M. and one at 9 P.M.)
:- screen(S), S != 3, #count { T : assigned(_,S,T) } != 2.
:- screen(S), S != 3, not assigned(_,S,7), not assigned(_,S,9).

% The western begins at some time before the horror film does
:- assigned(western,S1,T1), assigned(horror,S2,T2), T1 >= T2.

% The sci-fi film is not shown on screen 3
:- assigned(sci_fi,3,_).

% The romance is not shown on screen 2
:- assigned(romance,2,_).

% The horror film and the mystery are shown on different screens
:- assigned(horror,S,T1), assigned(mystery,S,T2).

% Additional condition: sci-fi and romance are on the same screen
:- assigned(sci_fi,S1,_), assigned(romance,S2,_), S1 != S2.

% Derive the necessary conditions for the options
% Option A: The western begins at 7 P.M.
option(a) :- assigned(western,_,7).

% Option B: The sci-fi film begins at 9 P.M.
option(b) :- assigned(sci_fi,_,9).

% Option C: The mystery begins at 8 P.M.
option(c) :- assigned(mystery,_,8).

% Option D: The romance begins at 9 P.M.
option(d) :- assigned(romance,_,9).

% Option E: The horror film begins at 8 P.M.
option(e) :- assigned(horror,_,8).

% Ensure only one option is true
:- option(X), option(Y), X != Y.

#show option/1.