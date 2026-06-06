% Quantum Nim - Optimal Moves Analysis

% Initial piles with explicit indices
pile(0,6).
pile(1,7).
pile(2,10).
pile(3,13).

% Compute initial nim-sum using XOR (^ is bitwise XOR in Clingo)
initial_nim_sum(Nim) :- 
    pile(0,S0), pile(1,S1), pile(2,S2), pile(3,S3),
    Nim = ((S0 ^ S1) ^ S2) ^ S3.

% Winning position if nim-sum != 0
is_winning_position(true) :- initial_nim_sum(Nim), Nim != 0.
is_winning_position(false) :- initial_nim_sum(Nim), Nim == 0.

% Generate standard move candidates: change pile i from S to T = S XOR Nim
% T must be between 0 and S (inclusive)
standard_move_candidate(i, T) :- 
    pile(i, S), initial_nim_sum(Nim), 
    T = S ^ Nim, T >= 0, T <= S.

% Constraint: T must be distinct from other piles (if T > 0)
:- standard_move_candidate(i, T), T > 0, pile(j, T), j != i.

% Valid standard moves are those that satisfy the constraint
valid_standard_move(i, T) :- standard_move_candidate(i, T), T == 0.
valid_standard_move(i, T) :- standard_move_candidate(i, T), T > 0, not pile(j, T) : j != i.

% Generate split candidates for even-sized piles
% Split into a and b where a + b = S, a != b, a > 0, b > 0
split_candidate(i, a, b) :- 
    pile(i, S), S mod 2 == 0, 
    a = 1..(S-1), b = S - a, a != b.

% Constraints: a and b must be distinct from other piles
:- split_candidate(i, a, b), pile(j, a), j != i.
:- split_candidate(i, a, b), pile(j, b), j != i.

% Valid split moves are those that satisfy the constraints
valid_split_move(i, a, b) :- 
    split_candidate(i, a, b), 
    not (pile(j, a) : j != i), 
    not (pile(j, b) : j != i).

% Compute new nim-sum for standard moves
new_nim_standard(i, T, NewNim) :- 
    valid_standard_move(i, T), pile(i, S), initial_nim_sum(Nim), 
    NewNim = Nim ^ S ^ T.

% Compute new nim-sum for split moves
new_nim_split(i, a, b, NewNim) :- 
    valid_split_move(i, a, b), pile(i, S), initial_nim_sum(Nim), 
    NewNim = Nim ^ S ^ a ^ b.

% Optimal moves are those with new nim-sum == 0
optimal_standard_move(i, T) :- new_nim_standard(i, T, NewNim), NewNim == 0.
optimal_split_move(i, a, b) :- new_nim_split(i, a, b, NewNim), NewNim == 0.

% Collect optimal moves into a list with stones removed and split sizes
optimal_move_list(standard, i, StonesRemoved, 0, 0) :- 
    optimal_standard_move(i, T), pile(i, S), StonesRemoved = S - T.
optimal_move_list(split, i, 0, a, b) :- optimal_split_move(i, a, b).

% Assign unique IDs to optimal moves (sorted by type and index)
optimal_move_id(M, Type, Index, StonesRemoved, SplitInto1, SplitInto2) :-
    optimal_move_list(Type, Index, StonesRemoved, SplitInto1, SplitInto2),
    M = #count { 1 : optimal_move_list(T2, I2, _, _, _), (T2 < Type; T2 == Type, I2 < Index) } + 1.

% Output optimal moves
optimal_move(M, Type, Index, StonesRemoved, SplitInto1, SplitInto2) :-
    optimal_move_id(M, Type, Index, StonesRemoved, SplitInto1, SplitInto2).

% Resulting piles for standard moves
resulting_pile(M, Size) :-
    optimal_move(M, standard, i, StonesRemoved, _, _),
    pile(i, S), T = S - StonesRemoved,
    j != i, pile(j, Size).
resulting_pile(M, T) :-
    optimal_move(M, standard, i, StonesRemoved, _, _),
    pile(i, S), T = S - StonesRemoved, T > 0.

% Resulting piles for split moves
resulting_pile(M, Size) :-
    optimal_move(M, split, i, _, a, b),
    j != i, pile(j, Size).
resulting_pile(M, a) :-
    optimal_move(M, split, i, _, a, b).
resulting_pile(M, b) :-
    optimal_move(M, split, i, _, a, b).

% Show the required output
#show initial_nim_sum/1.
#show is_winning_position/1.
#show optimal_move/6.
#show resulting_pile/2.