% Positive version
fof(rule_deadly_low, axiom, ! [X] : (deadly_disease(X) => low_survival_rate(X))).
fof(rule_severe_deadly, axiom, ! [X] : (severe_cancer(X) => deadly_disease(X))).
fof(rule_bile_severe, axiom, ! [X] : (bile_duct_cancer(X) => severe_cancer(X))).
fof(rule_chol_bile, axiom, ! [X] : (cholangiocarcinoma(X) => bile_duct_cancer(X))).
fof(rule_mild_low, axiom, ! [X] : (mild_flu(X) => low_survival_rate(X))).
fof(colorectal_not_bile_and_low, axiom, ~ (bile_duct_cancer(colorectal_cancer) & low_survival_rate(colorectal_cancer))).
fof(goal, conjecture, severe_cancer(colorectal_cancer)).