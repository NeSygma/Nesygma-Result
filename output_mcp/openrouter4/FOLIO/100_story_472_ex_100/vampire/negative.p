fof(premise1, axiom, ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).
fof(premise2, axiom, ! [X] : ((animal(X) & has_backbone(X)) => reproduce_mf(X))).
fof(premise3, axiom, ! [X] : ((animal(X) & vertebrate(X)) => has_backbone(X))).
fof(premise4, axiom, ! [X] : (bee(X) => ~reproduce_mf(X))).
fof(premise5, axiom, ! [X] : (queen_bee(X) => bee(X))).
fof(premise6, axiom, bee(harry)).
fof(conclusion, conjecture, (~invertebrate(harry) & ~queen_bee(harry))).