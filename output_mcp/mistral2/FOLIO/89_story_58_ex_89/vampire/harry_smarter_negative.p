fof(reads_knowledge, axiom, ! [P, B] : (reads(P, B) => gains_knowledge(P))).
fof(knowledge_smarter, axiom, ! [P] : (gains_knowledge(P) => becomes_smarter(P))).
fof(harry_reads_walden, axiom, reads(harry, walden)).
fof(goal_negation, conjecture, ~becomes_smarter(harry)).