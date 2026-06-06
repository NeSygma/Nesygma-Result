% Domain: movies
movie(horror). movie(mystery). movie(romance). movie(scifi). movie(western).

% Domain: screens
screen(1). screen(2). screen(3).

% Domain: times
time(7). time(8). time(9).

% Each movie gets exactly one (screen, time) assignment
1 { assigned(M, S, T) : screen(S), time(T) } 1 :- movie(M).

% Screen 3: exactly one movie at 8 PM
1 { assigned(M, 3, 8) : movie(M) } 1.
:- assigned(M, 3, T), T != 8.

% Screens 1 and 2: exactly two movies each, one at 7 and one at 9
:- screen(S), S != 3, #count { M : assigned(M, S, 7) } != 1.
:- screen(S), S != 3, #count { M : assigned(M, S, 9) } != 1.
:- screen(S), S != 3, #count { M : assigned(M, S, _) } != 2.

% No movie on screen 1 or 2 at 8 PM
:- assigned(M, S, 8), S != 3.

% Constraint: The western begins at some time before the horror film does.
:- assigned(western, _, Tw), assigned(horror, _, Th), Tw >= Th.

% Constraint: The sci-fi film is not shown on screen 3.
:- assigned(scifi, 3, _).

% Constraint: The romance is not shown on screen 2.
:- assigned(romance, 2, _).

% Constraint: The horror film and the mystery are shown on different screens.
:- assigned(horror, S1, _), assigned(mystery, S2, _), S1 = S2.

% Now check each option: which one CANNOT be a valid screen 2 schedule?
% We'll test each option by adding it as a constraint and seeing if UNSAT.

% Let's do this in one run by enumerating all valid schedules and checking which options appear.

% Get all valid assignments first, then check each option.

% We'll use a different approach: test each option individually by forcing it.

% Option A: screen2: 7=scifi, 9=horror
% Option B: screen2: 7=scifi, 9=mystery
% Option C: screen2: 7=scifi, 9=western
% Option D: screen2: 7=western, 9=horror
% Option E: screen2: 7=western, 9=mystery

% Let's just find all valid schedules and see which screen2 combos appear.
% We'll use a helper to record screen2 combos.

% First, let's just get all models and look at screen2 assignments.
#show assigned/3.