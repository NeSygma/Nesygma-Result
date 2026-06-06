fof(animal_type, axiom, ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).
fof(backbone_mating, axiom, ! [X] : ((animal(X) & has_backbone(X)) => reproduces_by_mating(X))).
fof(vertebrate_backbone, axiom, ! [X] : (vertebrate(X) => has_backbone(X))).
fof(bee_mating, axiom, ! [X] : (bee(X) => ~reproduces_by_mating(X))).
fof(queen_bee_is_bee, axiom, ! [X] : (queen_bee(X) => bee(X))).
fof(harry_is_bee, axiom, bee(harry)).
fof(bees_are_animals, axiom, ! [X] : (bee(X) => animal(X))).
fof(queen_bees_are_animals, axiom, ! [X] : (queen_bee(X) => animal(X))).

fof(goal, conjecture, queen_bee(harry)).