% Positive TPTP file: original conclusion as conjecture
fof(animal_invertebrate_or_vertebrate, axiom,
    ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).
fof(invertebrate_exclusive, axiom,
    ! [X] : (invertebrate(X) => ~vertebrate(X))).
fof(vertebrate_exclusive, axiom,
    ! [X] : (vertebrate(X) => ~invertebrate(X))).
fof(vertebrate_is_animal, axiom,
    ! [X] : (vertebrate(X) => animal(X))).
fof(invertebrate_is_animal, axiom,
    ! [X] : (invertebrate(X) => animal(X))).
fof(backbone_reproduces, axiom,
    ! [X] : ((animal(X) & backbone(X)) => reproduces_by_mating(X))).
fof(vertebrate_has_backbone, axiom,
    ! [X] : (vertebrate(X) => backbone(X))).
fof(bees_no_mating, axiom,
    ! [X] : (bee(X) => ~reproduces_by_mating(X))).
fof(queen_bee_is_bee, axiom,
    ! [X] : (queen_bee(X) => bee(X))).
fof(harry_is_bee, axiom, bee(harry)).
% Conclusion: P => Q
fof(conclusion, conjecture,
    ( (vertebrate(harry) & backbone(harry)) | (~vertebrate(harry) & ~backbone(harry)) )
    =>
    (~invertebrate(harry) & ~queen_bee(harry)) ).