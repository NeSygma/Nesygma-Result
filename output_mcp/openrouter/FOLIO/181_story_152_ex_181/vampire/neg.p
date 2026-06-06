% Negative test
fof(p1, axiom, flies_to(susan, lga)).
fof(p2, axiom, flies_from(john, lga)).
fof(p3, axiom, ! [P,A,B] : ((flies_from(P,A) & flies_to(P,B)) => A != B)).
fof(distinct, axiom, (susan != john & susan != lga & john != lga)).
fof(goal, conjecture, ~flies_to(john, lga)).