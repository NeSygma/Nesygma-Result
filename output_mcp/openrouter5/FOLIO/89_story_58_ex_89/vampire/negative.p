% Negative version: negated claim as conjecture
% Premises:
% 1. Books contain tons of knowledge.
% 2. When a person reads a book, that person gains knowledge.
% 3. If a person gains knowledge, they become smarter.
% 4. Harry read the book "Walden" by Henry Thoreau.

% Negated Conclusion: Harry is NOT smarter than before.

% Predicates:
% book(X) - X is a book
% contains_knowledge(X) - X contains knowledge
% person(X) - X is a person
% reads(X, Y) - X reads Y
% gains_knowledge(X) - X gains knowledge
% smarter_than_before(X) - X is smarter than before

fof(book_walden, axiom, book(walden)).
fof(books_contain_knowledge, axiom, ! [B] : (book(B) => contains_knowledge(B))).
fof(read_gains_knowledge, axiom, ! [P, B] : ((person(P) & book(B) & reads(P, B)) => gains_knowledge(P))).
fof(gains_knowledge_smarter, axiom, ! [P] : ((person(P) & gains_knowledge(P)) => smarter_than_before(P))).
fof(harry_person, axiom, person(harry)).
fof(harry_read_walden, axiom, reads(harry, walden)).

fof(goal_negated, conjecture, ~smarter_than_before(harry)).