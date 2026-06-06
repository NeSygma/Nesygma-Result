fof(mammal_has_teeth, axiom, ? [X] : (mammal(X) & has_teeth(X))).
fof(platypus_no_teeth, axiom, ~has_teeth(platypus)).
fof(platypus_mammal, axiom, mammal(platypus)).
fof(human_has_teeth, axiom, has_teeth(human)).
fof(goal, conjecture, ~reptile(platypus)).