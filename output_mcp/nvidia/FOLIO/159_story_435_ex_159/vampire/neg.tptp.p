% Axioms
fof(none_cs_lib, axiom, ! [X] : (works_in_library(X) => ~ from_cs_department(X))).
fof(part_time_job_implies_lib, axiom, ! [X] : (has_part_time_job(X) => works_in_library(X))).
fof(db_course_implies_cs, axiom, ! [X] : (taking_database_course(X) => from_cs_department(X))).
fof(class_with_david_implies_db, axiom, ! [X] : (taking_class_with_david(X) => taking_database_course(X))).
fof(lab_implies_class, axiom, ! [X] : (works_in_lab(X) => taking_class_with_david(X))).
fof(james_works_in_lab, axiom, works_in_lab(james)).
fof(james_not_lib, axiom, ~ works_in_library(james)).
fof(james_no_part_job, axiom, ~ has_part_time_job(james)).
% Negated conjecture
fof(neg_goal, conjecture, ~ (taking_database_course(james) | has_part_time_job(james))).