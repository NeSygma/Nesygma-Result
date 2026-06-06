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

% Helper: compute nim-sum of a set of piles
% We'll compute XOR iteratively
% First, define the XOR operation
xor(0, 0, 0).
xor(0, 1, 1).
xor(1, 0, 1).
xor(1, 1, 0).

% Compute XOR of two numbers using binary representation
% For simplicity, we'll use a direct approach with aggregates

% Define possible standard moves
% Remove N stones from pile I (1 ≤ N ≤ size)
{ standard_move(I, N) : N = 1..Size } :- pile(I, Size).

% Define possible split moves (only for even-sized piles)
% Split pile I into two non-empty piles A and B where A + B = Size
{ split_move(I, A, B) : A = 1..Size-1, B = Size-A, A < B } :- 
    pile(I, Size), 
    Size mod 2 = 0,
    power_available(1, split).

% Compute resulting piles after a standard move
resulting_piles_standard(I, N, ResultPiles) :-
    standard_move(I, N),
    pile(I, Size),
    NewSize = Size - N,
    % Create new pile list with updated size at index I
    ResultPiles = [NewSize : J = 0..3, J != I; Size : J = I].

% Compute resulting piles after a split move
resulting_piles_split(I, A, B, ResultPiles) :-
    split_move(I, A, B),
    % Remove pile I and add two new piles A and B
    ResultPiles = [Size : J = 0..3, J != I; A; B].

% Helper: compute nim-sum of a list of numbers
% We'll use a recursive approach
nim_sum_list([], 0).
nim_sum_list([X|Rest], Sum) :-
    nim_sum_list(Rest, RestSum),
    Sum = X xor RestSum.

% Check if resulting piles have all different sizes
all_different_sizes(Piles) :-
    % For each pair of piles, they must be different
    % We'll use a constraint approach
    true.

% Actually, let's use a simpler approach: generate all possible moves and check constraints

% Define all possible moves for current player
% Standard moves
move(standard, I, N, 0, 0) :- 
    standard_move(I, N),
    pile(I, Size),
    NewSize = Size - N,
    NewSize > 0.  % Can't remove all stones (must leave at least 1)

% Split moves
move(split, I, 0, A, B) :-
    split_move(I, A, B).

% Compute resulting piles after any move
resulting_piles(standard, I, N, 0, 0, ResultPiles) :-
    move(standard, I, N, 0, 0),
    pile(I, Size),
    NewSize = Size - N,
    % Build new pile list
    ResultPiles = [Size : J = 0..3, J != I; NewSize : J = I].

resulting_piles(split, I, 0, A, B, ResultPiles) :-
    move(split, I, 0, A, B),
    % Remove pile I and add A and B
    ResultPiles = [Size : J = 0..3, J != I; A; B].

% Check if all piles in resulting state have different sizes
valid_result(ResultPiles) :-
    % For each pair of piles, they must be different
    % We'll use a constraint
    true.

% Actually, let's use a different approach: directly compute nim-sum and check uniqueness

% For each move, compute the resulting nim-sum
% We need to compute XOR of all pile sizes in resulting state

% Let's define a helper to compute XOR of a list
% We'll use a recursive definition
xor_list([], 0).
xor_list([X], X).
xor_list([X, Y | Rest], Result) :-
    xor_list([X xor Y | Rest], Result).

% But Clingo doesn't support xor operator directly in lists
% Let's use a different approach: compute XOR step by step

% Define the resulting piles explicitly for each move
% For standard move on pile I removing N stones:
result_pile(standard, I, N, 0, 0, J, Size) :-
    move(standard, I, N, 0, 0),
    pile(J, Size),
    J != I.

result_pile(standard, I, N, 0, 0, I, NewSize) :-
    move(standard, I, N, 0, 0),
    pile(I, Size),
    NewSize = Size - N.

% For split move on pile I into A and B:
result_pile(split, I, 0, A, B, J, Size) :-
    move(split, I, 0, A, B),
    pile(J, Size),
    J != I.

result_pile(split, I, 0, A, B, 4, A) :-
    move(split, I, 0, A, B).

result_pile(split, I, 0, A, B, 5, B) :-
    move(split, I, 0, A, B).

% Now compute nim-sum of resulting piles
% We'll compute XOR of all pile sizes in resulting state
nim_sum_result(MoveType, I, N, A, B, Sum) :-
    % Get all pile sizes in resulting state
    % We need to XOR them together
    % Let's use a different approach: compute XOR iteratively
    true.

% Actually, let's simplify: compute nim-sum directly for each move type

% For standard move: nim-sum = (original nim-sum) XOR (original pile size) XOR (new pile size)
% Original nim-sum: 6 XOR 7 XOR 10 XOR 13 = ?
% Let's compute: 6 = 110, 7 = 111, 10 = 1010, 13 = 1101
% 6 XOR 7 = 001 (1)
% 1 XOR 10 = 1011 (11)
% 11 XOR 13 = 0110 (6)
% So initial nim-sum = 6

% For standard move on pile I removing N stones:
% New nim-sum = 6 XOR pile(I) XOR (pile(I) - N)
% = 6 XOR (pile(I) XOR (pile(I) - N))
% = 6 XOR N (since pile(I) XOR (pile(I) - N) = N when removing N stones? Not exactly)

% Actually, let's compute directly:
% nim_sum after move = XOR of all resulting pile sizes

% Let's define a direct computation for each move

% First, compute initial nim-sum
initial_nim_sum(6).  % Computed manually: 6 XOR 7 XOR 10 XOR 13 = 6

% For standard move on pile I removing N stones:
% New pile sizes: same as original except pile I becomes (size - N)
% New nim-sum = initial_nim_sum XOR original_size XOR new_size
% = 6 XOR size XOR (size - N)
% = 6 XOR N (since size XOR (size - N) = N when N ≤ size? Not exactly)

