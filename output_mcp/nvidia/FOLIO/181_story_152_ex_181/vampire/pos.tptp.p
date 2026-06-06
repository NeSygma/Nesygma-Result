fof(axiom_1, axiom, arrive(susan, lga)).
fof(axiom_2, axiom, depart(john, lga)).
fof(axiom_3, axiom, ! [P,A,B] : ((depart(P,A) & arrive(P,B)) => A != B)).
fof(axiom_4, axiom, susan != john).
fof(axiom_5, axiom, susan != lga).
fof(axiom_6, axiom, john != lga).
fof(conjecture, conjecture, arrive(john, lga)).