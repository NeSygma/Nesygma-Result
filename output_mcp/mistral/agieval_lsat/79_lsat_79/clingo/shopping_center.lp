% Define the spaces and businesses
space(1..7).
business(optometrist; pharmacy; restaurant; shoe_store; toy_store; veterinarian).

% Two restaurants (restaurant1 and restaurant2)
2 { assigned(restaurant, S) : space(S) } 2 :- business(restaurant).

% Each space has exactly one business
1 { assigned(B, S) : business(B) } 1 :- space(S).

% Each business is assigned to exactly one space
1 { assigned(B, S) : space(S) } 1 :- business(B), B != restaurant.

% Pharmacy must be at one end (1 or 7)
:- assigned(pharmacy, S), S != 1, S != 7.

% One restaurant must be at the other end
:- assigned(restaurant, S), S != 1, S != 7, not assigned(pharmacy, 1), not assigned(pharmacy, 7).

% Ensure pharmacy and one restaurant are at the ends
:- assigned(pharmacy, 1), not assigned(restaurant, 7).
:- assigned(pharmacy, 7), not assigned(restaurant, 1).
:- assigned(restaurant, 1), not assigned(pharmacy, 7).
:- assigned(restaurant, 7), not assigned(pharmacy, 1).

% Two restaurants must be separated by at least two businesses
restaurant_pos(S) :- assigned(restaurant, S).
:- restaurant_pos(S1), restaurant_pos(S2), S1 < S2, S2 - S1 - 1 < 2.

% Helper: adjacent spaces
adjacent(S1, S2) :- space(S1), space(S2), S1 = S2 + 1.
adjacent(S1, S2) :- space(S1), space(S2), S1 = S2 - 1.

% Pharmacy must be next to optometrist or veterinarian
:- assigned(pharmacy, S), not adjacent(S, S1), assigned(optometrist, S1), not assigned(veterinarian, S1).
:- assigned(pharmacy, S), not adjacent(S, S1), assigned(veterinarian, S1), not assigned(optometrist, S1).

% Toy store cannot be next to veterinarian
:- assigned(toy_store, S), adjacent(S, S1), assigned(veterinarian, S1).
:- assigned(veterinarian, S), adjacent(S, S1), assigned(toy_store, S1).

% Condition for the question: optometrist is next to shoe store
opt_shoe_adjacent :-
    assigned(optometrist, S), assigned(shoe_store, S1), adjacent(S, S1).

% Identify the pair of optometrist and shoe store
pair(S, S1) :- assigned(optometrist, S), assigned(shoe_store, S1), adjacent(S, S1).

% Identify the spaces immediately to the left and right of the pair
left_space(S_left) :-
    pair(S, S1), S_left = S - 1, space(S_left).
right_space(S_right) :-
    pair(S, S1), S_right = S1 + 1, space(S_right).

% Identify the businesses in those spaces
left_business(B) :- left_space(S_left), assigned(B, S_left).
right_business(B) :- right_space(S_right), assigned(B, S_right).

% Map to answer choices
% (A) the pharmacy and a restaurant
option(a) :- left_business(pharmacy), right_business(restaurant).
option(a) :- left_business(restaurant), right_business(pharmacy).

% (B) the pharmacy and the toy store
option(b) :- left_business(pharmacy), right_business(toy_store).
option(b) :- left_business(toy_store), right_business(pharmacy).

% (C) the two restaurants
option(c) :- left_business(restaurant), right_business(restaurant).

% (D) a restaurant and the toy store
option(d) :- left_business(restaurant), right_business(toy_store).
option(d) :- left_business(toy_store), right_business(restaurant).

% (E) a restaurant and the veterinarian
option(e) :- left_business(restaurant), right_business(veterinarian).
option(e) :- left_business(veterinarian), right_business(restaurant).

#show option/1.