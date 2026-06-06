fof(has_virus_implies_monkeypox, axiom,
    ! [X] : (has_virus(X, monkeypox_virus) => has_monkeypox(X))).

fof(monkeypox_in_animals, axiom,
    ? [Y] : (is_animal(Y) & has_virus(Y, monkeypox_virus))).

fof(humans_are_mammals, axiom,
    ! [X] : (is_human(X) => is_mammal(X))).

fof(mammals_are_animals, axiom,
    ! [X] : (is_mammal(X) => is_animal(X))).

fof(monkeypox_symptoms, axiom,
    ! [X] : (has_monkeypox(X) =>
             (has_symptom(X, fever) &
              has_symptom(X, headache) &
              has_symptom(X, muscle_pains) &
              has_symptom(X, tiredness)))).

fof(flu_causes_tiredness, axiom,
    ! [X] : (has_flu(X) => feels_tired(X))).

fof(goal_negation, conjecture,
    ~ (? [X] : is_animal(X))).