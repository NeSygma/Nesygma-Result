fof(horse_has_hooves, axiom, ! [X] : (horse(X) => has_hooves(X))).
fof(human_no_hooves, axiom, ! [X] : (human(X) => ~has_hooves(X))).
fof(conclusion, conjecture, ? [X] : (human(X) & horse(X))).