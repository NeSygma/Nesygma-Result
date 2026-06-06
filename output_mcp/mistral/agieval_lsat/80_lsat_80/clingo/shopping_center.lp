% Spaces
space(1..7).

% Businesses
business(optometrist; pharmacy; shoe_store; toy_store; veterinarian).

% Restaurants (two instances, but not distinguished)
restaurant(restaurant).

% Each space has exactly one business
1 { location(B, S) : business(B) } 1 :- space(S).

% Each business is in exactly one space
1 { location(B, S) : space(S) } 1 :- business(B).
1 { location(restaurant, S) : space(S) } 2.

% End spaces
end_space(1).
end_space(7).

% Pharmacy at one end
:- location(pharmacy, S), not end_space(S).

% One restaurant at the other end
:- location(pharmacy, 1), not 1 { location(restaurant, 7) } 1.
:- location(pharmacy, 7), not 1 { location(restaurant, 1) } 1.

% Two restaurants must be separated by at least two other businesses
% This means |S1 - S2| >= 3
:- 2 { location(restaurant, S) : space(S) },
   location(restaurant, S1), location(restaurant, S2),
   S1 != S2, abs(S1 - S2) < 3.

% Define adjacency
adjacent(S, S+1) :- space(S), space(S+1).
adjacent(S+1, S) :- space(S), space(S+1).

% Pharmacy must be next to either optometrist or veterinarian
:- location(pharmacy, S), end_space(S),
   not 1 { location(optometrist, S1) : adjacent(S, S1) } 1,
   not 1 { location(veterinarian, S1) : adjacent(S, S1) } 1.

% Toy store cannot be next to veterinarian
:- location(toy_store, S1), location(veterinarian, S2), adjacent(S1, S2).

% Shoe store is in space 4
:- not location(shoe_store, 4).

% Helper to check if optometrist is next to a restaurant
optometrist_next_to_restaurant :- location(optometrist, S), location(restaurant, S1), adjacent(S, S1).

% Helper to check if pharmacy is next to veterinarian
pharmacy_next_to_veterinarian :- location(pharmacy, S), location(veterinarian, S1), adjacent(S, S1).

% Helper to check if a restaurant is next to the toy store
restaurant_next_to_toy_store :- location(restaurant, S), location(toy_store, S1), adjacent(S, S1).

% Helper to check if shoe store is next to toy store
shoe_store_next_to_toy_store :- location(shoe_store, 4), location(toy_store, 3).
shoe_store_next_to_toy_store :- location(shoe_store, 4), location(toy_store, 5).

% Helper to check if shoe store is next to veterinarian
shoe_store_next_to_veterinarian :- location(shoe_store, 4), location(veterinarian, 3).
shoe_store_next_to_veterinarian :- location(shoe_store, 4), location(veterinarian, 5).

% Map the correct answer to option/1
% Based on analysis, option B must be true in all valid configurations
option(a) :- optometrist_next_to_restaurant.
option(b) :- pharmacy_next_to_veterinarian.
option(c) :- restaurant_next_to_toy_store.
option(d) :- shoe_store_next_to_toy_store.
option(e) :- shoe_store_next_to_veterinarian.

% Ensure at least one option is true
solution_exists :- option(_).

#show option/1.
#show solution_exists.