fof(animal_types, axiom, ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).
fof(backbone_mating, axiom, ! [X] : ((animal(X) & has_backbone(X)) => reproduce_male_female(X))).
fof(vertebrate_backbone, axiom, ! [X] : ((animal(X) & vertebrate(X)) => has_backbone(X))).
fof(bee_no_mating, axiom, ! [X] : (bee(X) => ~reproduce_male_female(X))).
fof(queen_is_bee, axiom, ! [X] : (queen_bee(X) => bee(X))).
fof(harry_bee, axiom, bee(harry)).
fof(goal, conjecture, ~queen_bee(harry)).