fof(has_teeth_some_mammals, axiom, ? [X] : (mammal(X) & has_teeth(X))).
fof(platypus_no_teeth, axiom, no_teeth(platypus)).
fof(platypus_is_mammal, axiom, mammal(platypus)).
fof(human_has_teeth, axiom, has_teeth(human)).
fof(no_teeth_def, axiom, ! [X] : (no_teeth(X) <=> ~has_teeth(X))).
fof(distinct_constants, axiom, (platypus != human)).
fof(conclusion, conjecture, (mammal(platypus) & no_teeth(platypus))).