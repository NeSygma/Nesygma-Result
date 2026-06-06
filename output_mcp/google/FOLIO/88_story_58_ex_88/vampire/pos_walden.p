fof(premise_1, axiom, ! [X] : (book(X) => contains_knowledge(X))).
fof(premise_2, axiom, ! [P, B] : ((person(P) & book(B) & reads(P, B)) => gains_knowledge(P))).
fof(premise_3, axiom, ! [P] : (gains_knowledge(P) => becomes_smarter(P))).
fof(premise_4, axiom, person(harry)).
fof(premise_5, axiom, book(walden)).
fof(premise_6, axiom, reads(harry, walden)).
fof(goal, conjecture, contains_knowledge(walden)).