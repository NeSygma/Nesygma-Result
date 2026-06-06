fof(bark_implies_not_liked, axiom, 
    ! [A] : (bark(A) => ~likes_jane(A))).

fof(all_dogs_bark, axiom, 
    ! [A] : (dog(A) => bark(A))).

fof(jump_implies_liked, axiom, 
    ! [A] : (jump(A) => likes_jane(A))).

fof(has_legs_implies_jump, axiom, 
    ! [A] : (has_legs(A) => jump(A))).

fof(terricolous_implies_has_legs, axiom, 
    ! [A] : (terricolous(A) => has_legs(A))).

fof(kiki_is_animal, axiom, 
    animal(kiki)).

fof(kiiki_premise, axiom, 
    (~jump(kiki) & ~has_legs(kiki)) => (terricolous(kiki) | has_legs(kiki))).

fof(conclusion_negation, conjecture, 
    ~(~bark(kiki) & ~dog(kiki))).