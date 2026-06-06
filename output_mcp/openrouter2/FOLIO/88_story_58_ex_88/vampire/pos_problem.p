fof(book_walden, axiom, book(walden)).
fof(read_harry_walden, axiom, read(harry, walden)).
fof(book_contains_knowledge, axiom, ! [X] : (book(X) => contains_knowledge(X))).
fof(read_gains_knowledge, axiom, ! [P,B] : (read(P,B) => gains_knowledge(P))).
fof(gains_knowledge_smarter, axiom, ! [P] : (gains_knowledge(P) => smarter(P))).
fof(conclusion, conjecture, contains_knowledge(walden)).