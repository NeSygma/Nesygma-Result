fof(book_contains_knowledge, axiom,
    ! [X] : (book(X) => contains_knowledge(X))).

fof(reading_gains_knowledge, axiom,
    ! [P, B] : ((person(P) & book(B) & reads(P, B)) => gains_knowledge(P))).

fof(gaining_makes_smarter, axiom,
    ! [P] : (gains_knowledge(P) => smarter(P))).

fof(walden_is_a_book, axiom, book(walden)).

fof(harry_is_a_person, axiom, person(harry)).

fof(harry_read_walden, axiom, reads(harry, walden)).

fof(goal, conjecture, contains_knowledge(walden)).