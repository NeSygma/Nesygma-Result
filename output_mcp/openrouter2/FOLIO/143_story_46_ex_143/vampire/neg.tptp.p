fof(rule_bred_back_is_artificial, axiom, ! [X] : (bred_back(X) => artificially_selected(X))).
fof(fact_bred_back_heck, axiom, bred_back(heck_cattle)).
fof(fact_heck_cattle, axiom, heck_cattle(heck_cattle)).
fof(fact_animal_heck, axiom, animal(heck_cattle)).
fof(fact_animal_aurochs, axiom, animal(aurochs)).
fof(conj_neg, conjecture, ! [X] : (heck_cattle(X) => ~artificially_selected(X))).