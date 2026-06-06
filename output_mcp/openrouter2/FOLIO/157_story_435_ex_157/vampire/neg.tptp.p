fof(prem1, axiom, ! [X] : (works_in_library(X) => ~from_cs_department(X))).
fof(prem2, axiom, ! [X] : (part_time_job_offered_by_university(X) => works_in_library(X))).
fof(prem3, axiom, ! [X] : (taking_database_course(X) => from_cs_department(X))).
fof(prem4, axiom, ! [X] : (taking_class_with_professor_david(X) => taking_database_course(X))).
fof(prem5, axiom, ! [X] : (works_in_lab(X) => taking_class_with_professor_david(X))).
fof(prem6, axiom, student(james)).
fof(prem7, axiom, works_in_lab(james)).
fof(prem8, axiom, (~works_in_lab(james) | ~part_time_job_offered_by_university(james))).
fof(goal, conjecture, ~part_time_job_offered_by_university(james)).