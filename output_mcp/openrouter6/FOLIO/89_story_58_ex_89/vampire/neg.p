fof(premise1, axiom, ! [X] : (book(X) => contains_knowledge(X))).
fof(premise2, axiom, ! [P, B] : (person(P) & book(B) & reads(P, B) => gains_knowledge(P))).
fof(premise3, axiom, ! [P] : (person(P) & gains_knowledge(P) => becomes_smarter(P))).
fof(premise4, axiom, person(harry)).
fof(premise5, axiom, book(walden)).
fof(premise6, axiom, reads(harry, walden)).
fof(goal, conjecture, ~becomes_smarter(harry)).