% Nontransitive Dice Problem
% Four dice (A, B, C, D) with 4 faces each, values 1-8
% Must form a cyclic dominance relationship with equal sums and distinct value sets

% Domain declarations
die(a). die(b). die(c). die(d).
face(1). face(2). face(3). face(4).
value(1..8).

% Each die has exactly 4 faces with values from 1-8
1 { value_on_die(D, F, V) : value(V) } 1 :- die(D), face(F).

% Ensure each die has exactly 4 faces (one value per face)
:- die(D), #count{F : value_on_die(D, F, _)} != 4.

% Calculate sum for each die
sum_die(D, S) :- die(D), S = #sum{V, F : value_on_die(D, F, V)}.

% All dice must have the same sum
common_sum(S) :- S = #min{S_D : sum_die(D, S_D)}, sum_die(D, S_D).
:- die(D), sum_die(D, S), common_sum(CS), S != CS.

% Helper: sorted values for each die (for output)
sorted_values(D, V1, V2, V3, V4) :-
    die(D),
    value_on_die(D, 1, V1),
    value_on_die(D, 2, V2),
    value_on_die(D, 3, V3),
    value_on_die(D, 4, V4),
    V1 <= V2, V2 <= V3, V3 <= V4.

% Unique value sets constraint
% For each pair of dice, their sets of values must be different
:- die(D1), die(D2), D1 != D2,
   #count{V : value_on_die(D1, _, V)} = N1,
   #count{V : value_on_die(D2, _, V)} = N2,
   N1 = N2,
   #count{V : value_on_die(D1, _, V), value_on_die(D2, _, V)} = N_common,
   N_common = N1.

% Win counting function
% For two dice D1 and D2, count how many times D1 beats D2
win_count(D1, D2, Count) :-
    die(D1), die(D2), D1 != D2,
    Count = #count{F1, F2 : value_on_die(D1, F1, V1), value_on_die(D2, F2, V2), V1 > V2}.

% Nontransitive cycle constraints
% A beats B (>8 wins out of 16)
:- win_count(a, b, C), C <= 8.
% B beats C (>8 wins out of 16)
:- win_count(b, c, C), C <= 8.
% C beats D (>8 wins out of 16)
:- win_count(c, d, C), C <= 8.
% D beats A (>8 wins out of 16)
:- win_count(d, a, C), C <= 8.

% Output the solution
#show die/1.
#show value_on_die/3.
#show sorted_values/5.
#show common_sum/1.
#show win_count/3.