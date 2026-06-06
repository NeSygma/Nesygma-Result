% Axioms
fof(prem1, axiom, ! [X] : ((student(X) & works_in_library(X)) => ~cs_dept(X))).
fof(prem2, axiom, ! [X] : ((student(X) & has_part_time_job(X)) => works_in_library(X))).
fof(prem3, axiom, ! [X] : (taking_db(X) => cs_dept(X))).
fof(prem4, axiom, ! [X] : (taking_class_with_David(X) => taking_db(X))).
fof(prem5, axiom, ! [X] : (works_in_lab(X) => taking_class_with_David(X))).
fof(prem6_student, axiom, student(james)).
fof(prem6_lab, axiom, works_in_lab(james)).
fof(prem7, axiom, ~works_in_lab(james) | ~has_part_time_job(james)).
fof(conclusion_neg, conjecture, ~taking_db(james)).