fof(book_knowledge, axiom, ! [X] : (book(X) => contains_knowledge(X))).
fof(reading_gains, axiom, ! [P, B] : ((reads(P, B) & book(B)) => gains_knowledge(P))).
fof(knowledge_smarter, axiom, ! [P] : (gains_knowledge(P) => smarter(P))).
fof(harry_reads, axiom, reads(harry, walden)).
fof(walden_book, axiom, book(walden)).
fof(goal, conjecture, ? [P] : (smarter(P) & gains_knowledge(P))).