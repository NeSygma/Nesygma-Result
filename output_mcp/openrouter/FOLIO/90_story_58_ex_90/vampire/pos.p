% Positive test
fof(distinct_consts, axiom, (harry != walden)).
fof(book_walden, axiom, book(walden)).
fof(reads_rule, axiom, ! [P,B] : (reads(P,B) => gains_knowledge(P))).
fof(gains_rule, axiom, ! [P] : (gains_knowledge(P) => smarter(P))).
fof(fact_harry_reads, axiom, reads(harry, walden)).
fof(goal, conjecture, ! [X] : (smarter(X) => gains_knowledge(X))).