% Premises about diseases and survival rates
fof(deadly_disease_implies_low_survival, axiom, 
    ! [X] : (deadly_disease(X) => low_survival_rate(X))).

fof(severe_cancer_is_deadly, axiom, 
    ! [X] : (severe_cancer(X) => deadly_disease(X))).

fof(bile_duct_cancer_is_severe, axiom, 
    severe_cancer(bile_duct_cancer)).

fof(cholangiocarcinoma_is_bile_duct, axiom, 
    ! [X] : (cholangiocarcinoma(X) => bile_duct_cancer(X))).

fof(mild_flu_low_survival, axiom, 
    low_survival_rate(mild_flu)).

fof(colorectal_cancer_not_both, axiom, 
    ~(bile_duct_cancer(colorectal_cancer) & low_survival_rate(colorectal_cancer))).

% Answer predicate mapping for conclusion options
fof(option1_mapping, axiom, 
    (cholangiocarcinoma(colorectal_cancer) => ans(option1))).

fof(option2_mapping, axiom, 
    (mild_flu(colorectal_cancer) => ans(option2))).

fof(option3_mapping, axiom, 
    (bile_duct_cancer(colorectal_cancer) => ans(option3))).

fof(option4_mapping, axiom, 
    ((cholangiocarcinoma(colorectal_cancer) & mild_flu(colorectal_cancer) & bile_duct_cancer(colorectal_cancer)) => ans(option4))).

% The conclusion: colorectal cancer is a form of Cholangiocarcinoma and it is a kind of mild flu or a kind of bile duct cancer, or all of the above
fof(goal, conjecture, ? [X] : ans(X)).