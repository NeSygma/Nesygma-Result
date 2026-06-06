fof(breeding_back_def, axiom, 
    form_of(breeding_back, artificial_selection)).

fof(heck_cattle_bred, axiom,
    bred_back(heck_cattle, aurochs, t1920s)).

fof(heck_cattle_animal, axiom,
    animal(heck_cattle)).

fof(aurochs_animal, axiom,
    animal(aurochs)).

fof(some_bred_back_resemble_extinct, axiom,
    ? [X, Y, T] : (bred_back(X, Y, T) & animal(X) & resemble(X, Y) & extinct(Y))).

fof(goal, conjecture, ~extinct(aurochs)).