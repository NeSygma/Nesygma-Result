% Negative version: Negated conclusion as conjecture
fof(animal_definition, axiom, ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).
fof(backbone_reproduction, axiom, ! [X] : (backbone(X) => reproduce_by_mating(X))).
fof(vertebrate_backbone, axiom, ! [X] : (vertebrate(X) => backbone(X))).
fof(bee_no_mating, axiom, ! [X] : (bee(X) => ~reproduce_by_mating(X))).
fof(queen_bee_is_bee, axiom, ! [X] : (queen_bee(X) => bee(X))).
fof(harry_is_bee, axiom, bee(harry)).
fof(goal_negation, conjecture, ~(((vertebrate(harry) & backbone(harry)) | (~vertebrate(harry) & ~backbone(harry))) => (~invertebrate(harry) & ~queen_bee(harry)))).