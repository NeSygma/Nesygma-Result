fof(some_mammals_have_teeth, axiom, ? [X] : (mammal(X) & has_teeth(X))).
fof(platypus_no_teeth, axiom, ~has_teeth(platypus)).
fof(platypus_is_mammal, axiom, mammal(platypus)).
fof(human_has_teeth, axiom, has_teeth(human)).
fof(conclusion, conjecture, mammal(human)).