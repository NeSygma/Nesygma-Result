% Positive version
fof(distinct, axiom, (james != dummy)).
fof(premise1, axiom, ! [X] : (works_in_library(X) => ~from_cs_dept(X))).
fof(premise2, axiom, ! [X] : (has_part_time_job_univ(X) => works_in_library(X))).
fof(premise3, axiom, ! [X] : (takes_database_course(X) => from_cs_dept(X))).
fof(premise4, axiom, ! [X] : (takes_class_with_prof_david(X) => takes_database_course(X))).
fof(premise5, axiom, ! [X] : (works_in_lab(X) => takes_class_with_prof_david(X))).
fof(premise6, axiom, works_in_lab(james)).
% Premise7 as disjunction of negations
fof(premise7, axiom, (~works_in_lab(james) | ~has_part_time_job_univ(james))).
fof(goal, conjecture, ~has_part_time_job_univ(james)).