% Positive run: prove extinct(aurochs)
fof(distinct_consts, axiom, (heck_cattle != aurochs)).
fof(animal_heck, axiom, animal(heck_cattle)).
fof(animal_aurochs, axiom, animal(aurochs)).
fof(bred_back_fact, axiom, bred_back(heck_cattle, aurochs)).
fof(exist_some, axiom, ? [X] : (animal(X) & to_be_bred_back(X) & resembles_extinct(X))).
fof(goal, conjecture, extinct(aurochs)).