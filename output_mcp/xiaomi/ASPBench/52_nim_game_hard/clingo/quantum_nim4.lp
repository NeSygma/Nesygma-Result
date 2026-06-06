% Quantum Nim - Find all optimal moves for Player 1

% Initial piles (0-indexed)
pile(0, 6).
pile(1, 7).
pile(2, 10).
pile(3, 13).

% Players
player(1).
player(2).

% Powers available
power_available(1, split).
power_available(2, merge).

% Current player
current_player(1).

% Helper: get all pile indices
pile_index(0..3).

% Helper: get pile size
pile_size(Index, Size) :- pile(Index, Size).

% Define possible standard moves
% Remove N stones from pile I (1 ≤ N ≤ size)
{ remove(I, N) : N = 1..Size } :- pile(I, Size).

% Define possible split moves (only for even-sized piles)
% Split pile I into two non-empty piles A and B where A + B = Size
{ split(I, A, B) : A = 1..Size-1, B = Size - A, A < B } :- 
    pile(I, Size), 
    Size mod 2 = 0.

% Constraint: after move, all piles must have different sizes
% For standard moves:
:- remove(I, N), 
   pile(I, Size), 
   NewSize = Size - N,
   pile(J, SizeJ), 
   J != I, 
   NewSize = SizeJ.

% For split moves:
:- split(I, A, B),
   pile(J, SizeJ),
   J != I,
   A = SizeJ.

:- split(I, A, B),
   pile(J, SizeJ),
   J != I,
   B = SizeJ.

% Also, the two new piles from split must be different
:- split(I, A, B), A = B.

