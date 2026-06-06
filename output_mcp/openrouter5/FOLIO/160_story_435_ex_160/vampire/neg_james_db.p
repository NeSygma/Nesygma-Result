% Negative version: conjecture is "James does NOT take the database course"
fof(premise_1, axiom, ! [X] : ((student(X) & works_library(X)) => ~cs_dept(X))).
fof(premise_2, axiom, ! [X] : ((student(X) & uni_parttime_job(X)) => works_library(X))).
fof(premise_3, axiom, ! [X] : ((student(X) & takes_db_course(X)) => cs_dept(X))).
fof(premise_4, axiom, ! [X] : ((student(X) & takes_class_with_david(X)) => takes_db_course(X))).
fof(premise_5, axiom, ! [X] : ((student(X) & works_lab(X)) => takes_class_with_david(X))).
fof(premise_6, axiom, student(james)).
fof(premise_7, axiom, works_lab(james)).
fof(premise_8, axiom, ~works_lab(james) | ~uni_parttime_job(james)).

fof(goal, conjecture, ~takes_db_course(james)).