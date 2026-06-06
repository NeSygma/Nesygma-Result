fof(p1, axiom, ! [X] : ((student(X) & works_in_library(X)) => ~from_cs_dept(X))).
fof(p2, axiom, ! [X] : ((student(X) & has_uni_part_time_job(X)) => works_in_library(X))).
fof(p3, axiom, ! [X] : ((student(X) & taking_database_course(X)) => from_cs_dept(X))).
fof(p4, axiom, ! [X] : ((student(X) & taking_class_with_david(X)) => taking_database_course(X))).
fof(p5, axiom, ! [X] : ((student(X) & works_in_lab(X)) => taking_class_with_david(X))).
fof(p6, axiom, (student(james) & works_in_lab(james))).
fof(goal, conjecture, ~has_uni_part_time_job(james)).