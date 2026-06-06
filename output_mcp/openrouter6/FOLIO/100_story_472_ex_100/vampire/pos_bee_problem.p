fof(animal_categories, axiom, ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).
fof(disjoint_categories, axiom, ! [X] : (invertebrate(X) => ~vertebrate(X))).
fof(invertebrate_animal, axiom, ! [X] : (invertebrate(X) => animal(X))).
fof(vertebrate_animal, axiom, ! [X] : (vertebrate(X) => animal(X))).
fof(backbone_reproduction, axiom, ! [X] : (has_backbone(X) => reproduces_by_mating(X))).
fof(vertebrate_backbone, axiom, ! [X] : (vertebrate(X) => has_backbone(X))).
fof(bees_no_mating, axiom, ! [X] : (bee(X) => ~reproduces_by_mating(X))).
fof(queen_bees_are_bees, axiom, ! [X] : (queen_bee(X) => bee(X))).
fof(harry_is_bee, axiom, bee(harry)).
fof(goal, conjecture, invertebrate(harry) | queen_bee(harry)).