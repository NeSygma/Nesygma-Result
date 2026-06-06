% Negative version
fof(ax1, axiom, ![B] : (occurs(monkeypox_virus, B) => may_get_monkeypox(B))).
fof(ax2, axiom, ?[A] : (animal(A) & occurs(monkeypox_virus, A))).
fof(ax3, axiom, ![X] : (human(X) => mammal(X))).
fof(ax4, axiom, ![X] : (mammal(X) => animal(X))).
fof(ax5_fever, axiom, symptom_of(monkeypox, fever)).
fof(ax5_headache, axiom, symptom_of(monkeypox, headache)).
fof(ax5_muscle, axiom, symptom_of(monkeypox, muscle_pain)).
fof(ax5_tired, axiom, symptom_of(monkeypox, tiredness)).
fof(ax6, axiom, ![P] : (gets(P, flu) => feels_tired(P))).
fof(distinct, axiom, (monkeypox_virus != monkeypox & monkeypox != flu & flu != coughing & coughing != fever & fever != headache & headache != muscle_pain & muscle_pain != tiredness)).
fof(goal, conjecture, ~symptom_of(monkeypox, coughing)).