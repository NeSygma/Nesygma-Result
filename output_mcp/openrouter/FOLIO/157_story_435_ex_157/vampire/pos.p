% Positive version
fof(premise1, axiom, ! [X] : (works_in_library(X) => ~from_cs_dept(X))).
fof(premise2, axiom, ! [X] : (part_time_job_univ(X) => works_in_library(X))).
fof(premise3, axiom, ! [X] : (taking_db_course(X) => from_cs_dept(X))).
fof(premise4, axiom, ! [X] : (taking_class_with_prof_david(X) => taking_db_course(X))).
fof(premise5, axiom, ! [X] : (works_in_lab(X) => taking_class_with_prof_david(X))).
fof(premise6, axiom, works_in_lab(james)).
% Interpreting the ambiguous statement as: ~works_in_lab(james) OR part_time_job_univ(james)
fof(premise7, axiom, (~works_in_lab(james) | part_time_job_univ(james))).
fof(goal, conjecture, part_time_job_univ(james)).