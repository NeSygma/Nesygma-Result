% Base facts and domains
solo(1..5).
pianist(wayne; zara).
piece_type(modern; traditional).

% Assign pianist and piece type to each solo
1 { assigned_pianist(S, P) : pianist(P) } 1 :- solo(S).
1 { assigned_piece(S, T) : piece_type(T) } 1 :- solo(S).

% Constraints from the problem statement

% The third solo is a traditional piece.
:- assigned_piece(3, modern).

% Exactly two of the traditional pieces are performed consecutively.
consecutive_traditional(S) :- assigned_piece(S, traditional), assigned_piece(S+1, traditional), solo(S), solo(S+1).
:- #count{S : consecutive_traditional(S)} != 1.

% In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece.
:- assigned_pianist(4, wayne), assigned_piece(4, modern).
:- assigned_pianist(4, zara), assigned_piece(4, traditional).

% The pianist who performs the second solo does not perform the fifth solo.
:- assigned_pianist(2, P), assigned_pianist(5, P), pianist(P).

% No traditional piece is performed until Wayne performs at least one modern piece.
% This means the first traditional piece must occur after Wayne's first modern piece.
first_traditional(S) :- assigned_piece(S, traditional), solo(S), not assigned_piece(T, traditional) : solo(T), T < S.
first_modern_wayne(S) :- assigned_pianist(S, wayne), assigned_piece(S, modern), solo(S), not assigned_piece(T, modern) : solo(T), T < S.
:- first_traditional(S), not first_modern_wayne(T) : solo(T), T < S.

% Additional constraint: If the pianist who performs the first solo also performs the second solo
same_pianist_first_second :- assigned_pianist(1, P), assigned_pianist(2, P), pianist(P).

% Derive the correct answer based on the condition
% (A) Zara performs the first solo.
option(a) :- same_pianist_first_second, assigned_pianist(1, zara).

% (B) Wayne performs the third solo.
option(b) :- same_pianist_first_second, assigned_pianist(3, wayne).

% (C) Zara performs the fifth solo.
option(c) :- same_pianist_first_second, assigned_pianist(5, zara).

% (D) The second solo is a traditional piece.
option(d) :- same_pianist_first_second, assigned_piece(2, traditional).

% (E) The fourth solo is a modern piece.
option(e) :- same_pianist_first_second, assigned_piece(4, modern).

% Ensure only one option is true at a time
:- option(X), option(Y), X != Y.

#show option/1.