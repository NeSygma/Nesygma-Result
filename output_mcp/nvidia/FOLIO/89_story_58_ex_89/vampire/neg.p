fof(neg, axiom, ! [X] : (book(X) => knowledge(X))).
fof(neg, axiom, ! [P,B] : ((person(P) & book(B) & reads(P,B)) => gains_knowledge(P))).
fof(neg, axiom, ! [P] : (gains_knowledge(P) => smarter(P))).
fof(neg, axiom, person(harry)).
fof(neg, axiom, book(walden)).
fof(neg, axiom, reads(harry, walden)).
fof(neg, conjecture, ~smarter(harry)).