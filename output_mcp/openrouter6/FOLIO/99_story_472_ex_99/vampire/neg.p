fof(premise1a, axiom, ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).
fof(premise1b, axiom, ! [X] : (invertebrate(X) => ~vertebrate(X))).
fof(premise1c, axiom, ! [X] : (vertebrate(X) => ~invertebrate(X))).
fof(premise2, axiom, ! [X] : (animal(X) & has_backbone(X) => reproduces_by_mating(X))).
fof(premise3, axiom, ! [X] : (vertebrate(X) => has_backbone(X))).
fof(premise4, axiom, ! [X] : (bee(X) => ~reproduces_by_mating(X))).
fof(premise5, axiom, ! [X] : (queen_bee(X) => bee(X))).
fof(premise6, axiom, bee(harry)).
fof(goal, conjecture, ~queen_bee(harry)).