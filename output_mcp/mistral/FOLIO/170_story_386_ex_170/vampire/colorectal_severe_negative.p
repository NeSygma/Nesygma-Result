fof(deadly_disease_implies_low_survival, axiom, 
    ! [X] : (deadly_disease(X) => low_survival_rate(X))).

fof(severe_cancer_implies_deadly_disease, axiom, 
    ! [X] : (severe_cancer(X) => deadly_disease(X))).

fof(bile_duct_cancer_implies_severe_cancer, axiom, 
    ! [X] : (bile_duct_cancer(X) => severe_cancer(X))).

fof(cholangiocarcinoma_implies_bile_duct_cancer, axiom, 
    ! [X] : (cholangiocarcinoma(X) => bile_duct_cancer(X))).

fof(mild_flu_implies_low_survival, axiom, 
    ! [X] : (mild_flu(X) => low_survival_rate(X))).

fof(colorectal_not_both, axiom, 
    ! [X] : (colorectal_cancer(X) => ~(bile_duct_cancer(X) & low_survival_rate(X))) ).

fof(cholangiocarcinoma_type, axiom, 
    cholangiocarcinoma(cholangiocarcinoma_type)).

fof(mild_flu_type, axiom, 
    mild_flu(mild_flu_type)).

fof(colorectal_cancer_type, axiom, 
    colorectal_cancer(colorectal_cancer_type)).

fof(distinct_types, axiom, 
    (bile_duct_cancer_type != colorectal_cancer_type &
     bile_duct_cancer_type != cholangiocarcinoma_type &
     colorectal_cancer_type != cholangiocarcinoma_type)).

fof(conclusion_negation, conjecture, 
    ~severe_cancer(colorectal_cancer_type)).