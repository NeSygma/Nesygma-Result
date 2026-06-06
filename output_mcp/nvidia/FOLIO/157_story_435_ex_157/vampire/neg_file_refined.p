% Axioms
fof(axiom_none_cs_lib, axiom, ! [X] : ((student(X) & works_in_library(X)) => ~from_cs(X))).
fof(axiom_part_job_impl_lib, axiom, ! [X] : ((student(X) & part_job(X)) => works_in_library(X))).
fof(axiom_db_course_cs, axiom, ! [X] : ((student(X) & taking_db_course(X)) => from_cs(X))).
fof(axiom_class_David_db, axiom, ! [X] : (taking_class_with_David(X) => taking_db_course(X))).
fof(axiom_lab_David, axiom, ! [X] : (works_in_lab(X) => taking_class_with_David(X))).
fof(fact_james_student, axiom, student(james)).
fof(fact_james_lab, axiom, works_in_lab(james)).
% Conjecture (negated)
fof(conclusion, conjecture, ~part_job(james)).