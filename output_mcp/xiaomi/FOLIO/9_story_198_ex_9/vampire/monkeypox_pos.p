fof(mpox_symptom_fever, axiom, symptom_of_monkeypox(fever)).
fof(mpox_symptom_headache, axiom, symptom_of_monkeypox(headache)).
fof(mpox_symptom_muscle_pains, axiom, symptom_of_monkeypox(muscle_pains)).
fof(mpox_symptom_tiredness, axiom, symptom_of_monkeypox(tiredness)).

fof(distinct_symptoms, axiom, (
    fever != headache &
    fever != muscle_pains &
    fever != tiredness &
    headache != muscle_pains &
    headache != tiredness &
    muscle_pains != tiredness &
    coughing != fever &
    coughing != headache &
    coughing != muscle_pains &
    coughing != tiredness
)).

fof(goal, conjecture, symptom_of_monkeypox(coughing)).