% Define the dice and face values.
die(a). die(b). die(c).
face_value(0..6).

% Assign exactly 6 faces to each die, with values from {0,1,2,3,4,5,6}.
{ face(D, V) : face_value(V) } = 6 :- die(D).

% Count the number of winning matchups between two dice (X beats Y if X > Y).
win_count(X, Y, N) :-
    die(X), die(Y), X != Y,
    N = #count { V1, V2 : face(X, V1), face(Y, V2), V1 > V2 }.

% Ensure that the number of winning matchups is >= 19 (i.e., P(X > Y) > 0.5).
beats(X, Y) :-
    die(X), die(Y), X != Y,
    win_count(X, Y, N), N >= 19.

% Nontransitive property: A beats B, B beats C, and C beats A.
:- not beats(a, b).
:- not beats(b, c).
:- not beats(c, a).

% Show the face values and win counts.
#show face/2.
#show win_count/3.