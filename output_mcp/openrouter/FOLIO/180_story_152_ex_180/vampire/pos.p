% Positive test: conjecture that Susan flies from LGA
fof(distinct_entities, axiom, (susan != john & susan != lga & john != lga)).
fof(premise1, axiom, flies_to(susan, lga)).
fof(premise2, axiom, ! [X, A, B] : ((flies_from(X, A) & flies_to(X, B)) => A != B)).
fof(premise3, axiom, flies_from(john, lga)).
fof(goal, conjecture, flies_from(susan, lga)).