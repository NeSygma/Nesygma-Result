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

% Condition 2: Exactly two of the traditional pieces are performed consecutively
% This means exactly one pair of adjacent positions both have traditional pieces
consecutive_trad(P) :- pos(P), P < 5, assign_type(P, traditional), assign_type(P+1, traditional).
:- #count{ P : consecutive_trad(P) } != 1.

% Condition 3: Fourth solo - Wayne performs traditional OR Zara performs modern
valid4 :- assign_pianist(4, wayne), assign_type(4, traditional).
valid4 :- assign_pianist(4, zara), assign_type(4, modern).
:- not valid4.

% Condition 4: Pianist of solo 2 does not perform solo 5
:- assign_pianist(2, M), assign_pianist(5, M).

% Condition 5: No traditional piece until Wayne performs at least one modern piece
has_wayne_modern_before(P) :- pos(P), pos(Q), Q < P, assign_pianist(Q, wayne), assign_type(Q, modern).
:- assign_type(P, traditional), not has_wayne_modern_before(P).

% Derive which positions are traditional
is_trad(P) :- assign_type(P, traditional).
is_modern(P) :- assign_type(P, modern).

% Show the actual assignments for debugging
#show assign_pianist/2.
#show assign_type/2.
#show is_trad/1.
#show is_modern/1.