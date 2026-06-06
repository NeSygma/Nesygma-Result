fof(read_rule, axiom, ! [P, B] : (read(P, B) => gains_knowledge(P))).
fof(knowledge_rule, axiom, ! [P] : (gains_knowledge(P) => becomes_smarter(P))).
fof(fact_read, axiom, read(harry, walden)).
fof(goal, conjecture, ~becomes_smarter(harry)).