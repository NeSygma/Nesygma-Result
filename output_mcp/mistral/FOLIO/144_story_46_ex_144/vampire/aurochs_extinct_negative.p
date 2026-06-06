fof(bred_back_definition, axiom, ! [X] : (bred_back(X) => domestic_animal(X))).
fof(heck_cattle_bred_back, axiom, bred_back(heck_cattle)).
fof(heck_cattle_resembles_aurochs, axiom, resembles(heck_cattle, aurochs)).
fof(heck_cattle_is_animal, axiom, animal(heck_cattle)).
fof(aurochs_is_animal, axiom, animal(aurochs)).
fof(some_bred_back_resemble_extinct, axiom, ? [X] : (bred_back(X) & animal(X) & ? [Y] : (extinct(Y) & resembles(X, Y)))).
fof(goal, conjecture, ~extinct(aurochs)).