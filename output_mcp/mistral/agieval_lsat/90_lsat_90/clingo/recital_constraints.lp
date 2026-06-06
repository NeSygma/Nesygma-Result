% Define the domain
solo(1..5).
pianist(wayne; zara).
piece_type(modern; traditional).

% Define consecutive pairs
consecutive_pair(1,2).
consecutive_pair(2,3).
consecutive_pair(3,4).
consecutive_pair(4,5).

% Helper predicate: before(J, I) means solo J is before solo I
before(J, I) :- consecutive_pair(J, I).
before(J, I) :- before(J, K), consecutive_pair(K, I).

% Assignments
1 { performs(P, S) : pianist(P) } 1 :- solo(S).
piece_type(S, modern) | piece_type(S, traditional) :- solo(S).

% Constraints
% 1. The third solo is a traditional piece.
piece_type(3, traditional).

% 2. Exactly one pair of consecutive solos are both traditional.
num_consecutive_traditional(N) :-
    N = #count { I,J : consecutive_pair(I,J), piece_type(I, traditional), piece_type(J, traditional) }.
:- num_consecutive_traditional(N), N != 1.

% 3. In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece.
:- piece_type(4, traditional), not performs(wayne, 4).
:- piece_type(4, modern), not performs(zara, 4).

% 4. The pianist who performs the second solo does not perform the fifth solo.
:- performs(P, 2), performs(P, 5).

% 5. No traditional piece is performed until Wayne performs at least one modern piece.
% For every solo I with a traditional piece, there must exist a solo J < I where Wayne performs a modern piece.
:- piece_type(I, traditional),
   not (performs(wayne, J), piece_type(J, modern), before(J, I)).

% Additional condition for the question: The pianist who performs the first solo also performs the second solo.
same_pianist_first_second :- performs(P, 1), performs(P, 2).

% Map the correct answer to option/1 (MANDATORY)
% (A) Zara performs the first solo.
option(a) :- same_pianist_first_second, performs(zara, 1).

% (B) Wayne performs the third solo.
option(b) :- same_pianist_first_second, performs(wayne, 3).

% (C) Zara performs the fifth solo.
option(c) :- same_pianist_first_second, performs(zara, 5).

% (D) The second solo is a traditional piece.
option(d) :- same_pianist_first_second, piece_type(2, traditional).

% (E) The fourth solo is a modern piece.
option(e) :- same_pianist_first_second, piece_type(4, modern).

#show option/1.