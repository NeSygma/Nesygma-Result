fof(deadly_implies_low, axiom, ! [X] : (deadly_disease(X) => low_survival_rate(X))).
fof(severe_implies_deadly, axiom, ! [X] : (severe_cancer(X) => deadly_disease(X))).
fof(bile_duct_implies_severe, axiom, ! [X] : (bile_duct_cancer(X) => severe_cancer(X))).
fof(cholangiocarcinoma_implies_bile, axiom, ! [X] : (cholangiocarcinoma(X) => bile_duct_cancer(X))).
fof(mild_flu_implies_low, axiom, ! [X] : (mild_flu(X) => low_survival_rate(X))).
fof(mild_flu_fact, axiom, mild_flu(mild_flu)).
fof(bile_duct_fact, axiom, bile_duct_cancer(bile_duct_cancer)).
fof(cholangiocarcinoma_fact, axiom, cholangiocarcinoma(cholangiocarcinoma)).
fof(colorectal_fact, axiom, colorectal_cancer(colorectal_cancer)).
fof(colorectal_not_bile_and_low, axiom, ~ (bile_duct_cancer(colorectal_cancer) & low_survival_rate(colorectal_cancer))).
fof(distincts, axiom, (bile_duct_cancer != cholangiocarcinoma & bile_duct_cancer != colorectal_cancer & bile_duct_cancer != mild_flu & cholangiocarcinoma != colorectal_cancer & cholangiocarcinoma != mild_flu & colorectal_cancer != mild_flu)).
fof(goal, conjecture, severe_cancer(colorectal_cancer)).