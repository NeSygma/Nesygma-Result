%% Quantum Nim - Optimal Move Finder
%% Current state: piles [6, 7, 10, 13], Player 1's turn, split power available

%% ========== DOMAINS ==========
pile(0..3).
pile_size(0,6). pile_size(1,7). pile_size(2,10). pile_size(3,13).

%% Possible stone removals: 1 to pile_size
removal(P, N) :- pile(P), pile_size(P, S), N = 1..S.

%% Possible split results for even-sized piles
%% Split an even pile of size S into two non-empty piles A, B where A+B=S, A>=1, B>=1
split_result(P, A, B) :- pile(P), pile_size(P, S), S > 0, S/2 = (S+1)/2, A = 1..S-1, B = S-A, B >= 1.

%% ========== STANDARD MOVES ==========
%% A standard move: remove N stones from pile P
{ standard_move(P, N) : removal(P, N) } 1 :- pile(P).

%% Resulting piles after standard move
%% For the modified pile: new size = old size - N
%% For other piles: unchanged
result_after_standard(P, S-N, P, N) :- standard_move(P, N), pile_size(P, S).
result_after_standard(Q, S, P, N) :- standard_move(P, N), pile(Q), Q != P, pile_size(Q, S).

%% ========== SPLIT POWER MOVES ==========
%% Player 1 can use split power at most once
{ split_used } 1.

%% Split move: split even pile P into A and B
{ split_move(P, A, B) : split_result(P, A, B) } 1 :- pile(P), not split_used.

%% If split is used, mark it
split_used :- split_move(P, A, B).

%% Resulting piles after split move
%% The split pile is replaced by two piles A and B
result_after_split(A, P, A, B) :- split_move(P, A, B).
result_after_split(B, P, A, B) :- split_move(P, A, B).
result_after_split(Q, S, P, A, B) :- split_move(P, A, B), pile(Q), Q != P, pile_size(Q, S).

%% ========== STATE VALIDITY ==========
%% After any move, no two piles can have the same size
%% Collect all resulting pile sizes and ensure uniqueness

%% For standard moves: collect sizes
standard_result_size(S, P, N) :- result_after_standard(_, S, P, N).

%% For split moves: collect sizes
split_result_size(S, P, A, B) :- result_after_split(S, _, P, A, B).

%% Constraint: no duplicate sizes after standard move
:- standard_move(P, N), 
   standard_result_size(S1, P, N), 
   standard_result_size(S2, P, N), 
   S1 = S2,
   result_after_standard(P1, S1, P, N),
   result_after_standard(P2, S2, P, N),
   P1 < P2.

%% Constraint: no duplicate sizes after split move
:- split_move(P, A, B),
   split_result_size(S1, P, A, B),
   split_result_size(S2, P, A, B),
   S1 = S2,
   result_after_split(S1, P1, P, A, B),
   result_after_split(S2, P2, P, A, B),
   P1 < P2.

%% ========== NIM-SUM CALCULATION ==========
%% Compute nim-sum (XOR) of resulting pile sizes
%% We need to compute XOR of all resulting pile sizes

%% For standard moves: XOR of all 4 resulting sizes
%% Represent XOR bit by bit for simplicity
%% Since pile sizes are small (max 20), we can enumerate

%% Helper: binary representation of a number
%% We'll compute XOR by checking each bit position

%% For standard moves: the resulting sizes are the 4 piles after removal
%% We need to compute XOR of these 4 numbers

%% Let's use a different approach: compute XOR directly
%% XOR of numbers a,b,c,d = a xor b xor c xor d

%% We'll enumerate all possible XOR results for standard moves
%% Since numbers are small, we can compute xor as:
%% xor(A,B) = A xor B (bitwise)

