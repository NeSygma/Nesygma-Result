% Domains
solo(1..5).
pianist(wayne; zara).
piece_type(modern; traditional).

% Base facts from problem and question
piece_type(3, traditional).  % The third solo is a traditional piece.
piece_type(5, traditional).  % Condition from the question: fifth solo is traditional

% Exactly two traditional pieces, and they are consecutive
% Since solo 3 and 5 are traditional, the only possible consecutive pair is (2,3)
piece_type(2, traditional).
piece_type(1, modern).
piece_type(4, modern).

% Constraint 5: No traditional piece is performed until Wayne performs at least one modern piece.
% This means: for any solo S with traditional piece, there must be a previous solo where Wayne performs modern.
% Since solo 2 is the first traditional piece, solo 1 must be Wayne playing modern.
assigned_pianist(1, wayne).

% Constraint 3: In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece.
% Since solo 4 is modern, we must have Zara as the pianist.
assigned_pianist(4, zara).

% Constraint 4: The pianist who performs the second solo does not perform the fifth solo.
:- assigned_pianist(2, P), assigned_pianist(5, P).

% Choice rules for remaining solos (2, 3, 5)
{ assigned_pianist(2, P) : pianist(P) } = 1.
{ assigned_pianist(3, P) : pianist(P) } = 1.
{ assigned_pianist(5, P) : pianist(P) } = 1.

% Constraint: Solo 1 must be modern (already set) and Solo 1 must be Wayne (already set)
% piece_type(1, modern) is already set above.

% Verify constraint 5 is satisfied by construction (Wayne plays modern in solo 1 before traditional in solo 2)

% Count how many solos have a completely determined pianist
% A solo S has a determined pianist if in all answer sets, assigned_pianist(S, P) is fixed for exactly one P.

% We can derive this by checking if the choice is forced by constraints.

% Solo 1 is determined (wayne)
determined_pianist(1) :- assigned_pianist(1, wayne).

% Solo 4 is determined (zara)
determined_pianist(4) :- assigned_pianist(4, zara).

% For solos 2, 3, 5: they are not determined because both pianists are possible in different models.

% Count the number of determined solos
num_determined(N) :- N = #count{ S : determined_pianist(S) }.

% Map the count to answer choices
option(a) :- num_determined(1).
option(b) :- num_determined(2).
option(c) :- num_determined(3).
option(d) :- num_determined(4).
option(e) :- num_determined(5).

#show option/1.