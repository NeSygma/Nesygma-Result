% --- Facts ---
pile(0, 6).
pile(1, 7).
pile(2, 10).
pile(3, 13).
player(1).

% --- Helper Predicates ---
pile_index(0..3).

% --- Generate Standard Moves ---
% Standard move: remove 1 to N stones from a pile
{ standard_move(PileIndex, StonesRemoved) :
    pile(PileIndex, Size),
    StonesRemoved = 1..Size
}.

% --- Generate Split Moves ---
% Split move: split an even-sized pile into two non-empty piles of unique sizes
{ power_split(PileIndex, SplitSize1, SplitSize2) :
    pile(PileIndex, Size),
    Size > 1,
    Size mod 2 = 0,
    SplitSize1 = 1..(Size-1),
    SplitSize2 = Size - SplitSize1,
    SplitSize1 < SplitSize2
}.

% --- Compute Resulting Piles for Standard Moves ---
resulting_pile(Index, NewSize) :-
    standard_move(PileIndex, StonesRemoved),
    pile(PileIndex, Size),
    Index = PileIndex,
    NewSize = Size - StonesRemoved,
    NewSize > 0.

resulting_pile(Index, Size) :-
    standard_move(PileIndex, StonesRemoved),
    pile(Index, Size),
    Index != PileIndex.

% --- Compute Resulting Piles for Split Moves ---
resulting_pile(4, SplitSize1) :-
    power_split(PileIndex, SplitSize1, SplitSize2).

resulting_pile(5, SplitSize2) :-
    power_split(PileIndex, SplitSize1, SplitSize2).

resulting_pile(Index, Size) :-
    power_split(PileIndex, SplitSize1, SplitSize2),
    pile(Index, Size),
    Index != PileIndex.

% --- Ensure All Piles Are Unique ---
:- resulting_pile(_, Size1),
   resulting_pile(_, Size2),
   Size1 = Size2,
   Size1 != Size2.

% --- Compute Nim-sum (bitwise XOR) ---
% Collect all resulting pile sizes
resulting_pile_size(Size) :-
    resulting_pile(_, Size).

% Compute XOR of all resulting pile sizes
nim_sum(N) :-
    N = #sum { Size : resulting_pile_size(Size) }.

% --- Optimal Moves ---
% Standard optimal move: leads to nim-sum 0
optimal_move(standard, PileIndex, StonesRemoved) :-
    standard_move(PileIndex, StonesRemoved),
    resulting_pile_size(Size1),
    resulting_pile_size(Size2),
    resulting_pile_size(Size3),
    resulting_pile_size(Size4),
    Size1 != Size2,
    Size1 != Size3,
    Size1 != Size4,
    Size2 != Size3,
    Size2 != Size4,
    Size3 != Size4,
    #sum { X : resulting_pile_size(X) } = 0.

% Split optimal move: leads to nim-sum 0
optimal_move(power_split, PileIndex, SplitSize1, SplitSize2) :-
    power_split(PileIndex, SplitSize1, SplitSize2),
    resulting_pile_size(Size1),
    resulting_pile_size(Size2),
    resulting_pile_size(Size3),
    resulting_pile_size(Size4),
    Size1 != Size2,
    Size1 != Size3,
    Size1 != Size4,
    Size2 != Size3,
    Size2 != Size4,
    Size3 != Size4,
    #sum { X : resulting_pile_size(X) } = 0.

% --- Show Optimal Moves ---
#show optimal_move/4.