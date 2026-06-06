fof(peter_pet_mammal_animal, axiom,
    ! [X] : ((peter_pet(X) & mammal(X)) => animal(X))).

fof(monkey_mammal, axiom,
    ! [X] : (monkey(X) => mammal(X))).

fof(peter_pet_monkey_or_bird, axiom,
    ! [X] : (peter_pet(X) => (monkey(X) | bird(X)))).

fof(peter_bird_can_fly, axiom,
    ! [X] : ((peter_pet(X) & bird(X)) => can_fly(X))).

fof(peter_pet_animal_can_breathe, axiom,
    ! [X] : ((peter_pet(X) & animal(X)) => can_breathe(X))).

fof(peter_pet_can_fly_has_wings, axiom,
    ! [X] : ((peter_pet(X) & can_fly(X)) => has_wings(X))).

fof(rock_is_peter_pet, axiom,
    peter_pet(rock)).

fof(rock_fly_or_bird_or_not_breathe, axiom,
    can_fly(rock) | bird(rock) | ~can_breathe(rock)).

fof(conclusion, conjecture,
    ~has_wings(rock)).