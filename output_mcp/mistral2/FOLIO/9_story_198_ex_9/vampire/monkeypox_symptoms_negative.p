fof(occurs_in_implies_monkeypox, axiom,
    ! [X] : (occurs_in(monkeypox_virus, X) => has_monkeypox(X))).

fof(monkeypox_in_animals, axiom,
    ? [X] : (is_animal(X) & occurs_in(monkeypox_virus, X))).

fof(humans_are_mammals, axiom,
    ! [X] : (human(X) => is_mammal(X))).

fof(mammals_are_animals, axiom,
    ! [X] : (is_mammal(X) => is_animal(X))).

fof(symptoms_of_monkeypox_fever, axiom,
    symptoms_of_monkeypox(fever)).

fof(symptoms_of_monkeypox_headache, axiom,
    symptoms_of_monkeypox(headache)).

fof(symptoms_of_monkeypox_muscle_pains, axiom,
    symptoms_of_monkeypox(muscle_pains)).

fof(symptoms_of_monkeypox_tiredness, axiom,
    symptoms_of_monkeypox(tiredness)).

fof(flu_implies_tired, axiom,
    ! [X] : (has_flu(X) => feels_tired_when_flu(X))).

fof(distinct_entities, axiom,
    (monkeypox_virus != coughing & monkeypox_virus != fever &
     monkeypox_virus != headache & monkeypox_virus != muscle_pains &
     monkeypox_virus != tiredness & coughing != fever & coughing != headache &
     coughing != muscle_pains & coughing != tiredness & fever != headache &
     fever != muscle_pains & fever != tiredness & headache != muscle_pains &
     headache != tiredness & muscle_pains != tiredness)).

fof(negated_conclusion, conjecture,
    ~symptoms_of_monkeypox(coughing)).