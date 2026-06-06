% Domain
solo(1..5).
pianist(wayne; zara).
piece_type(modern; traditional).

% Choice rules for the actual assignment
1 { pianist(S, P) : pianist(P) } 1 :- solo(S).
1 { piece_type(S, T) : piece_type(T) } 1 :- solo(S).

% Constraint 1: The third solo is a traditional piece.
:- piece_type(3, modern).

% Constraint 2: Exactly two of the traditional pieces are performed consecutively.
% This means exactly one pair of consecutive traditional pieces, and no three consecutive.
consecutive_traditional_pair(I) :-
    piece_type(I, traditional),
    piece_type(I+1, traditional),
    solo(I),
    solo(I+1).
:- 2 { I : consecutive_traditional_pair(I) }.
:- piece_type(I, traditional), piece_type(I+1, traditional), piece_type(I+2, traditional).

% Constraint 3: In solo 4, Wayne performs traditional OR Zara performs modern
:- pianist(4, wayne), piece_type(4, modern).
:- pianist(4, zara), piece_type(4, traditional).

% Constraint 4: Pianist of solo 2 ≠ pianist of solo 5
:- pianist(2, P), pianist(5, P).

% Constraint 5: No traditional piece is performed until Wayne performs at least one modern piece
% Helper: Wayne has performed a modern piece by solo S
wayne_modern_before(S) :-
    pianist(T, wayne),
    piece_type(T, modern),
    T < S,
    solo(S).

% No traditional piece before Wayne's first modern piece
:- piece_type(S, traditional),
   not wayne_modern_before(S).

% Define which answer choices are possible given the constraints
% (A) the first, third, and fourth
possible_A :- piece_type(1, traditional), piece_type(3, traditional), piece_type(4, traditional),
              not piece_type(2, traditional), not piece_type(5, traditional).
% (B) the second, third, and fourth
possible_B :- piece_type(2, traditional), piece_type(3, traditional), piece_type(4, traditional),
              not piece_type(1, traditional), not piece_type(5, traditional).
% (C) the third and fourth
possible_C :- piece_type(3, traditional), piece_type(4, traditional),
              not piece_type(1, traditional), not piece_type(2, traditional), not piece_type(5, traditional).
% (D) the third and fifth
possible_D :- piece_type(3, traditional), piece_type(5, traditional),
              not piece_type(1, traditional), not piece_type(2, traditional), not piece_type(4, traditional).
% (E) the fourth and fifth
possible_E :- piece_type(4, traditional), piece_type(5, traditional),
              not piece_type(1, traditional), not piece_type(2, traditional), not piece_type(3, traditional).

% Map to option/1
option(a) :- possible_A.
option(b) :- possible_B.
option(c) :- possible_C.
option(d) :- possible_D.
option(e) :- possible_E.

#show option/1.

% Sentinel to confirm satisfiability
solution_exists :- option(_).
#show solution_exists/0.