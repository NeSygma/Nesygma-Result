fof(book_walden, axiom, book(walden)).

fof(reading_gives_knowledge, axiom,
    ! [P, B] : ((person(P) & book(B) & read(P, B)) => gains_knowledge(P))).

fof(knowledge_makes_smarter, axiom,
    ! [P] : (gains_knowledge(P) => smarter(P))).

fof(harry_is_person, axiom, person(harry)).

fof(harry_read_walden, axiom, read(harry, walden)).

fof(goal, conjecture, smarter(harry)).