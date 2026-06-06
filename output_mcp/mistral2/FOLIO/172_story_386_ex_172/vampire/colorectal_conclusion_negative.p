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

fof(colorectal_cancer_not_both, axiom,
    ~(bile_duct_cancer(colorectal_cancer) & low_survival_rate(colorectal_cancer))).

fof(negated_conclusion, conjecture,
    ~(cholangiocarcinoma(colorectal_cancer) &
      (mild_flu(colorectal_cancer) | bile_duct_cancer(colorectal_cancer)))).