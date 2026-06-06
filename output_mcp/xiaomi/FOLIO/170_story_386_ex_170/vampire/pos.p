fof(deadly_survival, axiom, ! [X] : (deadly_disease(X) => low_survival_rate(X))).
fof(severe_deadly, axiom, ! [X] : (severe_cancer(X) => deadly_disease(X))).
fof(bile_duct_severe, axiom, severe_cancer(bile_duct_cancer_inst)).
fof(cholangio_bile, axiom, ! [X] : (cholangiocarcinoma(X) => bile_duct_cancer(X))).
fof(mild_flu_low, axiom, low_survival_rate(mild_flu)).
fof(colorectal_constraint, axiom, ~(bile_duct_cancer(colorectal_cancer) & low_survival_rate(colorectal_cancer))).
fof(goal, conjecture, severe_cancer(colorectal_cancer)).