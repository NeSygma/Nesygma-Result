% Axioms and negated conjecture for negative case
fof(exist_axiom, axiom, ? [X] : (bred_back(X) & ? [Y] : (resembles(X, Y) & extinct(Y)))).
fof(bred_back_heck_cattle, axiom, bred_back(heck_cattle)).
fof(resembles_heck_cattle_aurochs, axiom, resembles(heck_cattle, aurochs)).
fof(animal_heck_cattle, axiom, animal(heck_cattle)).
fof(animal_aurochs, axiom, animal(aurochs)).
fof(distinct_heck_aurochs, axiom, heck_cattle != aurochs).
fof(goal, conjecture, ~extinct(aurochs)).