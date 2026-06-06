fof(animal_classification, axiom, ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).
fof(invertebrate_vertebrate_disjoint, axiom, ! [X] : (~(invertebrate(X) & vertebrate(X)))).
fof(invertebrate_implies_animal, axiom, ! [X] : (invertebrate(X) => animal(X))).
fof(vertebrate_implies_animal, axiom, ! [X] : (vertebrate(X) => animal(X))).
fof(backbone_mating, axiom, ! [X] : ((animal(X) & has_backbone(X)) => reproduces_by_mating(X))).
fof(vertebrate_has_backbone, axiom, ! [X] : (vertebrate(X) => has_backbone(X))).
fof(bees_no_mating, axiom, ! [X] : (bee(X) => ~reproduces_by_mating(X))).
fof(queen_bee_is_bee, axiom, ! [X] : (queen_bee(X) => bee(X))).
fof(harry_is_bee, axiom, bee(harry)).
fof(goal_neg, conjecture, ~(invertebrate(harry) | queen_bee(harry))).