fof(axiom_breeding_back, axiom, ! [X] : (bred_back(X) => artificially_selected(X))).
fof(axiom_heck_cattle_bred_back, axiom, bred_back(heck_cattle)).
fof(axiom_heck_cattle_animal, axiom, animal(heck_cattle)).
fof(axiom_aurochs_animal, axiom, animal(aurochs)).
fof(axiom_distinct_hc_aurochs, axiom, (heck_cattle != aurochs)).
fof(neg_conclusion, conjecture, ~artificially_selected(heck_cattle)).