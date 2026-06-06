fof(mammals_have_teeth, axiom, ? [X] : (mammal(X) & has_teeth(X))).
fof(platypus_no_teeth, axiom, ! [X] : (platypus(X) => ~has_teeth(X))).
fof(platypus_is_mammal, axiom, ! [X] : (platypus(X) => mammal(X))).
fof(humans_have_teeth, axiom, ! [X] : (human(X) => has_teeth(X))).
fof(distinct, axiom, (platypus_instance != human_instance)).
fof(platypus_exists, axiom, platypus(platypus_instance)).
fof(human_exists, axiom, human(human_instance)).
fof(goal, conjecture, ~(! [X] : (human(X) => mammal(X)))).