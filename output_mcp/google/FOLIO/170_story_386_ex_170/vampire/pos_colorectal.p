fof(p1, axiom, ! [X] : (deadly_disease(X) => low_survival_rate(X))).
fof(p2, axiom, ! [X] : (severe_cancer(X) => deadly_disease(X))).
fof(p3, axiom, ! [X] : (bile_duct_cancer(X) => severe_cancer(X))).
fof(p4, axiom, ! [X] : (cholangiocarcinoma(X) => bile_duct_cancer(X))).
fof(p5, axiom, low_survival_rate(mild_flu)).
fof(p6, axiom, ~ (bile_duct_cancer(colorectal_cancer) & low_survival_rate(colorectal_cancer))).
fof(goal, conjecture, severe_cancer(colorectal_cancer)).