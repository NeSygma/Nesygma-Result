% Negative version
fof(distinct_entities, axiom, (harry != walden)).
fof(book_walden, axiom, book(walden)).
fof(all_books_knowledge, axiom, ! [B] : (book(B) => contains_knowledge(B))).
fof(reads_fact, axiom, reads(harry, walden)).
fof(reads_gain, axiom, ! [P,B] : ((reads(P,B) & book(B)) => gains_knowledge(P))).
fof(gain_smarter, axiom, ! [P] : (gains_knowledge(P) => smarter(P))).
fof(goal, conjecture, ~smarter(harry)).