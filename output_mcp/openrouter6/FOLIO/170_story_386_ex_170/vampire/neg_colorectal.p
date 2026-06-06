% Negative: negated conclusion ~severe_cancer(colorectal_cancer)
fof(deadly_disease_implies_low_survival, axiom, ! [X] : (deadly_disease(X) => low_survival_rate(X))).
fof(severe_cancer_implies_deadly_disease, axiom, ! [X] : (severe_cancer(X) => deadly_disease(X))).
fof(bile_duct_cancer_is_severe, axiom, severe_cancer(bile_duct_cancer)).
fof(cholangiocarcinoma_is_bile_duct, axiom, bile_duct_cancer(cholangiocarcinoma)).
fof(mild_flu_low_survival, axiom, low_survival_rate(mild_flu)).
fof(colorectal_cancer_not_both, axiom, ~(bile_duct_cancer(colorectal_cancer) & low_survival_rate(colorectal_cancer))).
fof(distinct_entities, axiom, (bile_duct_cancer != cholangiocarcinoma & bile_duct_cancer != mild_flu & bile_duct_cancer != colorectal_cancer & cholangiocarcinoma != mild_flu & cholangiocarcinoma != colorectal_cancer & mild_flu != colorectal_cancer)).
fof(goal, conjecture, ~severe_cancer(colorectal_cancer)).