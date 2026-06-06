fof(p1, axiom, ! [X] : (works_in_library(X) => ~from_cs_dept(X))).
fof(p2, axiom, ! [X] : (has_part_time_job(X) => works_in_library(X))).
fof(p3, axiom, ! [X] : (takes_database_course(X) => from_cs_dept(X))).
fof(p4, axiom, ! [X] : (takes_class_with_david(X) => takes_database_course(X))).
fof(p5, axiom, ! [X] : (works_in_lab(X) => takes_class_with_david(X))).
fof(p6, axiom, works_in_lab(james)).
fof(p7, axiom, ~works_in_lab(james) & ~has_part_time_job(james)).
fof(goal, conjecture, ~(takes_database_course(james) | has_part_time_job(james))).