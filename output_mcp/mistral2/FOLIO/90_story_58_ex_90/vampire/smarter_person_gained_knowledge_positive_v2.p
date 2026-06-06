fof(book_contains_knowledge, axiom, ! [B] : (book(B) => contains_knowledge(B))).
fof(reads_gains_knowledge, axiom, ! [P, B] : (reads(P, B) => gains_knowledge(P, B))).
fof(gains_knowledge_makes_smarter, axiom, ! [P] : (? [B] : gains_knowledge(P, B) => smarter(P))).
fof(harry_reads_walden, axiom, reads(harry, walden)).
fof(walden_is_book, axiom, book(walden)).
fof(conclusion, conjecture, ? [P] : (smarter(P) & ? [B] : gains_knowledge(P, B))).