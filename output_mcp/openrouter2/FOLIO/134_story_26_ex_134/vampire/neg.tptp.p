fof(ex_mammal_teeth, axiom, ? [X] : (mammal(X) & have_teeth(X))).
fof(platypus_no_teeth, axiom, ! [X] : (platypus(X) => ~have_teeth(X))).
fof(platypus_is_mammal, axiom, ! [X] : (platypus(X) => mammal(X))).
fof(human_has_teeth, axiom, ! [X] : (human(X) => have_teeth(X))).
fof(conjecture, conjecture, ? [X] : (human(X) & ~mammal(X))).