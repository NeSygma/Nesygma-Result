fof(tons_of_knowledge, axiom, ! [X] : (book(X) => tons_of_knowledge(X)).
fof(gains_from_reading, axiom, ! [P,B] : ((reads(P,B) & book(B)) => gains_knowledge(P)).)
fof(gains_implies_smarter, axiom, ! [P] : (gains_knowledge(P) => smarter(P)).)
fof(fact_book_walden, axiom, book(walden)).
fof(fact_harry_reads_walden, axiom, reads(harry, walden)).
fof(goal, conjecture, smarter(harry)).