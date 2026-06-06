% Base facts: spaces and businesses
space(1..7).

% Businesses: optometrist, pharmacy, two restaurants, shoe store, toy store, veterinarian
business(optometrist; pharmacy; restaurant; restaurant; shoe_store; toy_store; veterinarian).

% Ensure unique businesses in each space
1 { assignment(S, B) : business(B) } 1 :- space(S).

% Each business is assigned to exactly one space
1 { assignment(S, B) : space(S) } 1 :- business(B).

% The pharmacy must be at one end of the row
:- assignment(S, pharmacy), S != 1, S != 7.

% One restaurant must be at one end, and the other restaurant at the other end
:- { assignment(1, restaurant) } != 1.
:- { assignment(7, restaurant) } != 1.

% The two restaurants must be separated by at least two other businesses
restaurant_pos(S) :- assignment(S, restaurant).
:- restaurant_pos(S1), restaurant_pos(S2), S1 < S2, S2 - S1 < 3.

% The pharmacy must be next to either the optometrist or the veterinarian
:- assignment(S, pharmacy), not adjacent_to_pharmacy(S).

% Helper: Define adjacency
adjacent(S1, S2) :- space(S1), space(S2), S2 = S1 + 1.
adjacent(S1, S2) :- space(S1), space(S2), S2 = S1 - 1.

% Helper: Check if pharmacy is adjacent to optometrist or veterinarian
adjacent_to_pharmacy(S) :- assignment(S, pharmacy), assignment(S1, optometrist), adjacent(S, S1).
adjacent_to_pharmacy(S) :- assignment(S, pharmacy), assignment(S1, veterinarian), adjacent(S, S1).

% The toy store cannot be next to the veterinarian
:- assignment(S1, toy_store), assignment(S2, veterinarian), adjacent(S1, S2).

% Additional constraint: The shoe store is in space 2 (given condition)
:- not assignment(2, shoe_store).

% Map the correct answer to option/1 (MANDATORY)
% (A) The optometrist is in space 5
option(a) :- assignment(5, optometrist).

% (B) The pharmacy is in space 1
option(b) :- assignment(1, pharmacy).

% (C) A restaurant is in space 3
option(c) :- assignment(3, restaurant).

% (D) The toy store is in space 6
option(d) :- assignment(6, toy_store).

% (E) The veterinarian is in space 4
option(e) :- assignment(4, veterinarian).

#show option/1.