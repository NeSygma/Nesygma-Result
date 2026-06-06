fof(p1, axiom, ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).
fof(p2, axiom, ! [X] : ((animal(X) & has_backbone(X)) => reproduces_by_mating(X))).
fof(p3, axiom, ! [X] : (vertebrate(X) => has_backbone(X))).
fof(p4, axiom, ! [X] : (bee(X) => ~reproduces_by_mating(X))).
fof(p5, axiom, ! [X] : (queen_bee(X) => bee(X))).
fof(p6, axiom, bee(harry)).
fof(goal, conjecture, ~(((vertebrate(harry) & has_backbone(harry)) | (~vertebrate(harry) & ~has_backbone(harry))) => (~invertebrate(harry) & ~queen_bee(harry)))).