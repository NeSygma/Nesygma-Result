% Positive file: original conclusion as conjecture
% Premises
fof(premise_1, axiom, ! [X] : (deadly_disease(X) => low_survival_rate(X))).
fof(premise_2, axiom, ! [X] : (severe_cancer(X) => deadly_disease(X))).
fof(premise_3, axiom, ! [X] : (bile_duct_cancer(X) => severe_cancer(X))).
fof(premise_4, axiom, ! [X] : (cholangiocarcinoma(X) => bile_duct_cancer(X))).
fof(premise_5, axiom, ! [X] : (mild_flu(X) => low_survival_rate(X))).
fof(premise_6, axiom, ! [X] : ((colorectal_cancer(X) & bile_duct_cancer(X)) => ~low_survival_rate(X))).

% Conclusion: (A or B) => (A and C)
% where A = ! [X] : (colorectal_cancer(X) => bile_duct_cancer(X))
%       B = ! [X] : (colorectal_cancer(X) => cholangiocarcinoma(X))
%       C = ! [X] : (colorectal_cancer(X) => mild_flu(X))
fof(conclusion, conjecture,
    (! [X] : (colorectal_cancer(X) => bile_duct_cancer(X)) | ! [X] : (colorectal_cancer(X) => cholangiocarcinoma(X)))
    =>
    (! [X] : (colorectal_cancer(X) => bile_duct_cancer(X)) & ! [X] : (colorectal_cancer(X) => mild_flu(X)))
).