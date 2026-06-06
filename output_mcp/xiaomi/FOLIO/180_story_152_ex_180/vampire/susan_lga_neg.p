fof(premise_1, axiom, flies_to(susan, lga)).
fof(premise_2, axiom, ! [P, A1, A2] : ((flies_from(P, A1) & flies_to(P, A2)) => A1 != A2)).
fof(premise_3, axiom, flies_from(john, lga)).
fof(goal, conjecture, ~flies_from(susan, lga)).