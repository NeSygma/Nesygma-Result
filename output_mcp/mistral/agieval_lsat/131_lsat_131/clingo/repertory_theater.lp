% Domains
movie(horror; mystery; romance; sci_fi; western).
screen(1; 2; 3).
time(7; 8; 9).

% Each movie assigned to exactly one screen and time
1 { assigned(M, S, T) : screen(S), time(T) } 1 :- movie(M).

% Screen capacity constraints
:- screen(S), S != 3, #count { M,T : assigned(M,S,T) } != 2.
:- screen(S), S = 3, #count { M,T : assigned(M,S,T) } != 1.

% Screen 3 only at 8pm
:- assigned(M, 3, T), T != 8.

% Screens 1 and 2 have exactly one movie at 7pm and one at 9pm
:- screen(S), S != 3, #count { M : assigned(M,S,7) } != 1.
:- screen(S), S != 3, #count { M : assigned(M,S,9) } != 1.

% Constraints from problem
% Western begins before horror
western_before_horror :- assigned(western, _, T1), assigned(horror, _, T2), T1 < T2.
:- not western_before_horror.

% Sci-fi not on screen 3
:- assigned(sci_fi, 3, _).

% Romance not on screen 2
:- assigned(romance, 2, _).

% Horror and mystery on different screens
:- assigned(horror, S1, _), assigned(mystery, S2, _), S1 = S2.

% Given condition: romance begins before western
romance_before_western :- assigned(romance, _, T1), assigned(western, _, T2), T1 < T2.
:- not romance_before_western.

% Map the correct answer to option/1
option(a) :- assigned(horror, 1, _).
option(b) :- assigned(mystery, _, 7).
option(c) :- assigned(mystery, 2, _).
option(d) :- assigned(sci_fi, _, 9).
option(e) :- assigned(sci_fi, 2, _).

#show option/1.