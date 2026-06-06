% Define spaces and businesses
space(1..7).
business(optometrist; pharmacy; restaurant; shoe_store; toy_store; veterinarian).

% Each space has exactly one business
1 { assigned(S, B) : business(B) } 1 :- space(S).

% Each business is assigned to exactly one space, except restaurant which is assigned to two spaces
1 { assigned(S, restaurant) : space(S) } 2.
1 { assigned(S, B) : space(S) } 1 :- business(B), B != restaurant.

% Constraint 1: Pharmacy must be at one end, and one restaurant at the other
:- not ((assigned(1, pharmacy), assigned(7, restaurant)) ;
         (assigned(1, restaurant), assigned(7, pharmacy))).

% Constraint 2: The two restaurants must be separated by at least two other businesses
:- assigned(R1, restaurant), assigned(R2, restaurant), R1 < R2, R2 - R1 < 3.

% Constraint 3: Pharmacy must be next to either optometrist or veterinarian
:- assigned(P, pharmacy), not (
    (P = 1, (assigned(2, optometrist) ; assigned(2, veterinarian))) ;
    (P = 2, ((assigned(1, optometrist) ; assigned(1, veterinarian)) ; (assigned(3, optometrist) ; assigned(3, veterinarian)))) ;
    (P = 3, ((assigned(2, optometrist) ; assigned(2, veterinarian)) ; (assigned(4, optometrist) ; assigned(4, veterinarian)))) ;
    (P = 4, ((assigned(3, optometrist) ; assigned(3, veterinarian)) ; (assigned(5, optometrist) ; assigned(5, veterinarian)))) ;
    (P = 5, ((assigned(4, optometrist) ; assigned(4, veterinarian)) ; (assigned(6, optometrist) ; assigned(6, veterinarian)))) ;
    (P = 6, ((assigned(5, optometrist) ; assigned(5, veterinarian)) ; (assigned(7, optometrist) ; assigned(7, veterinarian)))) ;
    (P = 7, (assigned(6, optometrist) ; assigned(6, veterinarian)))
).

% Constraint 4: Toy store cannot be next to veterinarian
:- assigned(T, toy_store), assigned(V, veterinarian), (T = V + 1 ; V = T + 1).

% Option A: pharmacy, optometrist, shoe store, restaurant, veterinarian, toy store, restaurant
option_a :- assigned(1, pharmacy), assigned(2, optometrist), assigned(3, shoe_store),
            assigned(4, restaurant), assigned(5, veterinarian), assigned(6, toy_store), assigned(7, restaurant).

% Option B: pharmacy, veterinarian, optometrist, shoe store, restaurant, toy store, restaurant
option_b :- assigned(1, pharmacy), assigned(2, veterinarian), assigned(3, optometrist),
            assigned(4, shoe_store), assigned(5, restaurant), assigned(6, toy_store), assigned(7, restaurant).

% Option C: restaurant, shoe store, veterinarian, pharmacy, optometrist, toy store, restaurant
option_c :- assigned(1, restaurant), assigned(2, shoe_store), assigned(3, veterinarian),
            assigned(4, pharmacy), assigned(5, optometrist), assigned(6, toy_store), assigned(7, restaurant).

% Option D: restaurant, toy store, optometrist, restaurant, veterinarian, shoe store, pharmacy
option_d :- assigned(1, restaurant), assigned(2, toy_store), assigned(3, optometrist),
            assigned(4, restaurant), assigned(5, veterinarian), assigned(6, shoe_store), assigned(7, pharmacy).

% Option E: restaurant, optometrist, toy store, restaurant, shoe store, veterinarian, pharmacy
option_e :- assigned(1, restaurant), assigned(2, optometrist), assigned(3, toy_store),
            assigned(4, restaurant), assigned(5, shoe_store), assigned(6, veterinarian), assigned(7, pharmacy).

% Only one option can be true
:- option_a, option_b.
:- option_a, option_c.
:- option_a, option_d.
:- option_a, option_e.
:- option_b, option_c.
:- option_b, option_d.
:- option_b, option_e.
:- option_c, option_d.
:- option_c, option_e.
:- option_d, option_e.

% Map to answer choices
option(a) :- option_a.
option(b) :- option_b.
option(c) :- option_c.
option(d) :- option_d.
option(e) :- option_e.

#show option/1.