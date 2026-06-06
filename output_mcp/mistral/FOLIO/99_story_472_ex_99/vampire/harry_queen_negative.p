fof(disjoint_categories, axiom,
    ! [X] : (~(invertebrate(X) & vertebrate(X)))).

fof(cover_all_animals, axiom,
    ! [X] : (invertebrate(X) | vertebrate(X))).

fof(vertebrates_have_backbones, axiom,
    ! [X] : (vertebrate(X) => has_backbone(X))).

fof(backbones_imply_mating, axiom,
    ! [X] : (has_backbone(X) => reproduces_by_mating(X))).

fof(bees_no_mating, axiom,
    ! [X] : (bee(X) => ~reproduces_by_mating(X))).

fof(queen_bees_are_bees, axiom,
    ! [X] : (queen_bee(X) => bee(X))).

fof(harry_is_bee, axiom,
    bee(harry)).

fof(harry_is_not_queen_bee, conjecture,
    ~queen_bee(harry)).