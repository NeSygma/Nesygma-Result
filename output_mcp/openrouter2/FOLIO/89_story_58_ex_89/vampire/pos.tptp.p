fof(p1, axiom, ! [B] : (book(B) => contains_knowledge(B))).
fof(p2, axiom, ! [P,B] : (reads(P,B) => gains_knowledge(P))).
fof(p3, axiom, ! [P] : (gains_knowledge(P) => smarter(P))).
fof(p4, axiom, reads(harry, walden)).
fof(p5, axiom, book(walden)).
fof(distinct, axiom, harry != walden).
fof(goal, conjecture, smarter(harry)).