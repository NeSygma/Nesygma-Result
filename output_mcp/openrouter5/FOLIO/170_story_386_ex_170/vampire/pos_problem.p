% Positive version: original claim as conjecture
% Premises:

% If something is a deadly disease, then it comes with a low survival rate.
fof(premise_1, axiom, ! [X] : (deadly_disease(X) => low_survival_rate(X))).

% Severe cancers are deadly diseases.
fof(premise_2, axiom, ! [X] : (severe_cancer(X) => deadly_disease(X))).

% Bile duct cancer is a severe form cancer.
fof(premise_3, axiom, ! [X] : (bile_duct_cancer(X) => severe_cancer(X))).

% All Cholangiocarcinoma is bile duct cancer.
fof(premise_4, axiom, ! [X] : (cholangiocarcinoma(X) => bile_duct_cancer(X))).

% Mild flu comes with a low survival rate.
fof(premise_5, axiom, low_survival_rate(mild_flu)).

% Colorectal cancer is not both a bile duct cancer and with a low survival rate.
fof(premise_6, axiom, ~(bile_duct_cancer(colorectal_cancer) & low_survival_rate(colorectal_cancer))).

% Distinct entities
fof(distinct, axiom, (colorectal_cancer != mild_flu)).

% Conclusion: Colorectal cancer is a kind of severe cancer
fof(goal, conjecture, severe_cancer(colorectal_cancer)).