% Define XOR operation for small numbers (0-15)
xor_val(0, 0, 0).
xor_val(0, 1, 1).
xor_val(1, 0, 1).
xor_val(1, 1, 0).
xor_val(0, 2, 2).
xor_val(2, 0, 2).
xor_val(1, 2, 3).
xor_val(2, 1, 3).
xor_val(0, 3, 3).
xor_val(3, 0, 3).
xor_val(1, 3, 2).
xor_val(3, 1, 2).
xor_val(2, 3, 1).
xor_val(3, 2, 1).
xor_val(0, 4, 4).
xor_val(4, 0, 4).
xor_val(1, 4, 5).
xor_val(4, 1, 5).
xor_val(2, 4, 6).
xor_val(4, 2, 6).
xor_val(3, 4, 7).
xor_val(4, 3, 7).
xor_val(0, 5, 5).
xor_val(5, 0, 5).
xor_val(1, 5, 4).
xor_val(5, 1, 4).
xor_val(2, 5, 7).
xor_val(5, 2, 7).
xor_val(3, 5, 6).
xor_val(5, 3, 6).
xor_val(4, 5, 1).
xor_val(5, 4, 1).
xor_val(0, 6, 6).
xor_val(6, 0, 6).
xor_val(1, 6, 7).
xor_val(6, 1, 7).
xor_val(2, 6, 4).
xor_val(6, 2, 4).
xor_val(3, 6, 5).
xor_val(6, 3, 5).
xor_val(4, 6, 2).
xor_val(6, 4, 2).
xor_val(5, 6, 3).
xor_val(6, 5, 3).
xor_val(0, 7, 7).
xor_val(7, 0, 7).
xor_val(1, 7, 6).
xor_val(7, 1, 6).
xor_val(2, 7, 5).
xor_val(7, 2, 5).
xor_val(3, 7, 4).
xor_val(7, 3, 4).
xor_val(4, 7, 3).
xor_val(7, 4, 3).
xor_val(5, 7, 2).
xor_val(7, 5, 2).
xor_val(6, 7, 1).
xor_val(7, 6, 1).
xor_val(0, 8, 8).
xor_val(8, 0, 8).
xor_val(1, 8, 9).
xor_val(8, 1, 9).
xor_val(2, 8, 10).
xor_val(8, 2, 10).
xor_val(3, 8, 11).
xor_val(8, 3, 11).
xor_val(4, 8, 12).
xor_val(8, 4, 12).
xor_val(5, 8, 13).
xor_val(8, 5, 13).
xor_val(6, 8, 14).
xor_val(8, 6, 14).
xor_val(7, 8, 15).
xor_val(8, 7, 15).
xor_val(0, 9, 9).
xor_val(9, 0, 9).
xor_val(1, 9, 8).
xor_val(9, 1, 8).
xor_val(2, 9, 11).
xor_val(9, 2, 11).
xor_val(3, 9, 10).
xor_val(9, 3, 10).
xor_val(4, 9, 13).
xor_val(9, 4, 13).
xor_val(5, 9, 12).
xor_val(9, 5, 12).
xor_val(6, 9, 15).
xor_val(9, 6, 15).
xor_val(7, 9, 14).
xor_val(9, 7, 14).
xor_val(8, 9, 1).
xor_val(9, 8, 1).
xor_val(0, 10, 10).
xor_val(10, 0, 10).
xor_val(1, 10, 11).
xor_val(10, 1, 11).
xor_val(2, 10, 8).
xor_val(10, 2, 8).
xor_val(3, 10, 9).
xor_val(10, 3, 9).
xor_val(4, 10, 14).
xor_val(10, 4, 14).
xor_val(5, 10, 15).
xor_val(10, 5, 15).
xor_val(6, 10, 12).
xor_val(10, 6, 12).
xor_val(7, 10, 13).
xor_val(10, 7, 13).
xor_val(8, 10, 2).
xor_val(10, 8, 2).
xor_val(9, 10, 3).
xor_val(10, 9, 3).
xor_val(0, 11, 11).
xor_val(11, 0, 11).
xor_val(1, 11, 10).
xor_val(11, 1, 10).
xor_val(2, 11, 9).
xor_val(11, 2, 9).
xor_val(3, 11, 8).
xor_val(11, 3, 8).
xor_val(4, 11, 15).
xor_val(11, 4, 15).
xor_val(5, 11, 14).
xor_val(11, 5, 14).
xor_val(6, 11, 13).
xor_val(11, 6, 13).
xor_val(7, 11, 12).
xor_val(11, 7, 12).
xor_val(8, 11, 3).
xor_val(11, 8, 3).
xor_val(9, 11, 2).
xor_val(11, 9, 2).
xor_val(10, 11, 1).
xor_val(11, 10, 1).
xor_val(0, 12, 12).
xor_val(12, 0, 12).
xor_val(1, 12, 13).
xor_val(12, 1, 13).
xor_val(2, 12, 14).
xor_val(12, 2, 14).
xor_val(3, 12, 15).
xor_val(12, 3, 15).
xor_val(4, 12, 8).
xor_val(12, 4, 8).
xor_val(5, 12, 9).
xor_val(12, 5, 9).
xor_val(6, 12, 10).
xor_val(12, 6, 10).
xor_val(7, 12, 11).
xor_val(12, 7, 11).
xor_val(8, 12, 4).
xor_val(12, 8, 4).
xor_val(9, 12, 5).
xor_val(12, 9, 5).
xor_val(10, 12, 6).
xor_val(12, 10, 6).
xor_val(11, 12, 7).
xor_val(12, 11, 7).
xor_val(0, 13, 13).
xor_val(13, 0, 13).
xor_val(1, 13, 12).
xor_val(13, 1, 12).
xor_val(2, 13, 15).
xor_val(13, 2, 15).
xor_val(3, 13, 14).
xor_val(13, 3, 14).
xor_val(4, 13, 9).
xor_val(13, 4, 9).
xor_val(5, 13, 8).
xor_val(13, 5, 8).
xor_val(6, 13, 11).
xor_val(13, 6, 11).
xor_val(7, 13, 10).
xor_val(13, 7, 10).
xor_val(8, 13, 5).
xor_val(13, 8, 5).
xor_val(9, 13, 4).
xor_val(13, 9, 4).
xor_val(10, 13, 7).
xor_val(13, 10, 7).
xor_val(11, 13, 6).
xor_val(13, 11, 6).
xor_val(12, 13, 1).
xor_val(13, 12, 1).
xor_val(0, 14, 14).
xor_val(14, 0, 14).
xor_val(1, 14, 15).
xor_val(14, 1, 15).
xor_val(2, 14, 12).
xor_val(14, 2, 12).
xor_val(3, 14, 13).
xor_val(14, 3, 13).
xor_val(4, 14, 10).
xor_val(14, 4, 10).
xor_val(5, 14, 11).
xor_val(14, 5, 11).
xor_val(6, 14, 8).
xor_val(14, 6, 8).
xor_val(7, 14, 9).
xor_val(14, 7, 9).
xor_val(8, 14, 6).
xor_val(14, 8, 6).
xor_val(9, 14, 7).
xor_val(14, 9, 7).
xor_val(10, 14, 4).
xor_val(14, 10, 4).
xor_val(11, 14, 5).
xor_val(14, 11, 5).
xor_val(12, 14, 2).
xor_val(14, 12, 2).
xor_val(13, 14, 3).
xor_val(14, 13, 3).
xor_val(0, 15, 15).
xor_val(15, 0, 15).
xor_val(1, 15, 14).
xor_val(15, 1, 14).
xor_val(2, 15, 13).
xor_val(15, 2, 13).
xor_val(3, 15, 12).
xor_val(15, 3, 12).
xor_val(4, 15, 11).
xor_val(15, 4, 11).
xor_val(5, 15, 10).
xor_val(15, 5, 10).
xor_val(6, 15, 9).
xor_val(15, 6, 9).
xor_val(7, 15, 8).
xor_val(15, 7, 8).
xor_val(8, 15, 7).
xor_val(15, 8, 7).
xor_val(9, 15, 6).
xor_val(15, 9, 6).
xor_val(10, 15, 5).
xor_val(15, 10, 5).
xor_val(11, 15, 4).
xor_val(15, 11, 4).
xor_val(12, 15, 3).
xor_val(15, 12, 3).
xor_val(13, 15, 2).
xor_val(15, 13, 2).
xor_val(14, 15, 1).
xor_val(15, 14, 1).

