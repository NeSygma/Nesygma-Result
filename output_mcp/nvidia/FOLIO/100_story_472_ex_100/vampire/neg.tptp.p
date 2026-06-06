fof(axiom_1, axiom, ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).
fof(axiom_2, axiom, ! [X] : ((animal(X) & has_backbone(X)) => reproduces_by_mating(X))).
fof(axiom_3, axiom, ! [X] : (vertebrate(X) => has_backbone(X))).
fof(axiom_4, axiom, ! [X] : (bee(X) => ~reproduces_by_mating(X))).
fof(axiom_5, axiom, ! [X] : (queen_bee(X) => bee(X))).
fof(axiom_6, axiom, bee(harry)).
fof(axiom_7, axiom, ! [X] : (bee(X) => animal(X))).
fof(conclusion, conjecture, ~(invertebrate(harry) | queen_bee(harry))).