fof(book_contains_knowledge, axiom,
    ! [B] : (book(B) => contains_knowledge(B, tons_of_knowledge))).

fof(reads_gains_knowledge, axiom,
    ! [P, B] : (reads(P, B) => gains_knowledge(P))).

fof(gains_knowledge_smarter, axiom,
    ! [P] : (gains_knowledge(P) => smarter(P))).

fof(harry_is_person, axiom, person(harry)).
fof(walden_is_book, axiom, book(walden)).
fof(harry_reads_walden, axiom, reads(harry, walden)).

fof(conclusion, conjecture,
    contains_knowledge(walden, tons_of_knowledge)).