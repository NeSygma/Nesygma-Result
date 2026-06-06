% Premises about books, reading, and knowledge
fof(book_knowledge, axiom, ! [X] : (book(X) => contains_knowledge(X))).
fof(reading_gains_knowledge, axiom, ! [P, B] : ((person(P) & book(B) & reads(P, B)) => gains_knowledge(P))).
fof(knowledge_makes_smarter, axiom, ! [P] : (gains_knowledge(P) => smarter(P))).

% Facts about Harry and Walden
fof(harry_person, axiom, person(harry)).
fof(walden_book, axiom, book(walden)).
fof(harry_read_walden, axiom, reads(harry, walden)).

% Negated conclusion
fof(goal_neg, conjecture, ~smarter(harry)).