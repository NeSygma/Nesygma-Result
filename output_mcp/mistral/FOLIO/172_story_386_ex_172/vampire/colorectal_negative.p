fof(deadly_disease_implies_low_survival, axiom, 
    ! [X] : (deadly_disease(X) => low_survival_rate(X))).

fof(severe_cancer_implies_deadly_disease, axiom, 
    ! [X] : (severe_cancer(X) => deadly_disease(X))).

fof(bile_duct_cancer_is_severe, axiom, 
    severe_cancer(bile_duct_cancer)).

fof(cholangiocarcinoma_implies_bile_duct, axiom, 
    ! [X] : (cholangiocarcinoma(X) => bile_duct_cancer(X))).

fof(mild_flu_has_low_survival, axiom, 
    low_survival_rate(mild_flu)).

fof(colorectal_not_both, axiom, 
    ~ (bile_duct_cancer(colorectal_cancer) & low_survival_rate(colorectal_cancer))).

fof(conclusion_negation, conjecture, 
    ~ (cholangiocarcinoma(colorectal_cancer) &
       (mild_flu(colorectal_cancer) | bile_duct_cancer(colorectal_cancer)))).