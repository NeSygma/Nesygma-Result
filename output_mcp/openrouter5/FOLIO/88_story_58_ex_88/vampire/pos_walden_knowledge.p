% Positive version: original claim as conjecture
% Premises:
% 1. Books contain tons of knowledge.
fof(books_contain_knowledge, axiom, ! [B] : (book(B) => contains_knowledge(B))).

% 2. When a person reads a book, that person gains knowledge.
fof(read_gains_knowledge, axiom, ! [P, B] : ((person(P) & book(B) & reads(P, B)) => gains_knowledge(P))).

% 3. If a person gains knowledge, they become smarter.
fof(gains_becomes_smarter, axiom, ! [P] : (gains_knowledge(P) => becomes_smarter(P))).

% 4. Harry read the book "Walden" by Henry Thoreau.
fof(harry_reads_walden, axiom, reads(harry, walden)).
fof(harry_is_person, axiom, person(harry)).
fof(walden_is_book, axiom, book(walden)).

% Conclusion: Walden contains knowledge.
fof(conclusion, conjecture, contains_knowledge(walden)).