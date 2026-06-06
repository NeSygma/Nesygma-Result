fof(books_contain_knowledge, axiom, ! [B] : contains_knowledge(B)).
fof(reads_implies_gains_knowledge, axiom, ! [P, B] : (reads(P, B) => gains_knowledge(P))).
fof(gains_knowledge_implies_smarter, axiom, ! [P] : (gains_knowledge(P) => becomes_smarter(P))).
fof(harry_reads_walden, axiom, reads(harry, walden)).
fof(conclusion_negation, conjecture, ! [P] : (~becomes_smarter(P) | ~gains_knowledge(P))).