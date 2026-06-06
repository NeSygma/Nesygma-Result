fof(p1, axiom, ! [X] : ((student(X) & works_in_library(X)) => ~from_cs_dept(X))).
fof(p2, axiom, ! [X] : ((student(X) & part_time_job_uni(X)) => works_in_library(X))).
fof(p3, axiom, ! [X] : ((student(X) & taking_database(X)) => from_cs_dept(X))).
fof(p4, axiom, ! [X] : ((student(X) & taking_class_david(X)) => taking_database(X))).
fof(p5, axiom, ! [X] : ((student(X) & works_in_lab(X)) => taking_class_david(X))).
fof(p6, axiom, student(james)).
fof(p7, axiom, works_in_lab(james)).
fof(goal, conjecture, taking_database(james)).