% Compute XOR of multiple values using helper
xor3(X, Y, Z, Result) :-
    xor_val(X, Y, Temp),
    xor_val(Temp, Z, Result).

xor4(X, Y, Z, W, Result) :-
    xor_val(X, Y, Temp1),
    xor_val(Temp1, Z, Temp2),
    xor_val(Temp2, W, Result).

xor5(X, Y, Z, W, V, Result) :-
    xor_val(X, Y, Temp1),
    xor_val(Temp1, Z, Temp2),
    xor_val(Temp2, W, Temp3),
    xor_val(Temp3, V, Result).

% Compute nim-sum after standard move
% For pile 0 (size 6): removing N stones → new size = 6 - N
nim_sum_after_standard(0, N, Result) :-
    remove(0, N),
    pile(1, S1), pile(2, S2), pile(3, S3),
    NewSize = 6 - N,
    xor4(NewSize, S1, S2, S3, Result).

% For pile 1 (size 7): removing N stones → new size = 7 - N
nim_sum_after_standard(1, N, Result) :-
    remove(1, N),
    pile(0, S0), pile(2, S2), pile(3, S3),
    NewSize = 7 - N,
    xor4(S0, NewSize, S2, S3, Result).

% For pile 2 (size 10): removing N stones → new size = 10 - N
nim_sum_after_standard(2, N, Result) :-
    remove(2, N),
    pile(0, S0), pile(1, S1), pile(3, S3),
    NewSize = 10 - N,
    xor4(S0, S1, NewSize, S3, Result).

% For pile 3 (size 13): removing N stones → new size = 13 - N
nim_sum_after_standard(3, N, Result) :-
    remove(3, N),
    pile(0, S0), pile(1, S1), pile(2, S2),
    NewSize = 13 - N,
    xor4(S0, S1, S2, NewSize, Result).

% Compute nim-sum after split move
% For pile 0 (size 6): split into A and B
nim_sum_after_split(0, A, B, Result) :-
    split(0, A, B),
    pile(1, S1), pile(2, S2), pile(3, S3),
    xor5(S1, S2, S3, A, B, Result).

% For pile 1 (size 7): not even, so no split
% For pile 2 (size 10): split into A and B
nim_sum_after_split(2, A, B, Result) :-
    split(2, A, B),
    pile(0, S0), pile(1, S1), pile(3, S3),
    xor5(S0, S1, S3, A, B, Result).

% For pile 3 (size 13): not even, so no split

% A move is optimal if resulting nim-sum is 0
optimal_standard(I, N) :-
    remove(I, N),
    nim_sum_after_standard(I, N, 0).

optimal_split(I, A, B) :-
    split(I, A, B),
    nim_sum_after_split(I, A, B, 0).

% Compute initial nim-sum
initial_nim_sum(Result) :-
    pile(0, S0), pile(1, S1), pile(2, S2), pile(3, S3),
    xor4(S0, S1, S2, S3, Result).

% Winning position if nim-sum is non-zero
is_winning_position :- initial_nim_sum(S), S != 0.

% Show results
#show optimal_standard/2.
#show optimal_split/3.
#show initial_nim_sum/1.
#show is_winning_position/0.