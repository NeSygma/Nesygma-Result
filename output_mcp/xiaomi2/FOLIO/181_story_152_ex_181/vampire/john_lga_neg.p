fof(premise_1, axiom, flies_to(susan, lga)).
fof(premise_2, axiom, ! [P, A] : (flies_from(P, A) => ~flies_to(P, A))).
fof(premise_3, axiom, flies_from(john, lga)).
fof(goal, conjecture, ~flies_to(john, lga)).