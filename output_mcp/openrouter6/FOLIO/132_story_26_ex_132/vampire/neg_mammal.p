fof(premise_1, axiom, ? [X] : (mammal(X) & has_teeth(X))).
fof(premise_2, axiom, ~has_teeth(p)).
fof(premise_3, axiom, mammal(p)).
fof(premise_4, axiom, has_teeth(h)).
fof(neg_conclusion, conjecture, ~mammal(p) | has_teeth(p)).