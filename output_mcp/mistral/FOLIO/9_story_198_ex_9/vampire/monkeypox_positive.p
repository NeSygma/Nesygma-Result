fof(has_virus_implies_may_get_disease, axiom, 
    ! [X] : (has_virus(X, monkeypox_virus) => may_get_disease(X, monkeypox))).

fof(monkeypox_virus_in_animals, axiom, 
    ? [A] : (animal(A) & has_virus(A, monkeypox_virus))).

fof(humans_are_mammals, axiom, 
    ! [H] : (human(H) => mammal(H))).

fof(mammals_are_animals, axiom, 
    ! [M] : (mammal(M) => animal(M))).

fof(monkeypox_symptoms, axiom, 
    ! [X] : (has_disease(X, monkeypox) => 
             (has_symptom(X, fever) & 
              has_symptom(X, headache) & 
              has_symptom(X, muscle_pains) & 
              has_symptom(X, tiredness)))).

fof(flu_causes_tiredness, axiom, 
    ! [P] : (has_disease(P, flu) => has_symptom(P, tiredness))).

fof(goal, conjecture, 
    ! [X] : (has_disease(X, monkeypox) => has_symptom(X, coughing))).