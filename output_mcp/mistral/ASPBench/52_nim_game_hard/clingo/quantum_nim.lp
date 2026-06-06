% Initial state
pile(0, 6).
pile(1, 7).
pile(2, 10).
pile(3, 13).

current_player(player1).

% Powers available (though not used in standard moves for this solution)
has_power(player1, split).
has_power(player2, merge).

% Helper to get all pile indices
pile_index(0..3).

% Helper to get all pile sizes
pile_size(Size) :- pile(_, Size).

% Possible stones to remove: 1 to pile size
stones_to_remove(S, Size) :- pile(_, Size), S = 1..Size.

% Possible standard moves for Player 1
% Remove 1 to pile_size stones from any pile
possible_move(standard, PileIndex, StonesRemoved) :-
    pile(PileIndex, Size),
    pile_index(PileIndex),
    stones_to_remove(StonesRemoved, Size).

% Compute new pile sizes after a standard move
new_piles(standard, PileIndex, StonesRemoved, NewPile0, NewPile1, NewPile2, NewPile3) :-
    pile(0, P0), pile(1, P1), pile(2, P2), pile(3, P3),
    pile(PileIndex, Size),
    NewSize = Size - StonesRemoved,
    NewSize > 0,
    (
        PileIndex = 0, NewPile0 = NewSize, NewPile1 = P1, NewPile2 = P2, NewPile3 = P3 ;
        PileIndex = 1, NewPile0 = P0, NewPile1 = NewSize, NewPile2 = P2, NewPile3 = P3 ;
        PileIndex = 2, NewPile0 = P0, NewPile1 = P1, NewPile2 = NewSize, NewPile3 = P3 ;
        PileIndex = 3, NewPile0 = P0, NewPile1 = P1, NewPile2 = P2, NewPile3 = NewSize
    ).

% State validity: all piles must be unique
valid_state(NewPile0, NewPile1, NewPile2, NewPile3) :-
    NewPile0 != NewPile1, NewPile0 != NewPile2, NewPile0 != NewPile3,
    NewPile1 != NewPile2, NewPile1 != NewPile3,
    NewPile2 != NewPile3.

% Calculate nim-sum for a state
nim_sum(NewPile0, NewPile1, NewPile2, NewPile3, Sum) :-
    Sum = NewPile0 ^ NewPile1 ^ NewPile2 ^ NewPile3.

% Check if a move is valid and optimal (results in nim-sum = 0)
optimal_move(standard, PileIndex, StonesRemoved) :-
    possible_move(standard, PileIndex, StonesRemoved),
    new_piles(standard, PileIndex, StonesRemoved, NewPile0, NewPile1, NewPile2, NewPile3),
    valid_state(NewPile0, NewPile1, NewPile2, NewPile3),
    nim_sum(NewPile0, NewPile1, NewPile2, NewPile3, 0).

% Output format
#show optimal_move/3.