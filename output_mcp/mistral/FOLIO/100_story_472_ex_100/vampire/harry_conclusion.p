fof(animals_are_invertebrates_or_vertebrates, axiom, 
    ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).

fof(animals_with_backbones_reproduce_by_mating, axiom, 
    ! [X] : (animal(X) & has_backbone(X) => reproduces_by_mating(X))).

fof(vertebrates_have_backbones, axiom, 
    ! [X] : (vertebrate(X) => has_backbone(X))).

fof(bees_dont_reproduce_by_mating, axiom, 
    ! [X] : (bee(X) => ~reproduces_by_mating(X))).

fof(queen_bees_are_bees, axiom, 
    ! [X] : (queen_bee(X) => bee(X))).

fof(bees_are_animals, axiom, 
    ! [X] : (bee(X) => animal(X))).

fof(queen_bees_are_animals, axiom, 
    ! [X] : (queen_bee(X) => animal(X))).

fof(harry_is_a_bee, axiom, 
    bee(harry)).

fof(conclusion, conjecture, 
    (invertebrate(harry) | queen_bee(harry))).