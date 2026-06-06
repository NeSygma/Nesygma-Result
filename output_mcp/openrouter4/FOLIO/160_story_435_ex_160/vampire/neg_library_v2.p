% Negative version: Conjecture = James does NOT take the database course
% Premise 7 interpreted as: ~works_in_lab(james) | ~university_part_time_job(james)
fof(premise_1, axiom, ! [X] : (works_in_library(X) => ~cs_department(X))).
fof(premise_2, axiom, ! [X] : (university_part_time_job(X) => works_in_library(X))).
fof(premise_3, axiom, ! [X] : (takes_database_course(X) => cs_department(X))).
fof(premise_4, axiom, ! [X] : (takes_class_with_david(X) => takes_database_course(X))).
fof(premise_5, axiom, ! [X] : (works_in_lab(X) => takes_class_with_david(X))).
fof(premise_6, axiom, student(james) & works_in_lab(james)).
fof(premise_7, axiom, ~works_in_lab(james) | ~university_part_time_job(james)).
fof(goal, conjecture, ~takes_database_course(james)).