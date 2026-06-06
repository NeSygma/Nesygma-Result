fof(book_knowledge, axiom, ! [B] : (book(B) => ? [K] : contains_knowledge(B, K))).
fof(reads_gains, axiom, ! [P, B] : ((person(P) & book(B) & reads(P, B)) => gains_knowledge(P))).
fof(gains_smarter, axiom, ! [P] : (gains_knowledge(P) => smarter(P))).
fof(harry_reads_walden, axiom, person(harry) & book(walden) & reads(harry, walden)).
fof(goal, conjecture, ~(! [P] : (smarter(P) => gains_knowledge(P)))).