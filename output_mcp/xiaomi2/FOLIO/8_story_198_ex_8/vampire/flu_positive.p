fof(p1, axiom, ! [X] : (monkeypox_virus_occurs(X) => may_get_monkeypox(X))).
fof(p2, axiom, ? [X] : (animal(X) & monkeypox_virus_occurs(X))).
fof(p3, axiom, ! [X] : (human(X) => mammal(X))).
fof(p4, axiom, ! [X] : (mammal(X) => animal(X))).
fof(p5, axiom, ! [X] : (may_get_monkeypox(X) => has_tiredness(X))).
fof(p6, axiom, ! [X] : ((human(X) & gets_flu(X)) => has_tiredness(X))).
fof(conclusion, conjecture, ! [X] : (human(X) => ~gets_flu(X))).