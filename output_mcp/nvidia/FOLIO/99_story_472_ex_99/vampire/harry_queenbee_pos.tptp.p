fof(axiom_animal_disjunction, axiom, ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X))).)
fof(axiom_backbone_reproduction, axiom, ! [X] : ((animal(X) & has_backbone(X)) => reproduces_by_male_female(X))).
fof(axiom_vertebrate_backbone, axiom, ! [X] : (vertebrate(X) => has_backbone(X))).
fof(axiom_bee_no_reproduction, axiom, ! [X] : (bee(X) => ~reproduces_by_male_female(X))).
fof(axiom_queenbee_implies_bee, axiom, ! [X] : (queen_bee(X) => bee(X))).
fof(fact_harry_bee, axiom, bee(harry)).
fof(conjecture, conjecture, queen_bee(harry)).