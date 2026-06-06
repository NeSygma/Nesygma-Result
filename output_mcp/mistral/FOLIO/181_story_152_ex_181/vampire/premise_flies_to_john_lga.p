fof(susan_flies_to_lga, axiom, flies_to(susan, lga)).
fof(constraint, axiom, ! [P, A] : (flies_from(P, A) => ~flies_to(P, A))).
fof(john_flies_from_lga, axiom, flies_from(john, lga)).
fof(distinct_people, axiom, susan != john).
fof(conclusion, conjecture, flies_to(john, lga)).