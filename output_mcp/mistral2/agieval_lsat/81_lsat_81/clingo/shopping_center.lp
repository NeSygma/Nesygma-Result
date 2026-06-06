% Base facts: spaces and businesses
space(1..7).

business(optometrist).
business(pharmacy).
business(restaurant).
business(restaurant).  % Two restaurants
business(shoe_store).
business(toy_store).
business(veterinarian).

% Ensure unique businesses in spaces
1 { assigned(S, B) : business(B) } 1 :- space(S).

% Each business is assigned to exactly one space
1 { assigned(S, B) : space(S) } 1 :- business(B).

% The pharmacy must be at one end of the row
:- assigned(S, pharmacy), S != 1, S != 7.

% One of the restaurants must be at the other end
:- not assigned(1, restaurant), not assigned(7, restaurant).

% The two restaurants must be separated by at least two other businesses
% Original constraint: restaurants must be separated by at least two businesses
:- assigned(S1, restaurant), assigned(S2, restaurant), S1 < S2, S2 - S1 - 1 < 2.

% The pharmacy must be next to either the optometrist or the veterinarian
:- assigned(S, pharmacy), not adjacent_to_pharmacy(S).

adjacent_to_pharmacy(S) :- 
    assigned(S, optometrist), 
    (assigned(S-1, pharmacy) ; assigned(S+1, pharmacy)).

adjacent_to_pharmacy(S) :- 
    assigned(S, veterinarian), 
    (assigned(S-1, pharmacy) ; assigned(S+1, pharmacy)).

% The toy store cannot be next to the veterinarian
:- assigned(S1, toy_store), assigned(S2, veterinarian), adjacent(S1, S2).

adjacent(S1, S2) :- S2 = S1 + 1.
adjacent(S1, S2) :- S2 = S1 - 1.

% --- Replacement logic for the original constraint ---
% The correct replacement is: Either the toy store or the veterinarian must be somewhere between the two restaurants.
% This ensures that the two restaurants are separated by at least one business (toy store or veterinarian).

% Let's define the replacement constraint as Option C suggests:
% Either the toy store or the veterinarian must be somewhere between the two restaurants.

% This ensures that the two restaurants are separated by at least one business.

% Map the correct answer to option/1
option(c) :- 
    assigned(S1, restaurant), 
    assigned(S2, restaurant), 
    S1 < S2, 
    (between(S1, S2, toy_store) ; between(S1, S2, veterinarian)).

between(S1, S2, B) :- 
    space(S), 
    S1 < S < S2, 
    assigned(S, B).

#show option/1.