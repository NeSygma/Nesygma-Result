fof(monkeypox_virus_causes_monkeypox, axiom, 
    ! [X] : (has_virus(X, monkeypox_virus) => may_get_disease(X, monkeypox_disease))).

fof(monkeypox_virus_in_animals, axiom, 
    ? [X] : (animal(X) & has_virus(X, monkeypox_virus))).

fof(humans_are_mammals, axiom, 
    ! [X] : (human(X) => mammal(X))).

fof(mammals_are_animals, axiom, 
    ! [X] : (mammal(X) => animal(X))).

fof(flu_causes_tiredness, axiom, 
    ! [X] : (has_flu(X) => feels_tired(X))).

fof(conclusion_some_flu, conjecture, 
    ? [X] : has_flu(X)).