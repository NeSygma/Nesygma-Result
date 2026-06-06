%% Nontransitive Dice Problem
%% 4 dice (A,B,C,D), 4 faces each, values 1..8
%% Cyclic dominance: A>B, B>C, C>D, D>A (wins > 8/16)
%% Equal sum across all dice
%% Unique value sets per die

%% --- Domains ---
die(a; b; c; d).
face(1..4).
value(1..8).

%% --- Each die has exactly 4 faces, each face gets a value ---
{ face_val(D, F, V) : value(V) } 1 :- die(D), face(F).

%% Each die must have exactly 4 face values (one per face)
:- die(D), face(F), not face_val(D, F, _).

%% --- Constraint: Equal sum across all dice ---
%% Compute sum for each die
die_sum(D, S) :- S = #sum { V, F : face_val(D, F, V) }, die(D).

%% All dice must have the same sum
:- die_sum(D1, S1), die_sum(D2, S2), D1 != D2, S1 != S2.

%% --- Constraint: Unique value sets ---
%% The set of unique values on each die must be distinct
has_value(D, V) :- face_val(D, _, V).

%% Two dice cannot have identical value sets
same_set(D1, D2) :- die(D1), die(D2), D1 < D2,
   #count { V : has_value(D1, V), not has_value(D2, V) } = 0,
   #count { V : has_value(D2, V), not has_value(D1, V) } = 0.

:- same_set(D1, D2), D1 != D2.

%% --- Win determination ---
%% For each pair of dice (X,Y), count how many of the 16 roll combos X wins
win_roll(X, Y, Fx, Fy) :- face_val(X, Fx, Vx), face_val(Y, Fy, Vy), Vx > Vy.

win_count(X, Y, N) :- die(X), die(Y), X != Y,
   N = #count { Fx, Fy : win_roll(X, Y, Fx, Fy) }.

%% --- Nontransitive cycle constraints ---
%% A beats B: win_count(a, b, N), N > 8
:- win_count(a, b, N), N <= 8.
%% B beats C
:- win_count(b, c, N), N <= 8.
%% C beats D
:- win_count(c, d, N), N <= 8.
%% D beats A
:- win_count(d, a, N), N <= 8.

%% --- Sorted output: enforce non-decreasing order ---
:- face_val(D, F1, V1), face_val(D, F2, V2), F1 < F2, V1 > V2.

%% --- Show results ---
#show face_val/3.
#show die_sum/2.
#show win_count/3.