%% Define xor for two numbers up to 20
xor_val(0,0,0). xor_val(0,1,1). xor_val(0,2,2). xor_val(0,3,3). xor_val(0,4,4). xor_val(0,5,5). xor_val(0,6,6). xor_val(0,7,7). xor_val(0,8,8). xor_val(0,9,9). xor_val(0,10,10). xor_val(0,11,11). xor_val(0,12,12). xor_val(0,13,13). xor_val(0,14,14). xor_val(0,15,15). xor_val(0,16,16). xor_val(0,17,17). xor_val(0,18,18). xor_val(0,19,19). xor_val(0,20,20).
xor_val(1,0,1). xor_val(1,1,0). xor_val(1,2,3). xor_val(1,3,2). xor_val(1,4,5). xor_val(1,5,4). xor_val(1,6,7). xor_val(1,7,6). xor_val(1,8,9). xor_val(1,9,8). xor_val(1,10,11). xor_val(1,11,10). xor_val(1,12,13). xor_val(1,13,12). xor_val(1,14,15). xor_val(1,15,14). xor_val(1,16,17). xor_val(1,17,16). xor_val(1,18,19). xor_val(1,19,18). xor_val(1,20,21).
xor_val(2,0,2). xor_val(2,1,3). xor_val(2,2,0). xor_val(2,3,1). xor_val(2,4,6). xor_val(2,5,7). xor_val(2,6,4). xor_val(2,7,5). xor_val(2,8,10). xor_val(2,9,11). xor_val(2,10,8). xor_val(2,11,9). xor_val(2,12,14). xor_val(2,13,15). xor_val(2,14,12). xor_val(2,15,13). xor_val(2,16,18). xor_val(2,17,19). xor_val(2,18,16). xor_val(2,19,17). xor_val(2,20,22).
xor_val(3,0,3). xor_val(3,1,2). xor_val(3,2,1). xor_val(3,3,0). xor_val(3,4,7). xor_val(3,5,6). xor_val(3,6,5). xor_val(3,7,4). xor_val(3,8,11). xor_val(3,9,10). xor_val(3,10,9). xor_val(3,11,8). xor_val(3,12,15). xor_val(3,13,14). xor_val(3,14,13). xor_val(3,15,12). xor_val(3,16,19). xor_val(3,17,18). xor_val(3,18,17). xor_val(3,19,16). xor_val(3,20,23).
xor_val(4,0,4). xor_val(4,1,5). xor_val(4,2,6). xor_val(4,3,7). xor_val(4,4,0). xor_val(4,5,1). xor_val(4,6,2). xor_val(4,7,3). xor_val(4,8,12). xor_val(4,9,13). xor_val(4,10,14). xor_val(4,11,15). xor_val(4,12,8). xor_val(4,13,9). xor_val(4,14,10). xor_val(4,15,11). xor_val(4,16,20). xor_val(4,17,21). xor_val(4,18,22). xor_val(4,19,23). xor_val(4,20,16).
xor_val(5,0,5). xor_val(5,1,4). xor_val(5,2,7). xor_val(5,3,6). xor_val(5,4,1). xor_val(5,5,0). xor_val(5,6,3). xor_val(5,7,2). xor_val(5,8,13). xor_val(5,9,12). xor_val(5,10,15). xor_val(5,11,14). xor_val(5,12,9). xor_val(5,13,8). xor_val(5,14,11). xor_val(5,15,10). xor_val(5,16,21). xor_val(5,17,20). xor_val(5,18,23). xor_val(5,19,22). xor_val(5,20,17).
xor_val(6,0,6). xor_val(6,1,7). xor_val(6,2,4). xor_val(6,3,5). xor_val(6,4,2). xor_val(6,5,3). xor_val(6,6,0). xor_val(6,7,1). xor_val(6,8,14). xor_val(6,9,15). xor_val(6,10,12). xor_val(6,11,13). xor_val(6,12,10). xor_val(6,13,11). xor_val(6,14,8). xor_val(6,15,9). xor_val(6,16,22). xor_val(6,17,23). xor_val(6,18,20). xor_val(6,19,21). xor_val(6,20,18).
xor_val(7,0,7). xor_val(7,1,6). xor_val(7,2,5). xor_val(7,3,4). xor_val(7,4,3). xor_val(7,5,2). xor_val(7,6,1). xor_val(7,7,0). xor_val(7,8,15). xor_val(7,9,14). xor_val(7,10,13). xor_val(7,11,12). xor_val(7,12,11). xor_val(7,13,10). xor_val(7,14,9). xor_val(7,15,8). xor_val(7,16,23). xor_val(7,17,22). xor_val(7,18,21). xor_val(7,19,20). xor_val(7,20,19).
xor_val(8,0,8). xor_val(8,1,9). xor_val(8,2,10). xor_val(8,3,11). xor_val(8,4,12). xor_val(8,5,13). xor_val(8,6,14). xor_val(8,7,15). xor_val(8,8,0). xor_val(8,9,1). xor_val(8,10,2). xor_val(8,11,3). xor_val(8,12,4). xor_val(8,13,5). xor_val(8,14,6). xor_val(8,15,7). xor_val(8,16,24). xor_val(8,17,25). xor_val(8,18,26). xor_val(8,19,27). xor_val(8,20,28).
xor_val(9,0,9). xor_val(9,1,8). xor_val(9,2,11). xor_val(9,3,10). xor_val(9,4,13). xor_val(9,5,12). xor_val(9,6,15). xor_val(9,7,14). xor_val(9,8,1). xor_val(9,9,0). xor_val(9,10,3). xor_val(9,11,2). xor_val(9,12,5). xor_val(9,13,4). xor_val(9,14,7). xor_val(9,15,6). xor_val(9,16,25). xor_val(9,17,24). xor_val(9,18,27). xor_val(9,19,26). xor_val(9,20,29).
xor_val(10,0,10). xor_val(10,1,11). xor_val(10,2,8). xor_val(10,3,9). xor_val(10,4,14). xor_val(10,5,15). xor_val(10,6,12). xor_val(10,7,13). xor_val(10,8,2). xor_val(10,9,3). xor_val(10,10,0). xor_val(10,11,1). xor_val(10,12,6). xor_val(10,13,7). xor_val(10,14,4). xor_val(10,15,5). xor_val(10,16,26). xor_val(10,17,27). xor_val(10,18,24). xor_val(10,19,25). xor_val(10,20,30).
xor_val(11,0,11). xor_val(11,1,10). xor_val(11,2,9). xor_val(11,3,8). xor_val(11,4,15). xor_val(11,5,14). xor_val(11,6,13). xor_val(11,7,12). xor_val(11,8,3). xor_val(11,9,2). xor_val(11,10,1). xor_val(11,11,0). xor_val(11,12,7). xor_val(11,13,6). xor_val(11,14,5). xor_val(11,15,4). xor_val(11,16,27). xor_val(11,17,26). xor_val(11,18,25). xor_val(11,19,24). xor_val(11,20,31).
xor_val(12,0,12). xor_val(12,1,13). xor_val(12,2,14). xor_val(12,3,15). xor_val(12,4,8). xor_val(12,5,9). xor_val(12,6,10). xor_val(12,7,11). xor_val(12,8,4). xor_val(12,9,5). xor_val(12,10,6). xor_val(12,11,7). xor_val(12,12,0). xor_val(12,13,1). xor_val(12,14,2). xor_val(12,15,3). xor_val(12,16,28). xor_val(12,17,29). xor_val(12,18,30). xor_val(12,19,31). xor_val(12,20,24).
xor_val(13,0,13). xor_val(13,1,12). xor_val(13,2,15). xor_val(13,3,14). xor_val(13,4,9). xor_val(13,5,8). xor_val(13,6,11). xor_val(13,7,10). xor_val(13,8,5). xor_val(13,9,4). xor_val(13,10,7). xor_val(13,11,6). xor_val(13,12,1). xor_val(13,13,0). xor_val(13,14,3). xor_val(13,15,2). xor_val(13,16,29). xor_val(13,17,28). xor_val(13,18,31). xor_val(13,19,30). xor_val(13,20,25).
xor_val(14,0,14). xor_val(14,1,15). xor_val(14,2,12). xor_val(14,3,13). xor_val(14,4,10). xor_val(14,5,11). xor_val(14,6,8). xor_val(14,7,9). xor_val(14,8,6). xor_val(14,9,7). xor_val(14,10,4). xor_val(14,11,5). xor_val(14,12,2). xor_val(14,13,3). xor_val(14,14,0). xor_val(14,15,1). xor_val(14,16,30). xor_val(14,17,31). xor_val(14,18,28). xor_val(14,19,29). xor_val(14,20,26).
xor_val(15,0,15). xor_val(15,1,14). xor_val(15,2,13). xor_val(15,3,12). xor_val(15,4,11). xor_val(15,5,10). xor_val(15,6,9). xor_val(15,7,8). xor_val(15,8,7). xor_val(15,9,6). xor_val(15,10,5). xor_val(15,11,4). xor_val(15,12,3). xor_val(15,13,2). xor_val(15,14,1). xor_val(15,15,0). xor_val(15,16,31). xor_val(15,17,30). xor_val(15,18,29). xor_val(15,19,28). xor_val(15,20,27).
xor_val(16,0,16). xor_val(16,1,17). xor_val(16,2,18). xor_val(16,3,19). xor_val(16,4,20). xor_val(16,5,21). xor_val(16,6,22). xor_val(16,7,23). xor_val(16,8,24). xor_val(16,9,25). xor_val(16,10,26). xor_val(16,11,27). xor_val(16,12,28). xor_val(16,13,29). xor_val(16,14,30). xor_val(16,15,31). xor_val(16,16,0). xor_val(16,17,1). xor_val(16,18,2). xor_val(16,19,3). xor_val(16,20,4).
xor_val(17,0,17). xor_val(17,1,16). xor_val(17,2,19). xor_val(17,3,18). xor_val(17,4,21). xor_val(17,5,20). xor_val(17,6,23). xor_val(17,7,22). xor_val(17,8,25). xor_val(17,9,24). xor_val(17,10,27). xor_val(17,11,26). xor_val(17,12,29). xor_val(17,13,28). xor_val(17,14,31). xor_val(17,15,30). xor_val(17,16,1). xor_val(17,17,0). xor_val(17,18,3). xor_val(17,19,2). xor_val(17,20,5).
xor_val(18,0,18). xor_val(18,1,19). xor_val(18,2,16). xor_val(18,3,17). xor_val(18,4,22). xor_val(18,5,23). xor_val(18,6,20). xor_val(18,7,21). xor_val(18,8,26). xor_val(18,9,27). xor_val(18,10,24). xor_val(18,11,25). xor_val(18,12,30). xor_val(18,13,31). xor_val(18,14,28). xor_val(18,15,29). xor_val(18,16,2). xor_val(18,17,3). xor_val(18,18,0). xor_val(18,19,1). xor_val(18,20,6).
xor_val(19,0,19). xor_val(19,1,18). xor_val(19,2,17). xor_val(19,3,16). xor_val(19,4,23). xor_val(19,5,22). xor_val(19,6,21). xor_val(19,7,20). xor_val(19,8,27). xor_val(19,9,26). xor_val(19,10,25). xor_val(19,11,24). xor_val(19,12,31). xor_val(19,13,30). xor_val(19,14,29). xor_val(19,15,28). xor_val(19,16,3). xor_val(19,17,2). xor_val(19,18,1). xor_val(19,19,0). xor_val(19,20,7).
xor_val(20,0,20). xor_val(20,1,21). xor_val(20,2,22). xor_val(20,3,23). xor_val(20,4,16). xor_val(20,5,17). xor_val(20,6,18). xor_val(20,7,19). xor_val(20,8,28). xor_val(20,9,29). xor_val(20,10,30). xor_val(20,11,31). xor_val(20,12,24). xor_val(20,13,25). xor_val(20,14,26). xor_val(20,15,27). xor_val(20,16,4). xor_val(20,17,5). xor_val(20,18,6). xor_val(20,19,7). xor_val(20,20,0).

