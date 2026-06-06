fof(breeding_back_is_artificial, axiom,
    ! [X] : (bred_back(X) => artificial_selection(X))).

fof(heck_cattle_bred_back, axiom,
    bred_back(heck_cattle)).

fof(heck_cattle_is_animal, axiom,
    animal(heck_cattle)).

fof(aurochs_is_animal, axiom,
    animal(aurochs)).

fof(aurochs_extinct, axiom,
    extinct(aurochs)).

fof(heck_cattle_resemble_aurochs, axiom,
    resemble(heck_cattle, aurochs)).

fof(some_bred_back_resemble_extinct, axiom,
    ? [X, Y] : (bred_back(X) & animal(X) & resemble(X, Y) & extinct(Y))).

fof(goal, conjecture,
    ? [X] : (animal(X) & artificial_selection(X))).