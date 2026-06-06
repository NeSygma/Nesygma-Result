% Positive version: original claim as conjecture
% Premises:
% 1. All of New Vessel Press's published books are in English.
% 2. Neapolitan Chronicles is a book published by New Vessel Press.
% 3. Neapolitan Chronicles was translated from Italian.
% 4. Palace of Flies is a book published by New Vessel Press.
% Conclusion: Harry Potter was published by New Vessel Press.

fof(all_english, axiom, ! [B] : (published_by_new_vessel(B) => in_english(B))).
fof(neapolitan_published, axiom, published_by_new_vessel(neapolitan_chronicles)).
fof(neapolitan_translated, axiom, translated_from_italian(neapolitan_chronicles)).
fof(palace_published, axiom, published_by_new_vessel(palace_of_flies)).

fof(goal, conjecture, published_by_new_vessel(harry_potter)).