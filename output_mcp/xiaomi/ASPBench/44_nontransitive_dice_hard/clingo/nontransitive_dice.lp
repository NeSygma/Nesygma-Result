% Domain definitions
die(a). die(b). die(c). die(d).
face(1). face(2). face(3). face(4).
value(1..8).

% Each die has exactly 4 faces, each with a value 1-8
{ face_value(D, F, V) : value(V) } 1 :- die(D), face(F).

% Each die must have exactly 4 faces assigned
:- die(D), #count{F : face(F), face_value(D, F, _)} != 4.

% Sort faces for output (enforce non-decreasing order)
:- face_value(D, F1, V1), face_value(D, F2, V2), F1 < F2, V1 > V2.

% Calculate sum of each die
sum(D, S) :- die(D), S = #sum{V, F : face_value(D, F, V)}.

% All dice must have equal sums
:- sum(D1, S1), sum(D2, S2), D1 != D2, S1 != S2.

% Track distinct values on each die
has_value(D, V) :- face_value(D, _, V).

% Value sets must be unique (encoded as sorted tuples)
% We'll use a helper to compare sets
value_set(D, V1, V2, V3, V4) :- 
    die(D), 
    V1 = #min{V : has_value(D, V)},
    V4 = #max{V : has_value(D, V)},
    V2 = #min{V : has_value(D, V), V != V1},
    V3 = #max{V : has_value(D, V), V != V4}.

% Ensure unique value sets
:- value_set(D1, V1, V2, V3, V4), value_set(D2, V1, V2, V3, V4), D1 != D2.

% Count wins: die X beats die Y if X's value > Y's value
win_count(X, Y, N) :- 
    die(X), die(Y), X != Y,
    N = #count{F1, F2 : face_value(X, F1, VX), face_value(Y, F2, VY), VX > VY}.

% Cyclic dominance: A beats B, B beats C, C beats D, D beats A
:- win_count(a, b, N), N <= 8.
:- win_count(b, c, N), N <= 8.
:- win_count(c, d, N), N <= 8.
:- win_count(d, a, N), N <= 8.

% Show results
#show face_value/3.
#show win_count/3.
#show sum/2.