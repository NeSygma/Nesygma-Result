fof(animal_types, axiom, ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).
fof(backbone_reproduction, axiom, ! [X] : (has_backbone(X) => reproduces_by_mating(X))).
fof(vertebrate_backbone, axiom, ! [X] : (vertebrate(X) => has_backbone(X))).
fof(bee_reproduction, axiom, ! [X] : (bee(X) => ~reproduces_by_mating(X))).
fof(queen_is_bee, axiom, ! [X] : (queen_bee(X) => bee(X))).
fof(harry_is_bee, axiom, bee(harry)).
fof(goal, conjecture, ~queen_bee(harry)).