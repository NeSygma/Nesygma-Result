fof(p1, axiom, ! [X] : (works_in_library(X) => ~from_cs(X))).
fof(p2, axiom, ! [X] : (part_time_job_offered_by_university(X) => works_in_library(X))).
fof(p3, axiom, ! [X] : (takes_database_course(X) => from_cs(X))).
fof(p4, axiom, ! [X] : (takes_class_with_professor_david(X) => takes_database_course(X))).
fof(p5, axiom, ! [X] : (works_in_lab(X) => takes_class_with_professor_david(X))).
fof(p6, axiom, works_in_lab(j)).
fof(p7, axiom, (~works_in_lab(j) | ~part_time_job_offered_by_university(j))).
fof(goal, conjecture, ~(takes_database_course(j) | part_time_job_offered_by_university(j))).