fof(some_mammals_have_teeth, axiom,
    ? [X] : (mammal(X) & has_teeth(X))).
fof(platypuses_no_teeth, axiom,
    ! [X] : (platypus(X) => ~has_teeth(X))).
fof(platypuses_are_mammals, axiom,
    ! [X] : (platypus(X) => mammal(X))).
fof(humans_have_teeth, axiom,
    ! [X] : (human(X) => has_teeth(X))).
fof(platypus_exists, axiom, platypus(perry)).
fof(human_exists, axiom, human(alice)).
fof(goal, conjecture,
    ! [X] : (platypus(X) => reptile(X))).