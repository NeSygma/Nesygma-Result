% Positive version: original conclusion as conjecture
% Conclusion: A smarter person has gained knowledge.
% Formalized as: ! [X] : (smarter(X) => gained_knowledge(X))

fof(premise_1, axiom, ! [B] : (book(B) => contains_knowledge(B))).
fof(premise_2, axiom, ! [P, B] : ((person(P) & book(B) & reads(P, B)) => gains_knowledge(P))).
fof(premise_3, axiom, ! [P] : ((person(P) & gains_knowledge(P)) => smarter(P))).
fof(premise_4, axiom, person(harry)).
fof(premise_5, axiom, book(walden)).
fof(premise_6, axiom, reads(harry, walden)).

fof(goal, conjecture, ! [X] : ((person(X) & smarter(X)) => gains_knowledge(X))).