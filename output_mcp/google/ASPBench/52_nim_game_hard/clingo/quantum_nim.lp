% --- Domain ---
pile(0, 6).
pile(1, 7).
pile(2, 10).
pile(3, 13).

% --- Nim Sum Calculation ---
nim_sum(S) :- 
    pile(0, P0), pile(1, P1), pile(2, P2), pile(3, P3),
    S = P0 ^ P1 ^ P2 ^ P3.

% --- Standard Moves ---
possible_standard_move(Index, NewSize) :-
    pile(Index, Size),
    nim_sum(OldSum),
    NewSize = OldSum ^ Size,
    NewSize < Size,
    NewSize >= 0.

% Check distinctness for standard moves
% A move is valid if no other pile has the same size as the new pile
is_valid_standard(Index, NewSize) :-
    possible_standard_move(Index, NewSize),
    not duplicate_standard(Index, NewSize).

duplicate_standard(Index, NewSize) :-
    possible_standard_move(Index, NewSize),
    pile(OtherIndex, OtherSize),
    Index != OtherIndex,
    NewSize == OtherSize.

% --- Split Moves ---
possible_split_move(Index, A, B) :-
    pile(Index, Size),
    Size \ 2 == 0,
    A = 1..Size-1,
    B = Size - A,
    A < B,
    nim_sum(OldSum),
    0 == OldSum ^ Size ^ A ^ B.

% Check distinctness for split moves
is_valid_split(Index, A, B) :-
    possible_split_move(Index, A, B),
    not duplicate_split_a(Index, A, B),
    not duplicate_split_b(Index, A, B),
    A != B.

duplicate_split_a(Index, A, B) :-
    possible_split_move(Index, A, B),
    pile(OtherIndex, OtherSize),
    Index != OtherIndex,
    A == OtherSize.

duplicate_split_b(Index, A, B) :-
    possible_split_move(Index, A, B),
    pile(OtherIndex, OtherSize),
    Index != OtherIndex,
    B == OtherSize.

% --- Output ---
option(standard(Index, Size - NewSize)) :- is_valid_standard(Index, NewSize), pile(Index, Size).
option(split(Index, A, B)) :- is_valid_split(Index, A, B).

#show option/1.