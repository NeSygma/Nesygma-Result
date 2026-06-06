% Problem: KiKi is terricolous - Positive version
% Premises
fof(jane_does_not_like_barking_animals, axiom, 
    ! [X] : (animal(X) & barks(X) => ~likes_jane(X))).

fof(dogs_are_barking_animals, axiom, 
    ! [X] : (dog(X) => (animal(X) & barks(X)))).

fof(jane_likes_jumping_animals, axiom, 
    ! [X] : (animal(X) & jumps(X) => likes_jane(X))).

fof(has_legs_implies_jumps, axiom, 
    ! [X] : (animal(X) & has_legs(X) => jumps(X))).

fof(terricolous_implies_has_legs, axiom, 
    ! [X] : (animal(X) & terricolous(X) => has_legs(X))).

fof(kiki_is_animal, axiom, animal(kiki)).

fof(kiki_conditional, axiom, 
    ~(jumps(kiki) & has_legs(kiki)) => (terricolous(kiki) | has_legs(kiki))).

% Conclusion to prove
fof(goal, conjecture, terricolous(kiki)).