fof(premise1, axiom, ! [X] : (works_in_library(X) => ~from_cs_department(X))).
fof(premise2, axiom, ! [X] : (has_part_time_job(X) => works_in_library(X))).
fof(premise3, axiom, ! [X] : (takes_database_course(X) => from_cs_department(X))).
fof(premise4, axiom, ! [X] : (takes_prof_david_class(X) => takes_database_course(X))).
fof(premise5, axiom, ! [X] : (works_in_lab(X) => takes_prof_david_class(X))).
fof(premise6, axiom, works_in_lab(james)).
fof(premise7, axiom, (~works_in_library(james) & ~has_part_time_job(james))).
fof(goal, conjecture, ~has_part_time_job(james)).