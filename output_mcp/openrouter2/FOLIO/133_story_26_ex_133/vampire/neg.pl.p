fof(ex_mammal_has_teeth, axiom, ? [X] : (mammal(X) & has_teeth(X))).
fof(platypus_no_teeth, axiom, ! [X] : (platypus(X) => ~has_teeth(X))).
fof(platypus_is_mammal, axiom, ! [X] : (platypus(X) => mammal(X))).
fof(human_has_teeth, axiom, ! [X] : (human(X) => has_teeth(X))).
fof(conjecture, conjecture, ? [X] : (platypus(X) & ~reptile(X))).