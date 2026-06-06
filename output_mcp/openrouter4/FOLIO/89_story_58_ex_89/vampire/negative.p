% Negative: negated claim as conjecture
fof(premise1, axiom, ! [B] : (book(B) => contains_knowledge(B))).
fof(premise2, axiom, ! [P, B] : ((person(P) & book(B) & reads(P, B)) => gains_knowledge(P))).
fof(premise3, axiom, ! [P] : ((person(P) & gains_knowledge(P)) => becomes_smarter(P))).
fof(fact_harry_person, axiom, person(harry)).
fof(fact_walden_book, axiom, book(walden)).
fof(fact_harry_reads, axiom, reads(harry, walden)).
fof(conjecture_neg, conjecture, ~becomes_smarter(harry)).