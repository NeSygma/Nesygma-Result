fof(pets_mammals_are_animals, axiom, 
    ! [X] : (((is_peter_pet(X) & is_mammal(X)) => is_animal(X)))).

fof(all_monkeys_are_mammals, axiom, 
    ! [X] : (is_monkey(X) => is_mammal(X))).

fof(pets_are_monkeys_or_birds, axiom, 
    ! [X] : (is_peter_pet(X) => (is_monkey(X) | is_bird(X)))).

fof(peter_birds_can_fly, axiom, 
    ! [X] : ((is_peter_pet(X) & is_bird(X)) => can_fly(X))).

fof(peter_pet_animals_can_breathe, axiom, 
    ! [X] : ((is_peter_pet(X) & is_animal(X)) => can_breathe(X))).

fof(peter_pet_can_fly_has_wings, axiom, 
    ! [X] : ((is_peter_pet(X) & can_fly(X)) => has_wings(X))).

fof(rock_is_peter_pet, axiom, 
    is_peter_pet(rock)).

fof(rock_fly_or_bird_or_cannot_breathe, axiom, 
    (can_fly(rock) | is_bird(rock) | ~can_breathe(rock))).

fof(goal, conjecture, 
    is_monkey(rock)).