fof(vertebrate_has_backbone, axiom, ! [X] : (vertebrate(X) => has_backbone(X))).
fof(backbone_reproduces_by_mating, axiom, ! [X] : (has_backbone(X) => reproduces_by_mating(X))).
fof(bee_no_mating, axiom, ! [X] : (bee(X) => ~reproduces_by_mating(X))).
fof(queen_bee_is_bee, axiom, ! [X] : (queen_bee(X) => bee(X))).
fof(harry_is_bee, axiom, bee(harry)).
fof(harry_is_queen_bee, conjecture, queen_bee(harry)).