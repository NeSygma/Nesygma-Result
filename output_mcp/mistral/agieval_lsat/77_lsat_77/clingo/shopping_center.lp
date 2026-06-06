% Spaces
space(1..7).

% Business types
business(optometrist; pharmacy; restaurant; shoe_store; toy_store; veterinarian).

% Shoe store is in space 2 (given in the question)
assigned(2, shoe_store).

% Each space has exactly one business
1 { assigned(S, B) : business(B) } 1 :- space(S).

% Pharmacy must be at one end (space 1 or 7)
assigned(1, pharmacy) | assigned(7, pharmacy).

% Restaurant must be at the other end
:- assigned(1, pharmacy), not assigned(7, restaurant).
:- assigned(7, pharmacy), not assigned(1, restaurant).

% Pharmacy must be next to optometrist or veterinarian
:- assigned(1, pharmacy), not assigned(2, optometrist), not assigned(2, veterinarian).
:- assigned(7, pharmacy), not assigned(6, optometrist), not assigned(6, veterinarian).

% Adjacency relation
adjacent(S, S1) :- S = S1 + 1, space(S), space(S1).
adjacent(S, S1) :- S = S1 - 1, space(S), space(S1).

% Toy store cannot be next to veterinarian
:- assigned(S, toy_store), assigned(S1, veterinarian), adjacent(S, S1).

% Exactly two restaurants
2 { assigned(S, restaurant) : space(S) } 2.

% Each non-restaurant business appears exactly once
1 { assigned(S, optometrist) : space(S) } 1.
1 { assigned(S, pharmacy) : space(S) } 1.
1 { assigned(S, shoe_store) : space(S) } 1.
1 { assigned(S, toy_store) : space(S) } 1.
1 { assigned(S, veterinarian) : space(S) } 1.

% Two restaurants must be separated by at least two other businesses (distance >= 3)
restaurant_pos(P) :- assigned(P, restaurant).
:- restaurant_pos(P1), restaurant_pos(P2), P1 < P2, P2 - P1 < 3.

% Map the correct answer to option/1 (MANDATORY)
% Option A: The optometrist is in space 5
option(a) :- assigned(5, optometrist).

% Option B: The pharmacy is in space 1
option(b) :- assigned(1, pharmacy).

% Option C: A restaurant is in space 3
option(c) :- assigned(3, restaurant).

% Option D: The toy store is in space 6
option(d) :- assigned(6, toy_store).

% Option E: The veterinarian is in space 4
option(e) :- assigned(4, veterinarian).

#show option/1.