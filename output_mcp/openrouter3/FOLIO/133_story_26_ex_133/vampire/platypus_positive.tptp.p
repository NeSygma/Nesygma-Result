% Positive file: Platypuses are reptiles
fof(premise_1, axiom, ? [X] : (mammal(X) & has_teeth(X))).
fof(premise_2, axiom, ~has_teeth(platypus)).
fof(premise_3, axiom, mammal(platypus)).
fof(premise_4, axiom, has_teeth(human)).
fof(distinct_entities, axiom, (platypus != human)).
fof(goal, conjecture, reptile(platypus)).