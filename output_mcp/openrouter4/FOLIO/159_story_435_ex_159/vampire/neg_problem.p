fof(distinct, axiom, $true).
fof(premise1, axiom, ! [X] : ((student(X) & works_library(X)) => ~cs_dept(X))).
fof(premise2, axiom, ! [X] : ((student(X) & has_part_time_job(X)) => works_library(X))).
fof(premise3, axiom, ! [X] : ((student(X) & takes_database(X)) => cs_dept(X))).
fof(premise4, axiom, ! [X] : ((student(X) & takes_class_with_david(X)) => takes_database(X))).
fof(premise5, axiom, ! [X] : ((student(X) & works_lab(X)) => takes_class_with_david(X))).
fof(premise6, axiom, (student(james) & works_lab(james))).
fof(premise7, axiom, (~works_lab(james) | ~has_part_time_job(james))).
fof(negated_conclusion, conjecture, (~takes_database(james) & ~has_part_time_job(james))).