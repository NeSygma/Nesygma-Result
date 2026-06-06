fof(distinct_constants, axiom, (susan != john & susan != lga & john != lga)).
fof(premise1, axiom, flies_to(susan, lga)).
fof(premise2, axiom, ! [P, A, B] : ((flies_from(P, A) & flies_to(P, B)) => A != B)).
fof(premise3, axiom, flies_from(john, lga)).
fof(goal, conjecture, flies_to(john, lga)).