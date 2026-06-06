fof(book_contains_knowledge, axiom, 
    ! [B] : (book(B) => contains_knowledge(B))).

fof(reads_implies_gains_knowledge, axiom, 
    ! [P, B] : (reads(P, B) => gains_knowledge(P))).

fof(gains_knowledge_implies_smarter, axiom, 
    ! [P] : (gains_knowledge(P) => becomes_smarter(P))).

fof(harry_reads_walden, axiom, 
    reads(harry, walden)).

fof(walden_is_book, axiom, 
    book(walden)).

fof(harry_is_person, axiom, 
    person(harry)).

fof(henry_thoreau_is_person, axiom, 
    person(henry_thoreau)).

fof(book_walden_authored_by_thoreau, axiom, 
    authored_by(walden, henry_thoreau)).

fof(distinct_henry_walden, axiom, 
    henry_thoreau != walden).

fof(distinct_harry_henry, axiom, 
    harry != henry_thoreau).

fof(distinct_harry_walden, axiom, 
    harry != walden).

fof(goal_negation, conjecture, 
    ~smarter_than(harry, before)).