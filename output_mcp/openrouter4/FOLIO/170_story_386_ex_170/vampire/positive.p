fof(premise1, axiom, ! [X] : (deadly_disease(X) => low_survival_rate(X))).
fof(premise2, axiom, ! [X] : (severe_cancer(X) => deadly_disease(X))).
fof(premise3, axiom, ! [X] : (bile_duct_cancer(X) => severe_cancer(X))).
fof(premise4, axiom, ! [X] : (cholangiocarcinoma(X) => bile_duct_cancer(X))).
fof(premise5, axiom, low_survival_rate(mild_flu)).
fof(premise6, axiom, ~ (bile_duct_cancer(colorectal_cancer) & low_survival_rate(colorectal_cancer))).
fof(distinct_constants, axiom, (mild_flu != colorectal_cancer & mild_flu != cholangiocarcinoma & colorectal_cancer != cholangiocarcinoma)).
fof(conjecture, conjecture, severe_cancer(colorectal_cancer)).