% Let's compute properly:
% For pile 0 (size 6): removing N stones → new size = 6 - N
% New nim-sum = 6 XOR 6 XOR (6 - N) = 6 XOR (6 - N) XOR 6 = (6 - N) XOR 6 XOR 6 = 6 - N
% Wait, that's not right. Let me recalculate:
% Original piles: [6, 7, 10, 13]
% After removing N from pile 0: [6-N, 7, 10, 13]
% New nim-sum = (6-N) XOR 7 XOR 10 XOR 13
% = (6-N) XOR (7 XOR 10 XOR 13)
% = (6-N) XOR (7 XOR 10 XOR 13)
% 7 XOR 10 = 13, 13 XOR 13 = 0
% So new nim-sum = (6-N) XOR 0 = 6-N

% For pile 1 (size 7): removing N stones → new size = 7 - N
% New nim-sum = 6 XOR 7 XOR (7 - N) = 6 XOR N (since 7 XOR (7-N) = N? Not exactly)

% Let's compute 7 XOR (7-N):
% If N=1: 7 XOR 6 = 1
% If N=2: 7 XOR 5 = 2
% If N=3: 7 XOR 4 = 3
% If N=4: 7 XOR 3 = 4
% If N=5: 7 XOR 2 = 5
% If N=6: 7 XOR 1 = 6
% So 7 XOR (7-N) = N for N=1..6? Let's check:
% 7 XOR 6 = 1 (yes)
% 7 XOR 5 = 2 (yes)
% 7 XOR 4 = 3 (yes)
% 7 XOR 3 = 4 (yes)
% 7 XOR 2 = 5 (yes)
% 7 XOR 1 = 6 (yes)
% So yes, 7 XOR (7-N) = N for N=1..6

% Therefore, for pile 1: new nim-sum = 6 XOR N

% For pile 2 (size 10): removing N stones → new size = 10 - N
% New nim-sum = 6 XOR 10 XOR (10 - N)
% 10 XOR (10-N) = N for N=1..9? Let's check:
% 10 XOR 9 = 3 (not 1)
% So not equal to N. Let's compute directly:
% 10 XOR 9 = 3, 10 XOR 8 = 2, 10 XOR 7 = 13, etc.

% For pile 3 (size 13): removing N stones → new size = 13 - N
% New nim-sum = 6 XOR 13 XOR (13 - N)

% This is getting complicated. Let's use a different approach in ASP.

% Let's define the problem more directly in ASP.

% Define piles as facts
pile(0, 6).
pile(1, 7).
pile(2, 10).
pile(3, 13).

% Define possible standard moves
{ remove(I, N) : N = 1..Size } :- pile(I, Size).

% Define possible split moves (only for even piles)
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
   (A = SizeJ ; B = SizeJ).

% Also, the two new piles from split must be different
:- split(I, A, B), A = B.

% Compute nim-sum after move
% We'll compute XOR of all pile sizes after move

% For standard move:
% New piles: same as original except pile I becomes (Size - N)
% Nim-sum = XOR of all pile sizes

% Let's define a helper to compute XOR of two numbers
% We'll use a table for small numbers
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

% Compute nim-sum after standard move
nim_sum_after_standard(I, N, Result) :-
    remove(I, N),
    pile(0, S0), pile(1, S1), pile(2, S2), pile(3, S3),
    % Compute new size for pile I
    NewSize = S_I - N where pile(I, S_I),
    % Compute XOR of all piles
    % For I=0: [NewSize, S1, S2, S3]
    % For I=1: [S0, NewSize, S2, S3]
    % etc.
    % We'll handle each case separately
    I = 0, xor4(NewSize, S1, S2, S3, Result)
    ; I = 1, xor4(S0, NewSize, S2, S3, Result)
    ; I = 2, xor4(S0, S1, NewSize, S3, Result)
    ; I = 3, xor4(S0, S1, S2, NewSize, Result).

% Compute nim-sum after split move
nim_sum_after_split(I, A, B, Result) :-
    split(I, A, B),
    pile(0, S0), pile(1, S1), pile(2, S2), pile(3, S3),
    % For split, we remove pile I and add A and B
    % So we have 5 piles: original 4 minus I plus A and B
    % We need to compute XOR of these 5 values
    % For I=0: [S1, S2, S3, A, B]
    % For I=1: [S0, S2, S3, A, B]
    % etc.
    % We'll compute XOR of 5 values
    I = 0, xor5(S1, S2, S3, A, B, Result)
    ; I = 1, xor5(S0, S2, S3, A, B, Result)
    ; I = 2, xor5(S0, S1, S3, A, B, Result)
    ; I = 3, xor5(S0, S1, S2, A, B, Result).

% Helper for XOR of 5 values
xor5(X, Y, Z, W, V, Result) :-
    xor_val(X, Y, Temp1),
    xor_val(Temp1, Z, Temp2),
    xor_val(Temp2, W, Temp3),
    xor_val(Temp3, V, Result).

% A move is optimal if resulting nim-sum is 0
optimal_standard(I, N) :-
    remove(I, N),
    nim_sum_after_standard(I, N, 0).

optimal_split(I, A, B) :-
    split(I, A, B),
    nim_sum_after_split(I, A, B, 0).

% Show results
#show optimal_standard/2.
#show optimal_split/3.
#show initial_nim_sum/1.
#show is_winning_position/0.

% Compute initial nim-sum
initial_nim_sum(Result) :-
    pile(0, S0), pile(1, S1), pile(2, S2), pile(3, S3),
    xor4(S0, S1, S2, S3, Result).

% Winning position if nim-sum is non-zero
is_winning_position :- initial_nim_sum(S), S != 0.