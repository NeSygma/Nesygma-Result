% --- Declare dice and faces ---
die(a; b; c; d).
face(D, 1..4) :- die(D).

% --- Choose face values ---
{ face_value(D, F, V) : V = 1..8 } 1 :- die(D), face(D, F).

% --- Enforce value range ---
:- face_value(_, _, V), V < 1.
:- face_value(_, _, V), V > 8.

% --- Enforce equal sum ---
% Compute sum for each die
sum(D, S) :- die(D), S = #sum { V : face_value(D, F, V) }.
% Ensure all dice have the same sum
:- sum(a, S), sum(b, S), sum(c, S), sum(d, S), common_sum(S) = 0.
common_sum(S) :- sum(a, S), sum(b, S), sum(c, S), sum(d, S).

% --- Enforce unique sorted value lists ---
% Collect values for each die
has_value(D, V) :- face_value(D, F, V).
% Sort values for each die
sorted_values(D, V1, V2, V3, V4) :-
    has_value(D, V1), has_value(D, V2), has_value(D, V3), has_value(D, V4),
    V1 <= V2, V2 <= V3, V3 <= V4.
% Ensure unique sorted lists
:- sorted_values(D1, V1, V2, V3, V4), sorted_values(D2, V1, V2, V3, V4), D1 < D2.

% --- Enforce nontransitive cycle ---
% Define beats(X,Y) as winning more than 8 times out of 16
beats(X, Y) :-
    X = a, Y = b, N = #count { Vx, Vy : face_value(a, _, Vx), face_value(b, _, Vy), Vx > Vy }, N > 8;
    X = b, Y = c, N = #count { Vx, Vy : face_value(b, _, Vx), face_value(c, _, Vy), Vx > Vy }, N > 8;
    X = c, Y = d, N = #count { Vx, Vy : face_value(c, _, Vx), face_value(d, _, Vy), Vx > Vy }, N > 8;
    X = d, Y = a, N = #count { Vx, Vy : face_value(d, _, Vx), face_value(a, _, Vy), Vx > Vy }, N > 8.

% Ensure the cycle exists
:- not beats(a, b).
:- not beats(b, c).
:- not beats(c, d).
:- not beats(d, a).

% --- Output ---
#show face_value/3.
#show common_sum/1.
#show beats/2.