fof(axiom_deadly_disease, axiom, ! [X] : (deadly_disease(X) => low_survival_rate(X))).
fof(axiom_severe_cancer, axiom, ! [X] : (severe_cancer(X) => deadly_disease(X))).
fof(axiom_bile_duct_cancer, axiom, ! [X] : (bile_duct_cancer(X) => severe_cancer(X))).
fof(axiom_cholangiocarcinoma, axiom, bile_duct_cancer(cholangiocarcinoma)).
fof(axiom_mild_flu, axiom, low_survival_rate(mild_flu)).
fof(axiom_distinct, axiom, (cholangiocarcinoma != mild_flu & cholangiocarcinoma != colorectal_cancer & mild_flu != colorectal_cancer)).
fof(axiom_not_both, axiom, ~ (bile_duct_cancer(colorectal_cancer) & low_survival_rate(colorectal_cancer))).
fof(conclusion, conjecture, severe_cancer(colorectal_cancer)).