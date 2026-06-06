fof(premise_2, axiom, ! [P, B] : ((person(P) & book(B) & reads(P, B)) => gains_knowledge(P))).
fof(premise_3, axiom, ! [P] : (gains_knowledge(P) => smarter(P))).
fof(premise_4, axiom, (person(harry) & book(walden) & reads(harry, walden))).
fof(goal, conjecture, ~ ! [P] : (smarter(P) => gains_knowledge(P))).