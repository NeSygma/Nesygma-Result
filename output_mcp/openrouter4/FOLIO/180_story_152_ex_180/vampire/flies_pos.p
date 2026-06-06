fof(premise_1, axiom, flies_to(susan, lga)).
fof(premise_2, axiom, ! [X, A] : (flies_from(X, A) => ~flies_to(X, A))).
fof(premise_3, axiom, flies_from(john, lga)).
fof(conjecture, conjecture, flies_from(susan, lga)).