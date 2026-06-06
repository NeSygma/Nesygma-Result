fof(premise_1, axiom, ! [X] : (student(X) & works_in_library(X) => ~from_cs_dept(X))).
fof(premise_2, axiom, ! [X] : (student(X) & has_part_time_job(X) => works_in_library(X))).
fof(premise_3, axiom, ! [X] : (student(X) & taking_database_course(X) => from_cs_dept(X))).
fof(premise_4, axiom, ! [X] : (student(X) & taking_class_with_david(X) => taking_database_course(X))).
fof(premise_5, axiom, ! [X] : (student(X) & works_in_lab(X) => taking_class_with_david(X))).
fof(premise_6, axiom, student(james) & works_in_lab(james)).
fof(premise_7, axiom, ~works_in_lab(james) & ~has_part_time_job(james)).
fof(goal, conjecture, taking_database_course(james) | has_part_time_job(james)).