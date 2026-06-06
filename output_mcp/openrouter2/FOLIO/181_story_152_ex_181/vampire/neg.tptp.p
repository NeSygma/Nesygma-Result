fof(distinct_people, axiom, john != susan).
fof(rule_departure_arrival, axiom, ! [X, From, To] : ((flies_from(X, From) & flies_to(X, To)) => From != To)).
fof(fact_susan_fly_to, axiom, flies_to(susan, lga)).
fof(fact_john_fly_from, axiom, flies_from(john, lga)).
fof(conjecture, conjecture, ~flies_to(john, lga)).