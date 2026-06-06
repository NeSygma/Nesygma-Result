fof(distinct, axiom, (susan != john & susan != lga & john != lga)).
fof(fact1, axiom, flies_to(susan, lga)).
fof(fact2, axiom, flies_from(john, lga)).
fof(rule1, axiom, ! [P, A, B] : ((flies_from(P, A) & flies_to(P, B)) => A != B)).
fof(goal, conjecture, ~flies_from(susan, lga)).