fof(p1, axiom, ! [X] : (works_in_library(X) => ~from_cs(X))).
fof(p2, axiom, ! [X] : (part_time_job_offered(X) => works_in_library(X))).
fof(p3, axiom, ! [X] : (takes_database_course(X) => from_cs(X))).
fof(p4, axiom, ! [X] : (takes_with_prof_david(X) => takes_database_course(X))).
fof(p5, axiom, ! [X] : (works_in_lab(X) => takes_with_prof_david(X))).
fof(p6, axiom, works_in_lab(james)).
fof(p7, axiom, (~works_in_lab(james) | ~part_time_job_offered(james))).
fof(goal, conjecture, part_time_job_offered(james)).