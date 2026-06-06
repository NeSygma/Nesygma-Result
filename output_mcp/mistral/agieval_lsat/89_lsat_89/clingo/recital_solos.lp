% Define the domain
solo(1..5).
pianist(wayne; zara).
piece_type(modern; traditional).

% Assign pianists to solos (exactly one pianist per solo)
{ assigned_pianist(S, P) : pianist(P) } = 1 :- solo(S).

% Assign piece types to solos (exactly one type per solo)
{ assigned_piece(S, T) : piece_type(T) } = 1 :- solo(S).

% Constraint 1: The third solo is a traditional piece
:- not assigned_piece(3, traditional).

% Constraint 2: Exactly two of the traditional pieces are performed consecutively
% Define consecutive traditional solos
consecutive_traditional(S) :- 
    assigned_piece(S, traditional),
    assigned_piece(S+1, traditional),
    solo(S), solo(S+1).

% There should be exactly one such pair
:- 2 { consecutive_traditional(S) : solo(S) }.

% Constraint 3: In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece
% This translates to:
% - If Wayne is the pianist for solo 4, then the piece must be traditional
% - If Zara is the pianist for solo 4, then the piece must be modern
:- assigned_pianist(4, wayne), not assigned_piece(4, traditional).
:- assigned_pianist(4, zara), not assigned_piece(4, modern).

% Constraint 4: The pianist who performs the second solo does not perform the fifth solo
:- assigned_pianist(2, P), assigned_pianist(5, P).

% Constraint 5: No traditional piece is performed until Wayne performs at least one modern piece
% Define helper: wayne_has_modern_before(S) means there is a solo T < S where Wayne performs a modern piece
wayne_has_modern_before(S) :- 
    assigned_piece(T, modern),
    assigned_pianist(T, wayne),
    T < S,
    solo(S).

% Wayne must have performed at least one modern piece before any traditional piece
:- assigned_piece(S, traditional), not wayne_has_modern_before(S).

% Count the number of solos where Wayne performs a traditional piece
wayne_traditional(S) :- 
    assigned_pianist(S, wayne),
    assigned_piece(S, traditional).

wayne_traditional_count(N) :- 
    N = #count{ S : wayne_traditional(S) }.

% Find the minimum count of Wayne's traditional performances
% We use a minimize statement to find the smallest N
#minimize{ N : wayne_traditional_count(N) }.

% Derive the minimum value and map to answer choices
% We need to ensure that the minimum N is derived and shown
% Since #minimize does not produce an atom, we derive the minimum N explicitly

% Helper to find the minimum N
possible_min(N) :- wayne_traditional_count(N), not { wayne_traditional_count(M) : M < N }.

% Map the minimum N to the answer choices
option(a) :- possible_min(0).
option(b) :- possible_min(1).
option(c) :- possible_min(2).
option(d) :- possible_min(3).
option(e) :- possible_min(4).

#show option/1.