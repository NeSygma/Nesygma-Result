fof(axiom_book_knowledge, axiom, ! [X] : (book(X) => contains_knowledge(X))).
fof(axiom_read_gives_knowledge, axiom, ! [X,Y] : ((person(X) & book(Y) & reads(X,Y)) => gains_knowledge(X))).
fof(axiom_gain_smarter, axiom, ! [X] : (gains_knowledge(X) => smarter(X))).
fof(fact_harry_person, axiom, person(harry)).
fof(fact_walden_book, axiom, book(walden)).
fof(fact_reads_harry_walden, axiom, reads(harry, walden)).
fof(conjecture, conjecture, ! [X] : (~smarter(X) | ~gains_knowledge(X))).