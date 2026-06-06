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

% Now test each option by forcing it and checking if satisfiable.
% We'll use a choice to select which option to test, and then check.

% Option A: screen2: 7=scifi, 9=horror
option_a_possible :- assigned(scifi, 2, 7), assigned(horror, 2, 9).

% Option B: screen2: 7=scifi, 9=mystery
option_b_possible :- assigned(scifi, 2, 7), assigned(mystery, 2, 9).

% Option C: screen2: 7=scifi, 9=western
option_c_possible :- assigned(scifi, 2, 7), assigned(western, 2, 9).

% Option D: screen2: 7=western, 9=horror
option_d_possible :- assigned(western, 2, 7), assigned(horror, 2, 9).

% Option E: screen2: 7=western, 9=mystery
option_e_possible :- assigned(western, 2, 7), assigned(mystery, 2, 9).

% The answer is the option that is NOT possible
% We need to find which one cannot happen.

% Let's just enumerate all models and see which options appear.
#show option_a_possible/0.
#show option_b_possible/0.
#show option_c_possible/0.
#show option_d_possible/0.
#show option_e_possible/0.