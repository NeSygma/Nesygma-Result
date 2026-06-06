fof(animal_invertebrate_vertebrate, axiom, ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).
fof(animal_backbone_mating, axiom, ! [X] : ((animal(X) & backbone(X)) => male_female_mating(X))).
fof(vertebrate_backbone, axiom, ! [X] : (vertebrate(X) => backbone(X))).
fof(bee_no_mating, axiom, ! [X] : (bee(X) => ~male_female_mating(X))).
fof(queen_bee_bee, axiom, ! [X] : (queen_bee(X) => bee(X))).
fof(harry_bee, axiom, bee(harry)).
fof(conclusion_neg, conjecture, ((vertebrate(harry) & backbone(harry)) | (~vertebrate(harry) & ~backbone(harry))) & (invertebrate(harry) | queen_bee(harry))).