%% Compute XOR of 4 numbers using pairwise XOR
xor3(A,B,C,R) :- xor_val(A,B,X), xor_val(X,C,R).
xor4(A,B,C,D,R) :- xor_val(A,B,X), xor_val(X,C,Y), xor_val(Y,D,R).

%% Standard move nim-sum
standard_nim_sum(P, N, R) :- standard_move(P, N), 
    result_after_standard(P0, S0, P, N),
    result_after_standard(P1, S1, P, N),
    result_after_standard(P2, S2, P, N),
    result_after_standard(P3, S3, P, N),
    P0 = 0, P1 = 1, P2 = 2, P3 = 3,
    xor4(S0, S1, S2, S3, R).

%% Split move nim-sum (5 piles after split)
%% XOR of 5 numbers: compute pairwise
xor5(A,B,C,D,E,R) :- xor_val(A,B,X1), xor_val(X1,C,X2), xor_val(X2,D,X3), xor_val(X3,E,R).

split_nim_sum(P, A, B, R) :- split_move(P, A, B),
    result_after_split(S0, P0, P, A, B),
    result_after_split(S1, P1, P, A, B),
    result_after_split(S2, P2, P, A, B),
    result_after_split(S3, P3, P, A, B),
    result_after_split(S4, P4, P, A, B),
    P0 = 0, P1 = 1, P2 = 2, P3 = 3, P4 = 4,
    xor5(S0, S1, S2, S3, S4, R).

%% ========== OPTIMALITY ==========
%% A move is optimal if it results in nim-sum = 0
optimal_standard(P, N) :- standard_move(P, N), standard_nim_sum(P, N, 0).
optimal_split(P, A, B) :- split_move(P, A, B), split_nim_sum(P, A, B, 0).

%% ========== OUTPUT ==========
%% Initial nim-sum
initial_nim_sum(R) :- xor4(6,7,10,13,R).

%% Is winning position
is_winning_position :- initial_nim_sum(R), R != 0.

%% Show optimal moves
#show initial_nim_sum/1.
#show is_winning_position.
#show optimal_standard/2.
#show optimal_split/3.