fof(premise1, axiom, flies_to(susan, lga)).
fof(premise2, axiom, ! [P, A] : ((flies_from(P, A) & flies_to(P, A)) => ~true)).
fof(premise3, axiom, flies_from(john, lga)).
fof(conclusion_neg, conjecture, ~flies_from(susan, lga)).