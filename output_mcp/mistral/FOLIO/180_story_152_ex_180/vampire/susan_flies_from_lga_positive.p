tff(person_type, type, person: $tType).
tff(airport_type, type, airport: $tType).
tff(susan_decl, type, susan: person).
tff(john_decl, type, john: person).
tff(lga_decl, type, lga: airport).
tff(flies_to_type, type, flies_to: (person * airport) > $o).
tff(flies_from_type, type, flies_from: (person * airport) > $o).

fof(susan_flies_to_lga, axiom, flies_to(susan, lga)).
fof(departure_not_arrival, axiom, ! [P: person, A: airport] : (flies_from(P, A) => ~flies_to(P, A))).
fof(john_flies_from_lga, axiom, flies_from(john, lga)).
fof(conclusion, conjecture, flies_from(susan, lga)).