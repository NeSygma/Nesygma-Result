fof(book_decl, type, book: $tType).
fof(person_decl, type, person: $tType).
fof(state_decl, type, state: $tType).

fof(harry_type, type, harry: person).
fof(henry_thoreau_type, type, henry_thoreau: person).
fof(walden_type, type, walden: book).
fof(before_type, type, before: state).

fof(book_contains_knowledge, axiom, 
    ! [B: book] : (contains_knowledge(B))).

fof(reads_implies_gains_knowledge, axiom, 
    ! [P: person, B: book] : (reads(P, B) => gains_knowledge(P))).

fof(gains_knowledge_implies_smarter, axiom, 
    ! [P: person] : (gains_knowledge(P) => becomes_smarter(P))).

fof(harry_reads_walden, axiom, 
    reads(harry, walden)).

fof(walden_is_book, axiom, 
    book(walden)).

fof(harry_is_person, axiom, 
    person(harry)).

fof(henry_thoreau_is_person, axiom, 
    person(henry_thoreau)).

fof(distinct_henry_walden, axiom, 
    henry_thoreau != walden).

fof(distinct_harry_henry, axiom, 
    harry != henry_thoreau).

fof(distinct_harry_walden, axiom, 
    harry != walden).

fof(distinct_before_harry, axiom, 
    before != harry).

fof(distinct_before_walden, axiom, 
    before != walden).

fof(distinct_before_henry, axiom, 
    before != henry_thoreau).

fof(goal, conjecture, 
    smarter_than(harry, before)).