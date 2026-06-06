% Negative version: negated claim as conjecture
% Premises:
% Susan flies to LGA airport.
% The departure and arrival can not be at the same airport.
% John flies from LGA airport.
% Negated conclusion: John does NOT fly to LGA airport.

fof(distinct_people, axiom, susan != john).

fof(susan_to_lga, axiom, flies_to(susan, lga)).
fof(no_same_airport, axiom, ! [X, A] : ~(flies_from(X, A) & flies_to(X, A))).
fof(john_from_lga, axiom, flies_from(john, lga)).

fof(goal, conjecture, ~flies_to(john, lga)).