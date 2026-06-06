fof(all_peters_mammal_pets_are_animals, axiom, 
    ! [X] : ((pet_of(peter, X) & mammal(X)) => animal(X)).

fof(all_monkeys_are_mammals, axiom, 
    ! [X] : (monkey(X) => mammal(X)).

fof(peters_pets_are_monkeys_or_birds, axiom, 
    ! [X] : (pet_of(peter, X) => (monkey(X) | bird(X))).

fof(peters_birds_can_fly, axiom, 
    ! [X] : ((bird(X) & pet_of(peter, X)) => can_fly(X)).

fof(all_peters_animal_pets_can_breathe, axiom, 
    ! [X] : ((animal(X) & pet_of(peter, X)) => can_breathe(X)).

fof(pet_can_fly_implies_has_wings, axiom, 
    ! [X] : ((pet_of(peter, X) & can_fly(X)) => has_wings(X)).

fof(rock_is_peters_pet, axiom, 
    pet_of(peter, rock)).

fof(rock_fly_or_bird_or_cannot_breathe, axiom, 
    can_fly(rock) | bird(rock) | ~can_breathe(rock)).

fof(goal_negation, conjecture, 
    ~has_wings(rock)).