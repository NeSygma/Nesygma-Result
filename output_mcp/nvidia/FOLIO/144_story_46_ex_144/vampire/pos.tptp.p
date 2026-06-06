fof(axiom_animal_heck, axiom, animal(heck_cattle)).
fof(axiom_animal_aurochs, axiom, animal(aurochs)).
fof(axiom_bred_back, axiom, bred_back(heck_cattle)).
fof(axiom_resembles, axiom, resembles(heck_cattle, aurochs)).
fof(axiom_implies_extinct, axiom, ! [X,Y] : ((bred_back(X) & resembles(X,Y)) => extinct(Y)).
fof(conclusion, conjecture, extinct(aurochs)).