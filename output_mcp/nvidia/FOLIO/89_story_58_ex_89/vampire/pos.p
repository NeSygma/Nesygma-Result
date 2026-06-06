fof(pos, axiom, ! [X] : (book(X) => knowledge(X))).
fof(pos, axiom, ! [P,B] : ((person(P) & book(B) & reads(P,B)) => gains_knowledge(P))).
fof(pos, axiom, ! [P] : (gains_knowledge(P) => smarter(P))).
fof(pos, axiom, person(harry)).
fof(pos, axiom, book(walden)).
fof(pos, axiom, reads(harry, walden)).
fof(pos, conjecture, smarter(harry)).