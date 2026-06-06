% Spaces and businesses
space(1..7).

business(optometrist; pharmacy; restaurant1; restaurant2; shoe_store; toy_store; veterinarian).

% Helper to identify restaurants
restaurant(B) :- B = restaurant1.
restaurant(B) :- B = restaurant2.

% Assignment: each space has exactly one business, each business is in exactly one space
1 { assignment(S, B) : business(B) } 1 :- space(S).
1 { assignment(S, B) : space(S) } 1 :- business(B).

% Exactly two restaurants
2 { assignment(S, B) : space(S), restaurant(B) } 2.

% Pharmacy must be at one end (space 1 or 7)
pharmacy_at_end :- assignment(1, pharmacy).
pharmacy_at_end :- assignment(7, pharmacy).
:- not pharmacy_at_end.

% The other end must have a restaurant
other_end_has_restaurant :- assignment(1, B), restaurant(B).
other_end_has_restaurant :- assignment(7, B), restaurant(B).
:- not other_end_has_restaurant.

% Two restaurants must be separated by at least two other businesses
% Let S1 and S2 be the positions of the two restaurants, with S1 < S2
% Then S2 - S1 >= 3 (separated by at least two businesses)
restaurant_pos(S) :- assignment(S, B), restaurant(B).
:- restaurant_pos(S1), restaurant_pos(S2), S1 < S2, S2 - S1 < 3.

% Pharmacy must be next to either optometrist or veterinarian
:- assignment(1, pharmacy), not assignment(2, optometrist), not assignment(2, veterinarian).
:- assignment(7, pharmacy), not assignment(6, optometrist), not assignment(6, veterinarian).

% Adjacency helper
adjacent(S1, S2) :- S2 = S1 + 1, space(S1), space(S2).
adjacent(S1, S2) :- S2 = S1 - 1, space(S1), space(S2).

% Toy store cannot be next to veterinarian
:- assignment(S, toy_store), adjacent(S, S1), assignment(S1, veterinarian).

% Veterinarian is in space 5
:- not assignment(5, veterinarian).

% Define the conditions for each option
optometrist_in_space_2 :- assignment(2, optometrist).
pharmacy_in_space_7 :- assignment(7, pharmacy).
restaurant_in_space_4 :- assignment(4, B), restaurant(B).
shoe_store_in_space_6 :- assignment(6, shoe_store).
toy_store_in_space_3 :- assignment(3, toy_store).

% Map the correct answer to option/1
option(a) :- optometrist_in_space_2.
option(b) :- pharmacy_in_space_7.
option(c) :- restaurant_in_space_4.
option(d) :- shoe_store_in_space_6.
option(e) :- toy_store_in_space_3.

#show option/1.