% Negative version: test if negation of conclusion follows from premises
% Negated conclusion: James DOES have a part-time job offered by the university.

fof(premise_1, axiom, ! [X] : (works_library(X) => ~cs_dept(X))).
fof(premise_2, axiom, ! [X] : (pt_job_univ(X) => works_library(X))).
fof(premise_3, axiom, ! [X] : (takes_database(X) => cs_dept(X))).
fof(premise_4, axiom, ! [X] : (takes_class_david(X) => takes_database(X))).
fof(premise_5, axiom, ! [X] : (works_lab(X) => takes_class_david(X))).
fof(premise_6, axiom, works_lab(james)).
% Premise 7: ~works_lab(james) | ~pt_job_univ(james)
fof(premise_7, axiom, ~works_lab(james) | ~pt_job_univ(james)).

fof(neg_conclusion, conjecture, pt_job_univ(james)).