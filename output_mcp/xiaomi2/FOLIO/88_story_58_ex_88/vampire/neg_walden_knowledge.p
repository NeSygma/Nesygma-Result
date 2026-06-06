fof(books_contain_knowledge, axiom,
    ! [X] : (book(X) => contains_knowledge(X))).

fof(reading_gives_knowledge, axiom,
    ! [P, B] : ((person(P) & book(B) & reads(P, B)) => gains_knowledge(P))).

fof(knowledge_makes_smarter, axiom,
    ! [P] : ((person(P) & gains_knowledge(P)) => becomes_smarter(P))).

fof(harry_reads_walden, axiom,
    (person(harry) & book(walden) & reads(harry, walden))).

fof(goal, conjecture, ~contains_knowledge(walden)).