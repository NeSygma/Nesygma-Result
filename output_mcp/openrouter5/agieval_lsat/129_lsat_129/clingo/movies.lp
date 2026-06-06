% Domain: movies
movie(horror). movie(mystery). movie(romance). movie(scifi). movie(western).

% Domain: screens
screen(1). screen(2). screen(3).

% Domain: times
time(7). time(8). time(9).

% Each movie is shown exactly once, on one screen at one time.
% Screen 3 shows exactly one movie at 8 PM.
% Screens 1 and 2 show two movies each: one at 7 PM and one at 9 PM.

% We'll model: assigned(Movie, Screen, Time)

% Each movie gets exactly one (screen, time) assignment
1 { assigned(M, S, T) : screen(S), time(T) } 1 :- movie(M).

% Screen 3: exactly one movie at 8 PM, no other times
{ assigned(M, 3, 8) } :- movie(M).
:- assigned(M, 3, T), T != 8.
% Exactly one movie on screen 3
1 { assigned(M, 3, 8) : movie(M) } 1.

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

% Now evaluate each option.
% Each option lists two movies for screen 2: first at 7 PM, second at 9 PM.
% We need to find which option CANNOT be a valid list.

% Option A: screen 2: 7PM=scifi, 9PM=horror
option_a_possible :- assigned(scifi, 2, 7), assigned(horror, 2, 9).

% Option B: screen 2: 7PM=scifi, 9PM=mystery
option_b_possible :- assigned(scifi, 2, 7), assigned(mystery, 2, 9).

% Option C: screen 2: 7PM=scifi, 9PM=western
option_c_possible :- assigned(scifi, 2, 7), assigned(western, 2, 9).

% Option D: screen 2: 7PM=western, 9PM=horror
option_d_possible :- assigned(western, 2, 7), assigned(horror, 2, 9).

% Option E: screen 2: 7PM=western, 9PM=mystery
option_e_possible :- assigned(western, 2, 7), assigned(mystery, 2, 9).

% The answer is the option that is NOT possible in any valid schedule.
% We need to check which option has no satisfying assignment.

% We'll use a trick: find which option is impossible.
% Since we want the one that CANNOT be accurate, we check each.

% Let's just enumerate all valid schedules and see which options appear.
% We'll use #show to see all possible schedules.

#show assigned/3.
#show option_a_possible/0.
#show option_b_possible/0.
#show option_c_possible/0.
#show option_d_possible/0.
#show option_e_possible/0.