fof(books_knowledge, axiom, ! [B] : contains_tons_of_knowledge(B)).
fof(reads_gain, axiom, ! [P, B] : (reads(P, B) => gains_knowledge(P))).
fof(gain_smarter, axiom, ! [P] : (gains_knowledge(P) => smarter(P))).
fof(harry_read, axiom, reads(harry, walden)).
fof(distinct, axiom, harry != walden).
fof(goal, conjecture, ! [P] : (smarter(P) => gains_knowledge(P))).