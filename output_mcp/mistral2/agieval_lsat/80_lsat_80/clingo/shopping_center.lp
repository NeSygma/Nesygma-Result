% Base facts
space(1..7).
business(optometrist; pharmacy; restaurant1; restaurant2; shoe_store; toy_store; veterinarian).
restaurant(restaurant1; restaurant2).
pharmacy(pharmacy).
shoe_store(shoe_store).
toy_store(toy_store).
veterinarian(veterinarian).
optometrist(optometrist).

% Given: shoe store is at space 4
at(shoe_store, 4).

% End spaces
end(1). end(7).

% Next to relation
next_to(S1, S2) :- space(S1), space(S2), S2 = S1 + 1.
next_to(S1, S2) :- space(S1), space(S2), S2 = S1 - 1.

% Assign businesses to spaces (one business per space)
1 { at(B, S) : business(B) } 1 :- space(S).
1 { at(B, S) : space(S) } 1 :- business(B).

% Pharmacy at one end, restaurant at the other
:- at(pharmacy, S), not end(S).
:- at(restaurant1, S), not end(S), S != 7.
:- at(restaurant2, S), not end(S), S != 1.

% Ensure only one restaurant is at the other end
:- at(restaurant1, 1), at(restaurant2, 1).
:- at(restaurant1, 7), at(restaurant2, 7).

% Restaurants separated by at least two businesses
:- at(restaurant1, R1), at(restaurant2, R2), abs(R1 - R2) < 3.

% Pharmacy next to optometrist or veterinarian
:- at(pharmacy, P), not next_to(P, O), not next_to(P, V),
   at(optometrist, O), at(veterinarian, V).

% Toy store not next to veterinarian
:- at(toy_store, T), at(veterinarian, V), next_to(T, V).

% Derive positions for businesses
pos(B, S) :- at(B, S).

% Options to evaluate
% (A) Optometrist is next to a restaurant
optometrist_next_to_restaurant :-
    at(optometrist, O),
    (at(restaurant1, R1), next_to(O, R1) ; at(restaurant2, R2), next_to(O, R2)).

% (B) Pharmacy is next to the veterinarian
pharmacy_next_to_veterinarian :-
    at(pharmacy, P),
    at(veterinarian, V),
    next_to(P, V).

% (C) A restaurant is next to the toy store
restaurant_next_to_toy_store :-
    (at(restaurant1, R1) ; at(restaurant2, R2)),
    at(toy_store, T),
    next_to(R1, T).

% (D) Shoe store is next to the toy store
shoe_store_next_to_toy_store :-
    at(shoe_store, 4),
    at(toy_store, T),
    next_to(4, T).

% (E) Shoe store is next to the veterinarian
shoe_store_next_to_veterinarian :-
    at(shoe_store, 4),
    at(veterinarian, V),
    next_to(4, V).

% Map the correct answer to option/1
option(a) :- optometrist_next_to_restaurant.
option(b) :- pharmacy_next_to_veterinarian.
option(c) :- restaurant_next_to_toy_store.
option(d) :- shoe_store_next_to_toy_store.
option(e) :- shoe_store_next_to_veterinarian.

#show option/1.