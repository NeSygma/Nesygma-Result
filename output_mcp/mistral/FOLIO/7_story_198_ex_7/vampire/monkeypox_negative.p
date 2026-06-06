fof(monkeypox_virus_occurs_in_being, axiom, 
    ! [X] : (has_virus(X, monkeypox_virus) => has_monkeypox(X))).

fof(monkeypox_virus_in_animals, axiom, 
    ? [X] : (is_animal(X) & can_have_virus(X, monkeypox_virus))).

fof(humans_are_mammals, axiom, 
    ! [X] : (is_human(X) => is_mammal(X))).

fof(mammals_are_animals, axiom, 
    ! [X] : (is_mammal(X) => is_animal(X))).

fof(goal_negation, conjecture, 
    ~ (? [X] : is_animal(X))).