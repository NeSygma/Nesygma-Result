fof(some_mammals_have_teeth, axiom, ? [X] : (mammal(X) & has_teeth(X))).
fof(platypuses_no_teeth, axiom, ! [X] : (platypus(X) => ~has_teeth(X))).
fof(platypuses_are_mammals, axiom, ! [X] : (platypus(X) => mammal(X))).
fof(humans_have_teeth, axiom, ! [X] : (human(X) => has_teeth(X))).
fof(conclusion_negation, conjecture, ~(! [X] : (platypus(X) => (mammal(X) & ~has_teeth(X))))).