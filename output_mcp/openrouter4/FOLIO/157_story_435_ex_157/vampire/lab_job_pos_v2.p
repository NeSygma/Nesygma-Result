% Positive: conjecture is univ_job(james)
% Premise 7 interpreted as disjunction: ~works_lab(james) | ~univ_job(james)
fof(premise_1, axiom, ! [X] : (works_library(X) => ~cs_dept(X))).
fof(premise_2, axiom, ! [X] : (univ_job(X) => works_library(X))).
fof(premise_3, axiom, ! [X] : (takes_db(X) => cs_dept(X))).
fof(premise_4, axiom, ! [X] : (takes_david(X) => takes_db(X))).
fof(premise_5, axiom, ! [X] : (works_lab(X) => takes_david(X))).
fof(premise_6, axiom, works_lab(james)).
fof(premise_7, axiom, (~works_lab(james) | ~univ_job(james))).
fof(goal, conjecture, univ_job(james)).