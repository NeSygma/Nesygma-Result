% Define the dice
die(a; b; c).

% Define faces (1 through 6 for each die)
face(1..6).

% Define possible values for faces
value(0..6).

% Assign values to faces of each die
% Each die has 6 faces, each with a value from {0,1,2,3,4,5,6}
{ assigned(D, F, V) : value(V) } = 1 :- die(D), face(F).

% Calculate pairwise comparisons
% A beats B: P(A > B) > 0.5 means > 18 wins out of 36
count_ab(N) :-
    N = #count { F1, F2 : assigned(a, F1, V1), assigned(b, F2, V2), V1 > V2 }.

count_bc(N) :-
    N = #count { F1, F2 : assigned(b, F1, V1), assigned(c, F2, V2), V1 > V2 }.

count_ca(N) :-
    N = #count { F1, F2 : assigned(c, F1, V1), assigned(a, F2, V2), V1 > V2 }.

% Enforce the nontransitive property: each must win in > 18 matchups
:- count_ab(N), N <= 18.
:- count_bc(N), N <= 18.
:- count_ca(N), N <= 18.

% Show the assignment
#show assigned/3.