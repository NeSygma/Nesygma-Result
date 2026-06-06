% Problem: Harry is an invertebrate or a queen bee (negated)
% Premises
fof(animal_types, axiom, ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).
fof(backbone_reproduction, axiom, ! [X] : (backbone(X) => reproduce_by_mating(X))).
fof(vertebrate_backbone, axiom, ! [X] : (vertebrate(X) => backbone(X))).
fof(bee_reproduction, axiom, ! [X] : (bee(X) => ~reproduce_by_mating(X))).
fof(queen_is_bee, axiom, ! [X] : (queen_bee(X) => bee(X))).
fof(harry_is_bee, axiom, bee(harry)).

% Negated conclusion
fof(goal_negated, conjecture, ~(invertebrate(harry) | queen_bee(harry))).