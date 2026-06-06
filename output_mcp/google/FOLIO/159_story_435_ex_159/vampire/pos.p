fof(p1, axiom, ! [X] : ((student(X) & works_in_library(X)) => ~from_cs_dept(X))).
fof(p2, axiom, ! [X] : ((student(X) & has_uni_part_time_job(X)) => works_in_library(X))).
fof(p3, axiom, ! [X] : ((student(X) & takes_db_course(X)) => from_cs_dept(X))).
fof(p4, axiom, ! [X] : ((student(X) & takes_class_with_david(X)) => takes_db_course(X))).
fof(p5, axiom, ! [X] : ((student(X) & works_in_lab(X)) => takes_class_with_david(X))).
fof(p6, axiom, student(james)).
fof(p7, axiom, works_in_lab(james)).
fof(goal, conjecture, (takes_db_course(james) | has_uni_part_time_job(james))).