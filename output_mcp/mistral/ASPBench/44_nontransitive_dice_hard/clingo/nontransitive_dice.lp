%% Define the dice and their faces
% Four dice: A, B, C, D
dice(a). die(b). die(c). die(d).

% Each die has 4 faces
faces(1). faces(2). faces(3). faces(4).

% Value range: 1 to 8
value(1). value(2). value(3). value(4). value(5). value(6). value(7). value(8).

% Each die must have exactly 4 faces with values from 1 to 8
% We'll use a choice rule to assign values to each face of each die
{ face_value(D, F, V) : value(V) } = 1 :- die(D), faces(F).

% Enforce that each die's face values are sorted in non-decreasing order
% This means for any two faces F1 < F2 on the same die, V1 <= V2
:- face_value(D, F1, V1), face_value(D, F2, V2), F1 < F2, V1 > V2.

% Calculate the sum of face values for each die
sum(D, S) :- die(D), S = #sum { V, F : face_value(D, F, V) }.

% Enforce equal sum constraint: all dice must have the same sum
:- die(D1), die(D2), sum(D1, S1), sum(D2, S2), S1 != S2.

% Collect unique values for each die
unique_value(D, V) :- die(D), value(V), face_value(D, _, V).

% Enforce unique value sets: no two dice can have the same set of unique values
% To do this, we enforce that for any two dice, there exists a value in one but not the other
:- die(D1), die(D2), D1 != D2,
   not (unique_value(D1, V), not unique_value(D2, V)),
   not (unique_value(D2, V), not unique_value(D1, V)).

% Define when die X beats die Y: X wins in more than 8 out of 16 possible rolls
% For each pair of dice (X, Y), count how many times X's face > Y's face
beats(X, Y, N) :- die(X), die(Y), X != Y,
                  N = #count { Vx, Vy, Fx, Fy : face_value(X, Fx, Vx), face_value(Y, Fy, Vy), Vx > Vy },
                  N > 8.

% Enforce the nontransitive cycle: A beats B, B beats C, C beats D, D beats A
:- not beats(a, b, _).
:- not beats(b, c, _).
:- not beats(c, d, _).
:- not beats(d, a, _).

% Extract the common sum
common_sum(S) :- sum(a, S).

% Extract win counts for the analysis
win_counts("A_beats_B", N) :- beats(a, b, N).
win_counts("B_beats_C", N) :- beats(b, c, N).
win_counts("C_beats_D", N) :- beats(c, d, N).
win_counts("D_beats_A", N) :- beats(d, a, N).

% Show the dice configuration
#show face_value/3.
#show common_sum/1.
#show win_counts/2.