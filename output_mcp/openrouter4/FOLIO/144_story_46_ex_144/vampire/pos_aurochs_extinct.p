% Positive run: claim that aurochs are extinct
fof(premise_1, axiom,
    ! [X] : (bred_back(X) => resembles(X, some_extinct_animal))).
fof(premise_2, axiom,
    (bred_back(heck_cattle) & resembles(heck_cattle, aurochs))).
fof(premise_3, axiom, animal(heck_cattle)).
fof(premise_4, axiom, animal(aurochs)).
fof(premise_5, axiom,
    ? [X, Y] : (animal(X) & bred_back(X) & animal(Y) & extinct(Y) & resembles(X, Y))).
fof(conclusion, conjecture, extinct(aurochs)).