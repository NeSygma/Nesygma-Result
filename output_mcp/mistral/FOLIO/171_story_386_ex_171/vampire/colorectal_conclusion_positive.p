fof(implies_deadly_disease_low_survival, axiom, 
    ! [X] : (deadly_disease(X) => low_survival_rate(X))).

fof(severe_cancer_implies_deadly, axiom, 
    ! [X] : (severe_cancer(X) => deadly_disease(X))).

fof(bile_duct_cancer_is_severe, axiom, 
    severe_cancer(bdc)).

fof(bile_duct_cancer_is_bdc, axiom, 
    bile_duct_cancer(bdc)).

fof(all_cholangiocarcinoma_is_bdc, axiom, 
    ! [X] : (cholangiocarcinoma(X) => bile_duct_cancer(X))).

fof(mild_flu_exists, axiom, 
    mild_flu(mild_flu_c)).

fof(mild_flu_has_low_survival, axiom, 
    low_survival_rate(mild_flu_c)).

fof(colorectal_not_both_bdc_and_low_survival, axiom, 
    ~(bile_duct_cancer(colorectal_c) & low_survival_rate(colorectal_c))).

fof(conclusion, conjecture, 
    (bile_duct_cancer(colorectal_c) | cholangiocarcinoma(colorectal_c)) =>
    (bile_duct_cancer(colorectal_c) & mild_flu(colorectal_c))).