fof(book_contains_knowledge, axiom,
    ! [X] : book(X)).

fof(reading_gives_knowledge, axiom,
    ! [P, B] : ((person(P) & book(B) & reads(P, B)) => gains_knowledge(P))).

fof(knowledge_makes_smarter, axiom,
    ! [P] : (gains_knowledge(P) => smarter(P))).

fof(harry_is_person, axiom, person(harry)).

fof(walden_is_book, axiom, book(walden)).

fof(harry_read_walden, axiom, reads(harry, walden)).

fof(goal, conjecture, smarter(harry)).