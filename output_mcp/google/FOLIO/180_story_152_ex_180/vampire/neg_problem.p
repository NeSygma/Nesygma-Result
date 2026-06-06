fof(susan_flies_to_lga, axiom, flies_to(susan, lga)).
fof(john_flies_from_lga, axiom, flies_from(john, lga)).
fof(departure_arrival_constraint, axiom, ! [P, A] : (flies_to(P, A) & flies_from(P, A) => $false)).
fof(distinct_people, axiom, susan != john).
fof(goal, conjecture, ~flies_from(susan, lga)).