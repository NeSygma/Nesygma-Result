fof(some_mammals_have_teeth, axiom, ? [X] : (mammal(X) & has_teeth(X))).
fof(platypuses_no_teeth, axiom, no_teeth(platypus)).
fof(platypuses_are_mammals, axiom, mammal(platypus)).
fof(humans_have_teeth, axiom, has_teeth(human)).
fof(distinct_entities, axiom, (platypus != human)).
fof(negated_conclusion, conjecture, ~reptile(platypus)).