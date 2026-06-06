fof(animal_dichotomy, axiom, ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).
fof(backbone_reproduce, axiom, ! [X] : ((animal(X) & backbone(X)) => reproduce_mf(X))).
fof(vertebrate_backbone, axiom, ! [X] : ((animal(X) & vertebrate(X)) => backbone(X))).
fof(bee_no_reproduce, axiom, ! [X] : (bee(X) => ~reproduce_mf(X))).
fof(queen_bee_is_bee, axiom, ! [X] : (queen_bee(X) => bee(X))).
fof(harry_is_bee, axiom, bee(harry)).
fof(goal, conjecture, queen_bee(harry)).