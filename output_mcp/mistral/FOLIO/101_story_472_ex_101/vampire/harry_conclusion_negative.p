fof(animals_are_invertebrates_or_vertebrates, axiom, 
    ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).

fof(animals_with_backbones_reproduce_by_mating, axiom, 
    ! [X] : ((has_backbone(X) & animal(X)) => reproduces_by_mating(X))).

fof(vertebrates_have_backbones, axiom, 
    ! [X] : ((vertebrate(X) & animal(X)) => has_backbone(X))).

fof(bees_do_not_reproduce_by_mating, axiom, 
    ! [X] : (bee(X) => ~reproduces_by_mating(X))).

fof(queen_bees_are_bees, axiom, 
    ! [X] : (queen_bee(X) => bee(X))).

fof(bees_are_animals, axiom, 
    ! [X] : (bee(X) => animal(X))).

fof(harry_is_a_bee, axiom, 
    bee(harry)).

fof(mutual_exclusivity_invertebrate_vertebrate, axiom, 
    ! [X] : (invertebrate(X) => ~vertebrate(X))).

fof(negated_conclusion, conjecture, 
    (((vertebrate(harry) & has_backbone(harry)) | (~vertebrate(harry) & ~has_backbone(harry))) 
     & (invertebrate(harry) | queen_bee(harry)))).