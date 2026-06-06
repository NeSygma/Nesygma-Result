% Positive version: original claim as conjecture
fof(susan_to_lga, axiom, flies_to(susan, lga)).
fof(no_same_airport, axiom, ! [P, A] : (~(flies_from(P, A) & flies_to(P, A)))).
fof(john_from_lga, axiom, flies_from(john, lga)).
fof(goal, conjecture, flies_from(susan, lga)).