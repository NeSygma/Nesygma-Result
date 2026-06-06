% Spaces
space(1..7).

% Business types
business(optometrist; pharmacy; restaurant; shoe_store; toy_store; veterinarian).

% Each space has exactly one business
1 { assigned(S, B) : business(B) } 1 :- space(S).

% Exactly two restaurants
:- not #count{ S : assigned(S, restaurant) } = 2.

% Pharmacy at one end, one restaurant at the other end
:- assigned(1, pharmacy), not assigned(7, restaurant).
:- assigned(7, pharmacy), not assigned(1, restaurant).
:- not assigned(1, pharmacy), not assigned(7, pharmacy).
:- not assigned(1, restaurant), not assigned(7, restaurant).

% Pharmacy next to optometrist or veterinarian
:- assigned(1, pharmacy), not assigned(2, optometrist), not assigned(2, veterinarian).
:- assigned(7, pharmacy), not assigned(6, optometrist), not assigned(6, veterinarian).

% Toy store not next to veterinarian
:- assigned(S, toy_store), assigned(S1, veterinarian), (S = S1 + 1 ; S = S1 - 1), space(S1).

% Original constraint: restaurants separated by at least two businesses
restaurant_at(S) :- assigned(S, restaurant).
separation_ok :- restaurant_at(S1), restaurant_at(S2), S1 < S2, S2 - S1 >= 3.
:- not separation_ok.

% ==================================================
% Helper predicate for distance between two spaces
% ==================================================
distance(S1, S2, D) :- S1 < S2, D = S2 - S1, space(S1), space(S2).
distance(S1, S2, D) :- S1 > S2, D = S1 - S2, space(S1), space(S2).

% ==================================================
% Evaluate each substitution option
% ==================================================

% Option A: A restaurant must be in either space 3, space 4, or space 5.
% This would replace the restaurant separation constraint
option(a) :- 
    restaurant_at(3).
option(a) :- 
    restaurant_at(4).
option(a) :- 
    restaurant_at(5).

% Ensure Option A is only chosen if it satisfies the original problem
% (i.e., it must also satisfy the other constraints)
:- option(a), not (restaurant_at(3) ; restaurant_at(4) ; restaurant_at(5)).

% Option B: A restaurant must be next to either the optometrist or the veterinarian.
% This would replace the restaurant separation constraint
option(b) :- 
    restaurant_at(S),
    (assigned(S-1, optometrist) ; assigned(S-1, veterinarian) ;
     assigned(S+1, optometrist) ; assigned(S+1, veterinarian)),
    space(S-1).
option(b) :- 
    restaurant_at(S),
    (assigned(S-1, optometrist) ; assigned(S-1, veterinarian) ;
     assigned(S+1, optometrist) ; assigned(S+1, veterinarian)),
    space(S+1).

% Ensure Option B is only chosen if it satisfies the original problem
:- option(b), not (restaurant_at(S), 
                  (assigned(S-1, optometrist) ; assigned(S-1, veterinarian) ;
                   assigned(S+1, optometrist) ; assigned(S+1, veterinarian)),
                  (space(S-1) ; space(S+1))).

% Option C: Either the toy store or the veterinarian must be somewhere between the two restaurants.
% This would replace the restaurant separation constraint
option(c) :- 
    restaurant_at(S1), restaurant_at(S2), S1 < S2,
    #count{ S : S1 < S, S < S2, assigned(S, toy_store) } >= 1.
option(c) :- 
    restaurant_at(S1), restaurant_at(S2), S1 < S2,
    #count{ S : S1 < S, S < S2, assigned(S, veterinarian) } >= 1.

% Ensure Option C is only chosen if it satisfies the original problem
:- option(c), not (restaurant_at(S1), restaurant_at(S2), S1 < S2,
                   (#count{ S : S1 < S, S < S2, assigned(S, toy_store) } >= 1 ;
                    #count{ S : S1 < S, S < S2, assigned(S, veterinarian) } >= 1)).

% Option D: No more than two businesses can separate the pharmacy and the restaurant nearest it.
% This would replace the restaurant separation constraint
pharmacy_at(S) :- assigned(S, pharmacy).
nearest_restaurant_distance(D) :- 
    pharmacy_at(P), 
    D = #min{ D1 : restaurant_at(R), distance(P, R, D1) }.
option(d) :- nearest_restaurant_distance(D), D = 1.
option(d) :- nearest_restaurant_distance(D), D = 2.
option(d) :- nearest_restaurant_distance(D), D = 3.

% Ensure Option D is only chosen if it satisfies the original problem
:- option(d), nearest_restaurant_distance(D), D > 3.

% Option E: The optometrist cannot be next to the shoe store.
% This would replace the restaurant separation constraint
:- assigned(S, optometrist), assigned(S1, shoe_store), (S = S1 + 1 ; S = S1 - 1), space(S1).
option(e) :- not (assigned(S, optometrist), assigned(S1, shoe_store), (S = S1 + 1 ; S = S1 - 1), space(S1)).

% ==================================================
% Ensure only one option is correct
% ==================================================
:- option(A), option(B), A != B.
:- option(A), option(C), A != C.
:- option(A), option(D), A != D.
:- option(A), option(E), A != E.
:- option(B), option(C), B != C.
:- option(B), option(D), B != D.
:- option(B), option(E), B != E.
:- option(C), option(D), C != D.
:- option(C), option(E), C != E.
:- option(D), option(E), D != E.

% Show the answer
#show option/1.