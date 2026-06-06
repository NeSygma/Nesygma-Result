fof(read_gains, axiom, ! [P,B] : (read(P,B) => gains_knowledge(P))).
fof(gains_smarter, axiom, ! [P] : (gains_knowledge(P) => smarter(P))).
fof(read_harry, axiom, read(harry, walden)).
fof(distinct_harry_walden, axiom, harry != walden).
fof(conjecture, conjecture, ? [P] : (smarter(P) & ~gains_knowledge(P))).