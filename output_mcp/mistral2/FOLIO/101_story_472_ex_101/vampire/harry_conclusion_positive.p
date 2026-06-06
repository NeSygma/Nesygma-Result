fof(animals_are_invertebrates_or_vertebrates, axiom,
    ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).

fof(animals_with_backbones_reproduce_by_mating, axiom,
    ! [X] : (animal_with_backbone(X) => reproduces_by_mating(X))).

fof(vertebrates_have_backbones, axiom,
    ! [X] : (vertebrate(X) => animal_with_backbone(X))).

fof(bees_do_not_reproduce_by_mating, axiom,
    ! [X] : (is_a(X, bee) => ~reproduces_by_mating(X))).

fof(queen_bees_are_bees, axiom,
    ! [X] : (is_a(X, queen_bee) => is_a(X, bee))).

fof(harry_is_a_bee, axiom,
    is_a(harry, bee)).

fof(harry_is_an_animal, axiom,
    animal(harry)).

fof(distinct_types, axiom,
    (bee != queen_bee)).

fof(conclusion, conjecture,
    ( (vertebrate(harry) & animal_with_backbone(harry)) |
      (~vertebrate(harry) & ~animal_with_backbone(harry)) )
    =>
    ( ~invertebrate(harry) & ~is_a(harry, queen_bee) )).