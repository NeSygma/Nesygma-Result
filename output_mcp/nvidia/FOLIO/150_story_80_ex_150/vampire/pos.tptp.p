% Axiom: All books published by New Vessel Press are English books.
fof(pub_impl, axiom, ! [X] : (published_by(new_vessel_press, X) => english_book(X))).
% Fact: New Vessel Press published Neapolitan Chronicles.
fof(fact_published, axiom, published_by(new_vessel_press, neapolitan_chronicles)).
% Fact: Palace of Flies is also published by New Vessel Press.
fof(fact_palace, axiom, published_by(new_vessel_press, palace_of_flies)).
% Conjecture: Neapolitan Chronicles is an English book.
fof(goal, conjecture, english_book(neapolitan_chronicles)).