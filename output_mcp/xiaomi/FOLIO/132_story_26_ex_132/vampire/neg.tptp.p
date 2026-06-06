fof(some_mammals_have_teeth, axiom, ? [X] : (mammal(X) & has_teeth(X))).
fof(platypus_no_teeth, axiom, ! [X] : (platypus(X) => ~has_teeth(X))).
fof(platypus_is_mammal, axiom, ! [X] : (platypus(X) => mammal(X))).
fof(humans_have_teeth, axiom, ! [X] : (human(X) => has_teeth(X))).
fof(platypus_exists, axiom, platypus(p)).
fof(human_exists, axiom, human(h)).
fof(goal, conjecture, ~(! [X] : (platypus(X) => (mammal(X) & ~has_teeth(X))))).