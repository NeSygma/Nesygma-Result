% Positive file: Susan flies from LGA as conjecture
fof(distinct_constants, axiom, (susan != john & susan != lga & john != lga)).
fof(premise1, axiom, ? [F] : (flies(susan, F) & arrival(F, lga))).
fof(premise2, axiom, ? [F] : (flies(john, F) & departure(F, lga))).
fof(premise3, axiom, ! [F, A, B] : ((departure(F, A) & arrival(F, B)) => A != B)).
fof(conclusion, conjecture, ? [F] : (flies(susan, F) & departure(F, lga))).