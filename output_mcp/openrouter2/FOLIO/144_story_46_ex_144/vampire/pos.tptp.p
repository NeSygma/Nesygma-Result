fof(bred_back_heck, axiom, bred_back(heck_cattle)).
fof(resembles_heck_aurochs, axiom, resembles(heck_cattle, aurochs)).
fof(animal_heck, axiom, animal(heck_cattle)).
fof(animal_aurochs, axiom, animal(aurochs)).
fof(rule_some_bred_back_resemble_extinct, axiom, ! [X,Y] : ((bred_back(X) & animal(X) & resembles(X,Y)) => extinct(Y))).
fof(conjecture, conjecture, extinct(aurochs)).