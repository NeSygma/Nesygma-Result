fof(premise_2, axiom, ! [X, Y] : ((person(X) & book(Y) & reads(X, Y)) => gains_knowledge(X))).
fof(premise_3, axiom, ! [X] : ((person(X) & gains_knowledge(X)) => smarter(X))).
fof(premise_4, axiom, person(harry)).
fof(premise_5, axiom, book(walden)).
fof(premise_6, axiom, reads(harry, walden)).
fof(conjecture, conjecture, ~! [X] : (smarter(X) => gains_knowledge(X))).