fof(breeding_back_def, axiom, ! [X, Y] : (breeding_back(X, Y) => (animal(X) & animal(Y)))).
fof(heck_cattle_breeding_back, axiom, breeding_back(heck_cattle, aurochs)).
fof(heck_cattle_animal, axiom, animal(heck_cattle)).
fof(aurochs_animal, axiom, animal(aurochs)).
fof(some_animals_resemble_extinct, axiom, ? [X, Y] : (breeding_back(X, Y) & resemble(X, Y) & extinct(Y))).
fof(conclusion_negation, conjecture, ~extinct(aurochs)).