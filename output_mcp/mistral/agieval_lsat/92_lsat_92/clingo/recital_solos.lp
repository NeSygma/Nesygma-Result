% Domains
solo(1..5).
pianist(wayne; zara).
piece_type(modern; traditional).

% Assign pianist to each solo
1 { assigned(P, S) : pianist(P) } 1 :- solo(S).

% Assign piece type to each solo
1 { piece(S, T) : piece_type(T) } 1 :- solo(S).

% Constraint 1: The third solo is a traditional piece.
piece(3, traditional).

% Constraint 2: Exactly two traditional pieces, and they are consecutive
:- 2 != #count { S : piece(S, traditional) }.
:- 1 != #count { S : piece(S, traditional), piece(S+1, traditional), solo(S), solo(S+1) }.

% Constraint 3: In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece.
:- assigned(wayne, 4), not piece(4, traditional).
:- assigned(zara, 4), not piece(4, modern).

% Constraint 4: The pianist who performs the second solo does not perform the fifth solo.
:- assigned(P, 2), assigned(P, 5).

% Constraint 5: No traditional piece is performed until Wayne performs at least one modern piece.
% Helper: Wayne performs a modern piece at some solo S2 < S
wayne_modern_before(S) :- piece(S, traditional), assigned(wayne, S2), piece(S2, modern), S2 < S.
:- piece(S, traditional), solo(S), not wayne_modern_before(S).

% Additional constraint from the question: Wayne performs traditional in solo 5
:- not assigned(wayne, 5).
:- not piece(5, traditional).

% Now, we need to check which of the answer choices could be true.
% We'll define conditions for each option:

% (A) Zara performs the first solo.
option(a) :- assigned(zara, 1).

% (B) Wayne performs the second solo.
option(b) :- assigned(wayne, 2).

% (C) Zara performs the third solo.
option(c) :- assigned(zara, 3).

% (D) The second solo is a modern piece.
option(d) :- piece(2, modern).

% (E) The fourth solo is a traditional piece.
option(e) :- piece(4, traditional).

#show option/1.