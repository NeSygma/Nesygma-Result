fof(all_peters_mammals_are_animals, axiom,
    ! [X] : ((peter_pet(X) & mammal(X)) => animal(X))).

fof(all_monkeys_are_mammals, axiom,
    ! [X] : (monkey(X) => mammal(X))).

fof(peters_pets_are_monkeys_or_birds, axiom,
    ! [X] : (peter_pet(X) => (monkey(X) | bird(X)))).

fof(peters_birds_can_fly, axiom,
    ! [X] : ((peter_pet(X) & bird(X)) => can_fly(X))).

fof(peters_pet_animals_can_breathe, axiom,
    ! [X] : ((peter_pet(X) & animal(X)) => can_breathe(X))).

fof(peter_pet_can_fly_implies_has_wings, axiom,
    ! [X] : ((peter_pet(X) & can_fly(X)) => has_wings(X))).

fof(rock_is_peters_pet, axiom,
    peter_pet(rock)).

fof(rock_can_fly_or_bird_or_cannot_breathe, axiom,
    can_fly(rock) | bird(rock) | ~can_breathe(rock)).

fof(goal, conjecture,
    monkey(rock)).