% Domain
pos(1..5).
pianist(wayne).
pianist(zara).
piece_type(modern).
piece_type(traditional).

% For each position, assign exactly one pianist and one type
{ assign_pianist(P, M) : pianist(M) } 1 :- pos(P).
{ assign_type(P, T) : piece_type(T) } 1 :- pos(P).

% Condition 1: Third solo is a traditional piece
:- assign_type(3, modern).

% Condition 2: Exactly two traditional pieces are performed consecutively
% (exactly one pair of adjacent traditional pieces)
consecutive_trad(P) :- pos(P), P < 5, assign_type(P, traditional), assign_type(P+1, traditional).
:- #count{ P : consecutive_trad(P) } != 1.

% Condition 3: Fourth solo - Wayne performs traditional OR Zara performs modern
valid4 :- assign_pianist(4, wayne), assign_type(4, traditional).
valid4 :- assign_pianist(4, zara), assign_type(4, modern).
:- not valid4.

% Condition 4: Pianist of solo 2 does not perform solo 5
:- assign_pianist(2, M), assign_pianist(5, M).

% Condition 5: No traditional piece until Wayne performs at least one modern piece
% For every traditional position P, there must exist Q < P where Wayne plays modern
has_wayne_modern_before(P) :- pos(P), pos(Q), Q < P, assign_pianist(Q, wayne), assign_type(Q, modern).
:- assign_type(P, traditional), not has_wayne_modern_before(P).

% Check which answer choices could be the complete set of traditional pieces
% (A) traditional at 1, 3, 4
option_a_possible :- assign_type(1, traditional), assign_type(2, modern), assign_type(3, traditional), assign_type(4, traditional), assign_type(5, modern).

% (B) traditional at 2, 3, 4
option_b_possible :- assign_type(1, modern), assign_type(2, traditional), assign_type(3, traditional), assign_type(4, traditional), assign_type(5, modern).

% (C) traditional at 3, 4
option_c_possible :- assign_type(1, modern), assign_type(2, modern), assign_type(3, traditional), assign_type(4, traditional), assign_type(5, modern).

% (D) traditional at 3, 5
option_d_possible :- assign_type(1, modern), assign_type(2, modern), assign_type(3, traditional), assign_type(4, modern), assign_type(5, traditional).

% (E) traditional at 4, 5
option_e_possible :- assign_type(1, modern), assign_type(2, modern), assign_type(3, modern), assign_type(4, traditional), assign_type(5, traditional).

option(a) :- option_a_possible.
option(b) :- option_b_possible.
option(c) :- option_c_possible.
option(d) :- option_d_possible.
option(e) :- option_e_possible.

#show option/1.