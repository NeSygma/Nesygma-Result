fof(deadly_disease_implies_low_survival, axiom, ! [X] : (deadly_disease(X) => low_survival_rate(X))).
fof(severe_cancer_implies_deadly, axiom, ! [X] : (severe_cancer(X) => deadly_disease(X))).
fof(bile_duct_implies_severe, axiom, ! [X] : (bile_duct_cancer(X) => severe_cancer(X))).
fof(cholangiocarcinoma_implies_bile_duct, axiom, ! [X] : (cholangiocarcinoma(X) => bile_duct_cancer(X))).
fof(mild_flu_implies_low_survival, axiom, ! [X] : (mild_flu(X) => low_survival_rate(X))).
fof(colorectal_not_bile_duct_and_low_survival, axiom, ~(bile_duct_cancer(colorectal_cancer) & low_survival_rate(colorectal_cancer))).
fof(conclusion, conjecture, severe_cancer(colorectal_cancer)).