fof(deadly_low_survival, axiom, ! [X] : (deadly_disease(X) => low_survival_rate(X))).
fof(severe_deadly, axiom, ! [X] : (severe_cancer(X) => deadly_disease(X))).
fof(severe_bile_duct, axiom, severe_cancer(bile_duct_cancer)).
fof(chol_bile, axiom, ! [X] : (cholangiocarcinoma(X) => bile_duct_cancer(X))).
fof(mild_low_survival, axiom, ! [X] : (mild_flu(X) => low_survival_rate(X))).
fof(colorectal_not_bile_and_low, axiom, ~ (bile_duct_cancer(colorectal_cancer) & low_survival_rate(colorectal_cancer))).
fof(distinct, axiom, colorectal_cancer != bile_duct_cancer).
fof(conclusion, conjecture, cholangiocarcinoma(colorectal_cancer) & (mild_flu(colorectal_cancer) | bile_duct_cancer(colorectal_cancer))).