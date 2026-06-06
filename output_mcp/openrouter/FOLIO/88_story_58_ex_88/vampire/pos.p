% Positive version
fof(rule1, axiom, ! [X] : (book(X) => contains_knowledge(X))).
fof(rule2, axiom, ! [P,B] : (reads(P,B) => gains_knowledge(P))).
fof(rule3, axiom, ! [P] : (gains_knowledge(P) => smarter(P))).
fof(fact_book, axiom, book(walden)).
fof(fact_read, axiom, reads(harry, walden)).
fof(distinct, axiom, (harry != walden & harry != thoreau & walden != thoreau)).
fof(goal, conjecture, contains_knowledge(walden)).