% Colorectal Cancer Problem - Negative Version
% Premises
fof(rule_1, axiom, ! [X] : (deadly_disease(X) => low_survival_rate(X))).
fof(rule_2, axiom, ! [X] : (severe_cancer(X) => deadly_disease(X))).
fof(rule_3, axiom, ! [X] : (bile_duct_cancer(X) => severe_cancer(X))).
fof(rule_4, axiom, ! [X] : (cholangiocarcinoma(X) => bile_duct_cancer(X))).
fof(rule_5, axiom, ! [X] : (mild_flu(X) => low_survival_rate(X))).
fof(rule_6, axiom, ! [X] : ~(colorectal_cancer(X) & bile_duct_cancer(X) & low_survival_rate(X))).

% Negated conclusion
fof(goal, conjecture, ~(colorectal_cancer(colorectal) => severe_cancer(colorectal))).