% === Pile data ===
pile(0, 6).
pile(1, 7).
pile(2, 10).
pile(3, 13).

% === Even piles (eligible for split) ===
even(0). even(2).

% === Possible standard moves: remove N stones from pile P ===
possible_std(P, N) :- pile(P, S), N = 1..S.

% === Possible split moves: split even pile P into (A,B), A<B, A+B=S ===
possible_spl(P, A, B) :- even(P), pile(P, S), A = 1..S-1, B = 1..S-1, A + B = S, A < B.

% === Choice: select exactly one move ===
1 { do_std(P, N) : possible_std(P, N); do_spl(P, A, B) : possible_spl(P, A, B) } 1.

% === Resulting pile sizes after a standard move ===
result_pile(Q, S) :- do_std(P, _), pile(Q, S), Q != P.
result_pile(P, R) :- do_std(P, N), pile(P, S), R = S - N, R > 0.

% === Resulting pile sizes after a split move ===
result_pile(Q, S) :- do_spl(P, _, _), pile(Q, S), Q != P.
result_pile(4, A) :- do_spl(P, A, B).
result_pile(5, B) :- do_spl(P, A, B).

% === Constraint: all resulting pile sizes must be distinct ===
:- result_pile(I1, S), result_pile(I2, S), I1 < I2.

% === Precompute bit representations for all possible sizes 0..13 ===
% bit(S, B, V) means: in binary representation of S, bit position B has value V
bit_pos(0). bit_pos(1). bit_pos(2). bit_pos(3).

% Size 0: 0000
bit(0, 0, 0). bit(0, 1, 0). bit(0, 2, 0). bit(0, 3, 0).
% Size 1: 0001
bit(1, 0, 1). bit(1, 1, 0). bit(1, 2, 0). bit(1, 3, 0).
% Size 2: 0010
bit(2, 0, 0). bit(2, 1, 1). bit(2, 2, 0). bit(2, 3, 0).
% Size 3: 0011
bit(3, 0, 1). bit(3, 1, 1). bit(3, 2, 0). bit(3, 3, 0).
% Size 4: 0100
bit(4, 0, 0). bit(4, 1, 0). bit(4, 2, 1). bit(4, 3, 0).
% Size 5: 0101
bit(5, 0, 1). bit(5, 1, 0). bit(5, 2, 1). bit(5, 3, 0).
% Size 6: 0110
bit(6, 0, 0). bit(6, 1, 1). bit(6, 2, 1). bit(6, 3, 0).
% Size 7: 0111
bit(7, 0, 1). bit(7, 1, 1). bit(7, 2, 1). bit(7, 3, 0).
% Size 8: 1000
bit(8, 0, 0). bit(8, 1, 0). bit(8, 2, 0). bit(8, 3, 1).
% Size 9: 1001
bit(9, 0, 1). bit(9, 1, 0). bit(9, 2, 0). bit(9, 3, 1).
% Size 10: 1010
bit(10, 0, 0). bit(10, 1, 1). bit(10, 2, 0). bit(10, 3, 1).
% Size 11: 1011
bit(11, 0, 1). bit(11, 1, 1). bit(11, 2, 0). bit(11, 3, 1).
% Size 12: 1100
bit(12, 0, 0). bit(12, 1, 0). bit(12, 2, 1). bit(12, 3, 1).
% Size 13: 1101
bit(13, 0, 1). bit(13, 1, 0). bit(13, 2, 1). bit(13, 3, 1).

% === Nim-sum computation for resulting position ===
pile_bit(I, B, V) :- result_pile(I, S), bit(S, B, V).

% Count how many piles have bit B set
bit_set_count(B, C) :- C = #count { I : pile_bit(I, B, 1) }, bit_pos(B).

% XOR bit B is 1 if odd number of piles have it set
xor_bit(B) :- bit_set_count(B, C), C \ 2 = 1, C > 0.

% === Optimality: nim-sum must be 0 (no XOR bits set) ===
:- xor_bit(_).

% === Initial nim-sum computation ===
init_pile_bit(I, B, V) :- pile(I, S), bit(S, B, V).
init_bit_set_count(B, C) :- C = #count { I : init_pile_bit(I, B, 1) }, bit_pos(B).
init_xor_bit(B) :- init_bit_set_count(B, C), C \ 2 = 1, C > 0.

% Compute initial nim-sum value
bit_weight(0, 1). bit_weight(1, 2). bit_weight(2, 4). bit_weight(3, 8).
init_bit_val(B, 1) :- init_xor_bit(B).
init_bit_val(B, 0) :- bit_pos(B), not init_xor_bit(B).

initial_nim_sum(S) :- S = #sum { V * W : init_bit_val(B, V), bit_weight(B, W) }.

is_winning_position :- initial_nim_sum(S), S > 0.

% === Collect resulting sizes for display ===
result_size(S) :- result_pile(_, S).

% === Output ===
#show initial_nim_sum/1.
#show is_winning_position/0.
#show do_std/2.
#show do_spl/3.
#show result_pile/2.
#show result_size/1.