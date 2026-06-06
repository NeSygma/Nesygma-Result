% Negative version
fof(p1, axiom, ! [X] : (works_in_library(X) => ~from_cs_dept(X))).
fof(p2, axiom, ! [X] : (has_part_time_job_univ(X) => works_in_library(X))).
fof(p3, axiom, ! [X] : (takes_database_course(X) => from_cs_dept(X))).
fof(p4, axiom, ! [X] : (takes_class_with_prof_david(X) => takes_database_course(X))).
fof(p5, axiom, ! [X] : (works_in_lab(X) => takes_class_with_prof_david(X))).
fof(f1, axiom, works_in_lab(james)).
fof(f2, axiom, (~works_in_lab(james) | ~has_part_time_job_univ(james))).
fof(goal, conjecture, (~takes_database_course(james) & ~has_part_time_job_univ(james))).