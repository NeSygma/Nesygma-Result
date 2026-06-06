% Base facts: spaces and businesses
space(1..7).
business(optometrist; pharmacy; restaurant1; restaurant2; shoe_store; toy_store; veterinarian).

% Assign exactly one business to each space
1 { assignment(S, B) : business(B) } 1 :- space(S).
:- assignment(S1, B), assignment(S2, B), S1 != S2.

% The pharmacy must be at one end of the row and one of the restaurants at the other.
:- not assignment(1, pharmacy), not assignment(7, pharmacy).
:- not assignment(1, restaurant1), not assignment(1, restaurant2), not assignment(7, restaurant1), not assignment(7, restaurant2).

% The two restaurants must be separated by at least two other businesses.
:- assignment(S1, restaurant1), assignment(S2, restaurant2), |S1 - S2| < 3.
:- assignment(S1, restaurant1), assignment(S2, restaurant2), S1 = S2.

% The pharmacy must be next to either the optometrist or the veterinarian.
:- assignment(S, pharmacy), not adjacent(S, optometrist), not adjacent(S, veterinarian).

% The toy store cannot be next to the veterinarian.
:- assignment(S1, toy_store), assignment(S2, veterinarian), adjacent(S1, S2).

% Helper predicate: adjacent spaces
adjacent(S1, S2) :- space(S1), space(S2), |S1 - S2| = 1.

% Additional constraint: optometrist is next to the shoe store
:- not adjacent_optometrist_shoe_store.

% Define adjacent_optometrist_shoe_store
adjacent_optometrist_shoe_store :-
    assignment(S, optometrist),
    assignment(S1, shoe_store),
    adjacent(S, S1).

% Define the businesses immediately on either side of the optometrist-shoe store pair
left_business(S, B) :-
    assignment(S, B),
    assignment(S1, optometrist),
    assignment(S2, shoe_store),
    adjacent(S1, S2),
    S = S1 - 1.

right_business(S, B) :-
    assignment(S, B),
    assignment(S1, optometrist),
    assignment(S2, shoe_store),
    adjacent(S1, S2),
    S = S2 + 1.

% Check the options
% (A) the pharmacy and a restaurant
option(a) :-
    left_business(S1, pharmacy),
    right_business(S2, B),
    business(B),
    B = restaurant1.
option(a) :-
    left_business(S1, pharmacy),
    right_business(S2, B),
    business(B),
    B = restaurant2.

option(a) :-
    left_business(S1, B1),
    B1 = pharmacy,
    right_business(S2, pharmacy),
    pharmacy = restaurant1.
option(a) :-
    left_business(S1, B1),
    B1 = pharmacy,
    right_business(S2, pharmacy),
    pharmacy = restaurant2.

% (B) the pharmacy and the toy store
option(b) :-
    left_business(S1, pharmacy),
    right_business(S2, toy_store).

option(b) :-
    left_business(S1, toy_store),
    right_business(S2, pharmacy).

% (C) the two restaurants
option(c) :-
    left_business(S1, restaurant1),
    right_business(S2, restaurant2).

option(c) :-
    left_business(S1, restaurant2),
    right_business(S2, restaurant1).

% (D) a restaurant and the toy store
option(d) :-
    left_business(S1, B1),
    business(B1),
    B1 = restaurant1,
    right_business(S2, toy_store).

option(d) :-
    left_business(S1, B1),
    business(B1),
    B1 = restaurant2,
    right_business(S2, toy_store).

option(d) :-
    left_business(S1, toy_store),
    right_business(S2, B2),
    business(B2),
    B2 = restaurant1.

option(d) :-
    left_business(S1, toy_store),
    right_business(S2, B2),
    business(B2),
    B2 = restaurant2.

% (E) a restaurant and the veterinarian
option(e) :-
    left_business(S1, B1),
    business(B1),
    B1 = restaurant1,
    right_business(S2, veterinarian).

option(e) :-
    left_business(S1, B1),
    business(B1),
    B1 = restaurant2,
    right_business(S2, veterinarian).

option(e) :-
    left_business(S1, veterinarian),
    right_business(S2, B2),
    business(B2),
    B2 = restaurant1.

option(e) :-
    left_business(S1, veterinarian),
    right_business(S2, B2),
    business(B2),
    B2 = restaurant2.

#show option/1.