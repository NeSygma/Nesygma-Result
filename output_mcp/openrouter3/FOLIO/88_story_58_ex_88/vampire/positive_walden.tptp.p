fof(all_books_contain_knowledge, axiom, ! [B] : contains_knowledge(B)).
fof(reads_gains_knowledge, axiom, ! [P,B] : (reads(P,B) => gains_knowledge(P))).
fof(gains_knowledge_smarter, axiom, ! [P] : (gains_knowledge(P) => becomes_smarter(P))).
fof(harry_reads_walden, axiom, reads(harry, walden)).
fof(goal, conjecture, contains_knowledge(walden)).