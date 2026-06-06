fof(susan_flies_to_lga, axiom, flies_to(susan, lga)).
fof(departure_arrival_not_same, axiom, ! [P, A] : (flies_from(P, A) => ~flies_to(P, A))).
fof(john_flies_from_lga, axiom, flies_from(john, lga)).
fof(conclusion, conjecture, flies_to(john, lga)).