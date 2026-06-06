% Domains
solo(1..5).
pianist(wayne; zara).
piece(modern; traditional).

% Choice rules: assign pianist and piece type to each solo
1 { assign_pianist(S, P) : pianist(P) } 1 :- solo(S).
1 { assign_piece(S, T) : piece(T) } 1 :- solo(S).

% Condition 1: Solo 3 is traditional
assign_piece(3, traditional).

% Condition 2: Exactly two traditional pieces are consecutive
% Count consecutive pairs of traditional pieces
consecutive_trad(S) :- solo(S), S < 5, assign_piece(S, traditional), assign_piece(S+1, traditional).
count_consecutive(N) :- N = #count { S : consecutive_trad(S) }.
:- count_consecutive(N), N != 2.

% Condition 3: Solo 4: either Wayne performs traditional OR Zara performs modern
:- assign_pianist(4, wayne), assign_piece(4, modern).
:- assign_pianist(4, zara), assign_piece(4, traditional).

% Condition 4: Pianist of solo 2 ≠ pianist of solo 5
:- assign_pianist(2, P), assign_pianist(5, P).

% Condition 5: No traditional piece until Wayne performs at least one modern piece
% This means: if any solo S has traditional piece, then there must exist some solo S' < S where Wayne performs modern
first_trad(S) :- assign_piece(S, traditional), not assign_piece(S-1, traditional), S > 1.
first_trad(1) :- assign_piece(1, traditional).
wayne_modern_before(S) :- solo(S), solo(S'), S' < S, assign_pianist(S', wayne), assign_piece(S', modern).
:- first_trad(S), not wayne_modern_before(S).

% Additional condition: Pianist of solo 1 = pianist of solo 2
:- assign_pianist(1, P1), assign_pianist(2, P2), P1 != P2.

% Helper predicates for answer choices
% A: Zara performs the first solo
zara_first :- assign_pianist(1, zara).

% B: Wayne performs the third solo
wayne_third :- assign_pianist(3, wayne).

% C: Zara performs the fifth solo
zara_fifth :- assign_pianist(5, zara).

% D: The second solo is a traditional piece
second_trad :- assign_piece(2, traditional).

% E: The fourth solo is a modern piece
fourth_modern :- assign_piece(4, modern).

% Map the correct answer to option/1
option(a) :- zara_first.
option(b) :- wayne_third.
option(c) :- zara_fifth.
option(d) :- second_trad.
option(e) :- fourth_modern.

#show option/1.