fof(premise1, axiom, ? [X] : (mammal(X) & has_teeth(X))).
fof(premise2, axiom, ~has_teeth(platypus)).
fof(premise3, axiom, mammal(platypus)).
fof(premise4, axiom, has_teeth(human)).
fof(distinct, axiom, platypus != human).
fof(goal, conjecture, ~mammal(human)).